from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform
from database import insert_entry, init_db
from backup import create_backup, schedule_backup
from drive_upload import upload_to_drive
from datetime import datetime, timedelta
import calendar
import os
import threading
from kivy.logger import Logger

# OCR functionality (optional)
OCR_AVAILABLE = False
try:
    import pytesseract
    from PIL import Image
    
    # Set Tesseract path for Windows
    if platform != 'android':
        # Try common Windows installation paths
        tesseract_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
        ]
        
        for path in tesseract_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
    
    OCR_AVAILABLE = True
    Logger.info("OCR functionality available")
except ImportError as e:
    Logger.warning(f"OCR packages not available. Install pytesseract and pillow for OCR features.")
except Exception as e:
    Logger.warning(f"OCR initialization error: {e}")

class CPDScreen(Screen):
    dialog = None
    camera = None
    photo_path = None
    selected_activity_type = None
    selected_start_date = None
    selected_end_date = None
    selected_points = None  # For CPD points
    current_date_type = None  # 'start' or 'end'
    extracted_text = None  # For OCR text storage
    ocr_dialog = None  # For OCR text selection dialog
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.post_init, 0)
    
    def post_init(self, dt):
        """Initialize after the widget is built"""
        # Request permissions for Android
        if platform == 'android':
            self.request_android_permissions()
    
    def request_android_permissions(self):
        """Request camera and storage permissions on Android"""
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])
        except ImportError:
            Logger.info("CPD: Not on Android platform")
    
    def show_date_picker(self, date_type):
        """Show a mobile-friendly date picker"""
        self.current_date_type = date_type
        
        # Create main layout - NO padding at top, anchor to top
        content = BoxLayout(orientation='vertical', spacing=8, padding=[10, 0, 10, 10])
        
        # Header - normal size, positioned at very top
        header = Label(
            text=f"Select {date_type.title()} Date",
            size_hint_y=None,
            height='35dp',
            font_size='18sp',
            color=(0.2, 0.4, 0.8, 1),
            pos_hint={'top': 1}  # Anchor to top
        )
        content.add_widget(header)
        
        # Get current date
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        # Year selection - normal size, positioned high
        year_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=8)
        year_layout.add_widget(Label(text='Year:', size_hint_x=0.2, font_size='16sp'))
        
        year_buttons = BoxLayout(orientation='horizontal', spacing=5)
        for year in range(current_year - 2, current_year + 3):
            btn = Button(
                text=str(year),
                font_size='14sp',
                background_color=(0.2, 0.6, 1, 1) if year == current_year else (0.9, 0.9, 0.9, 1),
                color=(1, 1, 1, 1) if year == current_year else (0.2, 0.2, 0.2, 1)
            )
            btn.bind(on_release=lambda x, y=year: self.select_year(y))
            year_buttons.add_widget(btn)
        
        year_layout.add_widget(year_buttons)
        content.add_widget(year_layout)
        
        # Month selection - normal size
        month_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_y=None, height='90dp')
        month_layout.add_widget(Label(text='Month:', size_hint_y=None, height='25dp', font_size='16sp'))
        
        # First row of months - normal size
        month_row1 = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='30dp')
        for month in range(1, 7):
            btn = Button(
                text=calendar.month_abbr[month],
                font_size='12sp',
                background_color=(0.2, 0.6, 1, 1) if month == current_month else (0.9, 0.9, 0.9, 1),
                color=(1, 1, 1, 1) if month == current_month else (0.2, 0.2, 0.2, 1)
            )
            btn.bind(on_release=lambda x, m=month: self.select_month(m))
            month_row1.add_widget(btn)
        
        # Second row of months - normal size
        month_row2 = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height='30dp')
        for month in range(7, 13):
            btn = Button(
                text=calendar.month_abbr[month],
                font_size='12sp',
                background_color=(0.2, 0.6, 1, 1) if month == current_month else (0.9, 0.9, 0.9, 1),
                color=(1, 1, 1, 1) if month == current_month else (0.2, 0.2, 0.2, 1)
            )
            btn.bind(on_release=lambda x, m=month: self.select_month(m))
            month_row2.add_widget(btn)
        
        month_layout.add_widget(month_row1)
        month_layout.add_widget(month_row2)
        content.add_widget(month_layout)
        
        # Day selection grid - normal size
        self.day_grid = GridLayout(cols=7, spacing=2, size_hint_y=None, height='180dp')
        
        # Day headers - normal size
        for day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
            self.day_grid.add_widget(Label(text=day, font_size='12sp', size_hint_y=None, height='25dp'))
        
        # Generate calendar for current month
        self.selected_year = current_year
        self.selected_month = current_month
        self.update_calendar()
        
        content.add_widget(self.day_grid)
        
        # Action buttons - normal size
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='45dp')
        
        cancel_btn = Button(text='Cancel', background_color=(0.8, 0.4, 0.4, 1), font_size='14sp')
        cancel_btn.bind(on_release=self.close_date_picker)
        
        today_btn = Button(text='Today', background_color=(0.4, 0.8, 0.4, 1), font_size='14sp')
        today_btn.bind(on_release=self.select_today)
        
        button_layout.add_widget(cancel_btn)
        button_layout.add_widget(today_btn)
        content.add_widget(button_layout)
        
        # Create and show popup directly with content (no wrapper)
        self.dialog = Popup(
            title='Select Date',
            content=content,
            size_hint=(0.9, 0.75),
            auto_dismiss=False
        )
        self.dialog.open()
    
    def select_year(self, year):
        """Handle year selection"""
        self.selected_year = year
        self.update_calendar()
        
        # Update year button colors directly from dialog content
        content = self.dialog.content
        if hasattr(content, 'children'):
            for child in content.children:
                if isinstance(child, BoxLayout) and hasattr(child, 'children') and len(child.children) == 2:
                    # This is the year layout
                    year_buttons_container = child.children[0]  # year_buttons BoxLayout
                    if isinstance(year_buttons_container, BoxLayout):
                        for btn in year_buttons_container.children:
                            if hasattr(btn, 'text') and btn.text.isdigit():
                                if int(btn.text) == year:
                                    btn.background_color = (0.2, 0.6, 1, 1)
                                    btn.color = (1, 1, 1, 1)  # White text for selected
                                else:
                                    btn.background_color = (0.9, 0.9, 0.9, 1)
                                    btn.color = (0.2, 0.2, 0.2, 1)  # Dark text for unselected
    
    def select_month(self, month):
        """Handle month selection"""
        self.selected_month = month
        self.update_calendar()
        
        # Update month button colors directly from dialog content  
        content = self.dialog.content
        if hasattr(content, 'children'):
            for child in content.children:
                if isinstance(child, BoxLayout) and hasattr(child, 'children'):
                    # Look for month layout (has month rows)
                    for subchild in child.children:
                        if isinstance(subchild, BoxLayout):
                            for btn in subchild.children:
                                if hasattr(btn, 'text') and btn.text in calendar.month_abbr:
                                    month_num = list(calendar.month_abbr).index(btn.text)
                                    if month_num == month:
                                        btn.background_color = (0.2, 0.6, 1, 1)
                                        btn.color = (1, 1, 1, 1)  # White text for selected
                                    else:
                                        btn.background_color = (0.9, 0.9, 0.9, 1)
                                        btn.color = (0.2, 0.2, 0.2, 1)  # Dark text for unselected
    
    def update_calendar(self):
        """Update the calendar grid for the selected month/year"""
        # Clear existing day buttons (keep headers)
        while len(self.day_grid.children) > 7:
            self.day_grid.remove_widget(self.day_grid.children[0])
        
        # Get calendar for selected month
        cal = calendar.monthcalendar(self.selected_year, self.selected_month)
        
        # Add day buttons - normal size
        for week in cal:
            for day in week:
                if day == 0:
                    # Empty day
                    self.day_grid.add_widget(Label(text='', size_hint_y=None, height='25dp'))
                else:
                    btn = Button(
                        text=str(day),
                        font_size='12sp',
                        size_hint_y=None,
                        height='25dp',
                        background_color=(0.9, 0.9, 0.9, 1)
                    )
                    btn.bind(on_release=lambda x, d=day: self.select_day(d))
                    self.day_grid.add_widget(btn)
    
    def select_day(self, day):
        """Handle day selection"""
        selected_date = datetime(self.selected_year, self.selected_month, day)
        date_str = selected_date.strftime("%Y-%m-%d")
        
        if self.current_date_type == 'start':
            self.selected_start_date = date_str
            self.ids.date_start_btn.text = f"Start: {date_str}"
            self.ids.date_start_btn.background_color = (0.2, 0.6, 1, 1)
            self.ids.date_start_btn.color = (1, 1, 1, 1)  # White text for visibility
        else:
            self.selected_end_date = date_str
            self.ids.date_end_btn.text = f"End: {date_str}"
            self.ids.date_end_btn.background_color = (0.2, 0.6, 1, 1)
            self.ids.date_end_btn.color = (1, 1, 1, 1)  # White text for visibility
        
        self.close_date_picker()
    
    def select_today(self, instance):
        """Select today's date"""
        today = datetime.now()
        self.select_day(today.day)
    
    def close_date_picker(self, *args):
        """Close the date picker"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
    
    def show_points_selector(self):
        """Show points selection popup"""
        # Create popup content
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Title
        title_label = Label(
            text='Select CPD Points',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1)
        )
        content.add_widget(title_label)
        
        # Points grid - common point values
        points_grid = GridLayout(cols=5, spacing=10, size_hint_y=None, height=150)
        
        # Common point values (-, 0 through 12)
        point_values = ['-', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 'Clear']
        
        for value in point_values:
            if value == '-':
                btn = Button(
                    text='-',
                    background_color=(0.6, 0.6, 0.6, 1),
                    color=(1, 1, 1, 1),
                    font_size='16sp'
                )
                btn.bind(on_release=lambda x: self.select_points(None))
            elif value == 'Clear':
                btn = Button(
                    text='Clear',
                    background_color=(0.8, 0.2, 0.2, 1),
                    color=(1, 1, 1, 1),
                    font_size='14sp'
                )
                btn.bind(on_release=lambda x: self.select_points(None))
            else:
                btn = Button(
                    text=str(value),
                    background_color=(0.2, 0.6, 1, 1),
                    color=(1, 1, 1, 1),
                    font_size='16sp'
                )
                btn.bind(on_release=lambda x, p=value: self.select_points(p))
            
            points_grid.add_widget(btn)
        
        content.add_widget(points_grid)
        
        # Close button
        close_btn = Button(
            text='Cancel',
            size_hint_y=None,
            height=50,
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        close_btn.bind(on_release=self.close_points_selector)
        content.add_widget(close_btn)
        
        # Create and show popup
        self.points_dialog = Popup(
            title='CPD Points',
            content=content,
            size_hint=(0.8, 0.7),
            auto_dismiss=False
        )
        self.points_dialog.open()
    
    def select_points(self, points):
        """Handle points selection"""
        if points is None:
            self.selected_points = None
            self.ids.points_btn.text = "Select Points (Optional)"
            self.ids.points_btn.background_color = (0.9, 0.9, 0.9, 1)
            self.ids.points_btn.color = (0.2, 0.2, 0.2, 1)  # Dark text
        else:
            self.selected_points = points
            self.ids.points_btn.text = f"Points: {points}"
            self.ids.points_btn.background_color = (0.2, 0.6, 1, 1)
            self.ids.points_btn.color = (1, 1, 1, 1)  # White text for visibility
        
        self.close_points_selector()
    
    def close_points_selector(self, *args):
        """Close the points selector"""
        if hasattr(self, 'points_dialog') and self.points_dialog:
            self.points_dialog.dismiss()
            self.points_dialog = None
    
    def show_error(self, message):
        """Show error message"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        content.add_widget(Label(text=message, font_size='14sp'))
        
        close_btn = Button(text='OK', size_hint_y=None, height=50)
        content.add_widget(close_btn)
        
        error_popup = Popup(
            title='Error',
            content=content,
            size_hint=(0.6, 0.3),
            auto_dismiss=False
        )
        close_btn.bind(on_release=error_popup.dismiss)
        error_popup.open()

    def select_type(self, activity_type):
        """Handle activity type selection"""
        self.selected_activity_type = activity_type
        
        # Reset all buttons to normal state
        button_ids = ['type_paper', 'type_conference', 'type_project', 'type_course', 'type_other']
        for button_id in button_ids:
            if hasattr(self.ids, button_id):
                self.ids[button_id].background_color = (1, 1, 1, 1)  # Default white
        
        # Highlight selected button
        button_map = {
            'Paper': 'type_paper',
            'Conference': 'type_conference',
            'Project': 'type_project',
            'Course': 'type_course',
            'Other': 'type_other'
        }
        
        if activity_type in button_map and hasattr(self.ids, button_map[activity_type]):
            self.ids[button_map[activity_type]].background_color = (0.2, 0.6, 1, 1)  # Light blue
        
        # Update label
        self.ids.selected_type.text = f"Selected: {activity_type}"
        self.ids.selected_type.color = (0.2, 0.4, 0.8, 1)  # Blue color
    
    def validate_dates(self):
        """Validate date inputs"""
        if not self.selected_start_date or not self.selected_end_date:
            return False, "Please select both start and end dates"
        
        try:
            start_date = datetime.strptime(self.selected_start_date, "%Y-%m-%d")
            end_date = datetime.strptime(self.selected_end_date, "%Y-%m-%d")
            if end_date < start_date:
                return False, "End date cannot be before start date"
            return True, ""
        except ValueError:
            return False, "Invalid date format"
    
    def validate_form(self):
        """Validate all form inputs"""
        if not self.selected_start_date:
            return False, "Please select start date"
        if not self.selected_end_date:
            return False, "Please select end date"
        if not self.ids.name.text.strip():
            return False, "Name is required"
        if not self.selected_activity_type:
            return False, "Please select an activity type"
        if not self.ids.description.text.strip():
            return False, "Description is required"
        
        date_valid, date_error = self.validate_dates()
        if not date_valid:
            return False, date_error
        
        return True, ""
    
    def show_error_dialog(self, message):
        """Show error dialog"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message, text_size=(None, None)))
        
        button = Button(text='OK', size_hint=(1, 0.3))
        content.add_widget(button)
        
        self.dialog = Popup(title='Error', content=content, size_hint=(0.8, 0.4))
        button.bind(on_release=self.dialog.dismiss)
        self.dialog.open()
    
    def take_photo(self):
        """Open camera to take photo"""
        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.8))
        content.add_widget(self.camera)
        
        button_layout = BoxLayout(orientation="horizontal", spacing=10, size_hint=(1, 0.2))
        
        capture_btn = Button(text="Capture")
        capture_btn.bind(on_release=self.capture_photo)
        
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_release=self.close_camera)
        
        button_layout.add_widget(capture_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        self.dialog = Popup(title="Take Photo", content=content, size_hint=(0.8, 0.8))
        self.dialog.open()
    
    def capture_photo(self, *args):
        """Capture and save photo with OCR processing"""
        if self.camera:
            # Create dedicated phone folder structure
            if platform == 'android':
                # Use Android external storage
                try:
                    from android.storage import primary_external_storage_path
                    base_path = primary_external_storage_path()
                    photos_dir = os.path.join(base_path, "CPD_Tracker", "Photos")
                except ImportError:
                    # Fallback for development
                    photos_dir = os.path.join("cpd_tracker", "assets", "photos")
            else:
                # Development/Desktop path
                photos_dir = os.path.join("cpd_tracker", "assets", "photos")
                
            os.makedirs(photos_dir, exist_ok=True)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cpd_photo_{timestamp}.png"
            self.photo_path = os.path.join(photos_dir, filename)
            
            # Export camera texture
            self.camera.export_to_png(self.photo_path)
            
            # Update UI
            self.ids.photo_status.text = f"Photo saved: {filename}"
            self.ids.photo_status.color = (0.2, 0.6, 0.2, 1)  # Green color
            
            # Close camera first
            self.close_camera()
            
            # Process OCR if available
            if OCR_AVAILABLE:
                Clock.schedule_once(lambda dt: self.process_ocr(), 0.5)
            else:
                # Schedule Google Drive sync directly if no OCR
                self.schedule_drive_sync()
    
    def schedule_drive_sync(self):
        """Schedule Google Drive sync for photos and database"""
        try:
            # Schedule sync in background thread
            threading.Thread(target=self.sync_to_drive, daemon=True).start()
        except Exception as e:
            Logger.error(f"CPD: Error scheduling drive sync: {e}")
    
    def sync_to_drive(self):
        """Sync photos and database to Google Drive"""
        try:
            # Import drive upload function
            from drive_upload import upload_to_drive
            
            # Upload recent photo if exists
            if self.photo_path and os.path.exists(self.photo_path):
                upload_to_drive(self.photo_path, f"CPD_Photos/{os.path.basename(self.photo_path)}")
            
            # Create and upload database backup
            create_backup()
            
            Logger.info("CPD: Successfully synced to Google Drive")
        except Exception as e:
            Logger.error(f"CPD: Error syncing to Drive: {e}")

    def process_ocr(self):
        """Process captured photo with OCR and show text selection dialog"""
        try:
            # Load and process image
            image = Image.open(self.photo_path)
            
            # Extract text using pytesseract
            extracted_text = pytesseract.image_to_string(image, config='--psm 6')
            
            if extracted_text.strip():
                # Store extracted text for selection
                self.extracted_text = extracted_text.strip()
                
                # Show text selection dialog
                self.show_ocr_dialog()
            else:
                # No text found
                self.show_message("OCR Result", "No readable text found in the image.")
                self.schedule_drive_sync()
                
        except pytesseract.TesseractNotFoundError:
            # Tesseract executable not found
            self.show_message(
                "OCR Setup Required", 
                "Tesseract OCR engine is not installed.\n\n"
                "For Windows:\n"
                "1. Download from: github.com/UB-Mannheim/tesseract/wiki\n"
                "2. Install the executable\n"
                "3. Add to PATH environment variable\n\n"
                "For Android: OCR will work automatically in the compiled app."
            )
            self.schedule_drive_sync()
        except Exception as e:
            Logger.warning(f"OCR Error: Failed to process image: {e}")
            self.show_message("OCR Error", f"Failed to extract text from image.\nError: {str(e)}")
            self.schedule_drive_sync()
    
    def show_ocr_dialog(self):
        """Show dialog for OCR text selection"""
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView
        from kivy.metrics import dp
        
        # Create dialog content
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Title
        title_label = Label(
            text="OCR Text Extracted",
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.4, 0.8, 1)
        )
        content.add_widget(title_label)
        
        # Instruction
        instruction = Label(
            text="Select and edit the text to use in description:",
            size_hint_y=None,
            height=dp(25),
            text_size=(None, None)
        )
        content.add_widget(instruction)
        
        # Scrollable text input for editing
        text_scroll = ScrollView(size_hint=(1, 0.6))
        self.ocr_text_input = TextInput(
            text=self.extracted_text,
            multiline=True,
            size_hint_y=None,
            text_size=(None, None)
        )
        self.ocr_text_input.bind(texture_size=self.ocr_text_input.setter('size'))
        text_scroll.add_widget(self.ocr_text_input)
        content.add_widget(text_scroll)
        
        # Button layout
        button_layout = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        
        # Use text button
        use_button = Button(
            text="Use This Text",
            background_color=(0.2, 0.6, 0.2, 1)
        )
        use_button.bind(on_release=self.use_ocr_text)
        button_layout.add_widget(use_button)
        
        # Skip button
        skip_button = Button(
            text="Skip",
            background_color=(0.6, 0.2, 0.2, 1)
        )
        skip_button.bind(on_release=self.skip_ocr_text)
        button_layout.add_widget(skip_button)
        
        content.add_widget(button_layout)
        
        # Create and show popup
        self.ocr_dialog = Popup(
            title="OCR Text Selection",
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        self.ocr_dialog.open()
    
    def use_ocr_text(self, *args):
        """Use selected OCR text in description field"""
        if self.ocr_text_input and self.ocr_text_input.text.strip():
            # Get current description text
            current_desc = self.ids.description.text
            
            # Append OCR text to description (or replace if empty)
            if current_desc.strip():
                new_desc = f"{current_desc}\n\n{self.ocr_text_input.text.strip()}"
            else:
                new_desc = self.ocr_text_input.text.strip()
            
            # Update description field
            self.ids.description.text = new_desc
            
            # Show confirmation
            self.show_message("OCR Success", "Text added to description field!")
        
        # Close dialog and sync
        if self.ocr_dialog:
            self.ocr_dialog.dismiss()
        self.schedule_drive_sync()
    
    def show_message(self, title, message):
        """Show a simple message popup"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Message label
        msg_label = Label(
            text=message,
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        content.add_widget(msg_label)
        
        # OK button
        ok_button = Button(
            text="OK",
            size_hint=(1, None),
            height=40
        )
        content.add_widget(ok_button)
        
        # Create popup
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )
        
        # Bind OK button to close popup
        ok_button.bind(on_release=popup.dismiss)
        
        popup.open()

    def skip_ocr_text(self, *args):
        """Skip OCR text and continue"""
        if self.ocr_dialog:
            self.ocr_dialog.dismiss()
        self.schedule_drive_sync()

    def close_camera(self, *args):
        """Close camera dialog"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        self.camera = None
    
    def clear_form(self):
        """Clear all form fields"""
        # Reset date picker values
        self.selected_start_date = None
        self.selected_end_date = None
        self.ids.date_start_btn.text = "📅 Select Start Date"
        self.ids.date_start_btn.background_color = (1, 1, 1, 1)
        self.ids.date_start_btn.color = (0.2, 0.2, 0.2, 1)  # Dark text
        self.ids.date_end_btn.text = "📅 Select End Date"
        self.ids.date_end_btn.background_color = (1, 1, 1, 1)
        self.ids.date_end_btn.color = (0.2, 0.2, 0.2, 1)  # Dark text
        
        self.ids.name.text = ""
        self.selected_activity_type = None
        
        # Reset points selection
        self.selected_points = None
        self.ids.points_btn.text = "Select Points (Optional)"
        self.ids.points_btn.background_color = (0.9, 0.9, 0.9, 1)
        
        # Reset all type buttons
        button_ids = ['type_paper', 'type_conference', 'type_project', 'type_course', 'type_other']
        for button_id in button_ids:
            if hasattr(self.ids, button_id):
                self.ids[button_id].background_color = (1, 1, 1, 1)  # Default white
        
        self.ids.selected_type.text = "No type selected"
        self.ids.selected_type.color = (0.6, 0.6, 0.6, 1)  # Gray color
        self.ids.description.text = ""
        self.ids.photo_status.text = "No photo taken"
        self.ids.photo_status.color = (0.6, 0.6, 0.6, 1)  # Gray color
        self.ids.status.text = ""
        self.photo_path = None
    
    def submit_entry(self):
        """Submit CPD entry after validation"""
        # Validate form
        is_valid, error_message = self.validate_form()
        if not is_valid:
            self.show_error_dialog(error_message)
            return
        
        # Prepare data
        data = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date_start": self.selected_start_date,
            "date_end": self.selected_end_date,
            "name": self.ids.name.text,
            "type": self.selected_activity_type,
            "description": self.ids.description.text,
            "photo": self.photo_path if self.photo_path else "",
            "points": self.selected_points if self.selected_points is not None else 0
        }
        
        try:
            # Insert entry
            insert_entry(data)
            self.ids.status.text = "✓ Entry saved successfully!"
            self.ids.status.color = (0.2, 0.6, 0.2, 1)  # Green color
            
            # Schedule Google Drive sync
            self.schedule_drive_sync()
            
            # Clear form
            Clock.schedule_once(lambda dt: self.clear_form(), 2)
            
            # Check if backup is needed (every 2 weeks)
            schedule_backup()
            
        except Exception as e:
            self.ids.status.text = f"Error: {str(e)}"
            self.ids.status.color = (0.8, 0.2, 0.2, 1)  # Red color
            Logger.error(f"CPD: Error saving entry: {e}")

    def export_to_csv(self):
        """Export all CPD entries to CSV file"""
        try:
            import csv
            import sqlite3
            from datetime import datetime
            
            # Connect to database
            db_path = os.path.join("cpd_tracker", "cpd.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all entries
            cursor.execute("""
                SELECT date_created, date_start, date_end, name, type, description, points, photo
                FROM cpd_entries 
                ORDER BY date_start DESC
            """)
            entries = cursor.fetchall()
            conn.close()
            
            if not entries:
                self.show_error("No entries found to export")
                return
            
            # Create export directory in dedicated folder
            if platform == 'android':
                try:
                    from android.storage import primary_external_storage_path
                    base_path = primary_external_storage_path()
                    export_dir = os.path.join(base_path, "CPD_Tracker", "Exports")
                except ImportError:
                    export_dir = os.path.join("cpd_tracker", "exports")
            else:
                export_dir = os.path.join("cpd_tracker", "exports")
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cpd_export_{timestamp}.csv"
            filepath = os.path.join(export_dir, filename)
            
            # Write CSV file
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'Entry Date', 'Start Date', 'End Date', 'Activity Name', 
                    'Activity Type', 'Description', 'CPD Points', 'Photo'
                ])
                
                # Write data
                for entry in entries:
                    writer.writerow(entry)
            
            # Show success message
            self.show_success_dialog(f"✓ Export successful!\n\nFile saved as:\n{filename}\n\nLocation: {export_dir}\n\nTotal entries: {len(entries)}")
            
            # Schedule Google Drive sync for export
            try:
                threading.Thread(target=lambda: upload_to_drive(filepath, f"CPD_Exports/{filename}"), daemon=True).start()
            except Exception as sync_error:
                Logger.error(f"CPD: Export sync error: {sync_error}")
            
        except Exception as e:
            self.show_error(f"Export failed: {str(e)}")
            Logger.error(f"CPD: Export error: {e}")

    def show_success_dialog(self, message):
        """Show success dialog"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(
            text=message, 
            font_size='14sp',
            text_size=(400, None),
            halign='center',
            valign='center'
        )
        content.add_widget(label)
        
        button = Button(
            text='OK', 
            size_hint_y=None, 
            height=50,
            background_color=(0.2, 0.8, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        content.add_widget(button)
        
        success_popup = Popup(
            title='Success', 
            content=content, 
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        button.bind(on_release=success_popup.dismiss)
        success_popup.open()

class CPDApp(App):
    def build(self):
        self.title = "CPD Tracker"
        
        # Initialize database
        init_db()
        
        return Builder.load_file("cpd.kv")
    
    def on_start(self):
        """Called when the app starts"""
        # Create dedicated phone storage structure
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                base_path = primary_external_storage_path()
                app_dir = os.path.join(base_path, "CPD_Tracker")
                photos_dir = os.path.join(app_dir, "Photos")
                backups_dir = os.path.join(app_dir, "Backups")
                exports_dir = os.path.join(app_dir, "Exports")
            except ImportError:
                # Fallback for development
                app_dir = "cpd_tracker"
                photos_dir = os.path.join(app_dir, "assets", "photos")
                backups_dir = os.path.join(app_dir, "backups")
                exports_dir = os.path.join(app_dir, "exports")
        else:
            # Development/Desktop structure
            app_dir = "cpd_tracker"
            photos_dir = os.path.join(app_dir, "assets", "photos")
            backups_dir = os.path.join(app_dir, "backups")
            exports_dir = os.path.join(app_dir, "exports")
            
        # Create all necessary directories
        os.makedirs(photos_dir, exist_ok=True)
        os.makedirs(backups_dir, exist_ok=True)
        os.makedirs(exports_dir, exist_ok=True)
        
        Logger.info(f"CPD: Created app directories in {app_dir}")

if __name__ == "__main__":
    CPDApp().run()
