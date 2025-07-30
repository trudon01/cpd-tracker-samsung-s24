#!/usr/bin/env python3
"""
Samsung S24 Configuration Test
This sets the window size to simulate Samsung Galaxy S24 screen dimensions
"""

import os
from kivy.config import Config

# Samsung Galaxy S24 specifications:
# Resolution: 1080 x 2340 pixels
# For desktop testing, we'll scale it down but maintain aspect ratio
# Scale factor: 0.5 for comfortable desktop viewing
width = int(1080 * 0.5)   # 540px
height = int(2340 * 0.5)  # 1170px

# Configure window for S24 simulation
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 100)
Config.set('graphics', 'top', 50)
Config.write()

# Import and run the main app
from kivy.lang import Builder
from main import CPDApp
from kivy.app import App

class CPDS24App(CPDApp):
    def build(self):
        self.title = "CPD Tracker - Samsung S24 Mode"
        
        # Initialize database
        from database import init_db
        init_db()
        
        return Builder.load_file("cpd.kv")

if __name__ == "__main__":
    print(f"Samsung S24 Simulation Mode")
    print(f"Window Size: {width}x{height} (50% scale of actual S24)")
    print(f"Actual S24 Resolution: 1080x2340")
    print("=" * 50)
    
    app = CPDS24App()
    app.run()
