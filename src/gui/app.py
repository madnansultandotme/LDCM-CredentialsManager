"""
Main application window
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from src.config import COLORS, APP_NAME, APP_VERSION, DB_NAME
from src.vault import VaultManager
from src.gui.styles import get_global_styles
from src.gui.screens.unlock import UnlockScreen
from src.gui.screens.dashboard import DashboardScreen


class LDCMApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Theme state
        self.current_theme = "dark"
        self.colors = COLORS["dark"]
        
        # Configure window
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Initialize vault
        db_path = os.path.join(os.path.expanduser("~"), ".ldcm", DB_NAME)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.vault = VaultManager(db_path)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Current screen
        self.current_screen = None
        
        # Apply theme and show screen
        self.apply_theme()
        self.show_unlock_screen()
    
    def apply_theme(self):
        """Apply current theme colors and global styles"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.colors["bg_main"]};
            }}
            {get_global_styles(self.colors)}
        """)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.colors = COLORS[self.current_theme]
        self.apply_theme()
        
        # Rebuild current screen
        if self.vault.is_unlocked:
            self.show_dashboard()
        else:
            self.show_unlock_screen()
    
    def show_unlock_screen(self):
        if self.current_screen:
            self.current_screen.setParent(None)
            self.current_screen.deleteLater()
        self.current_screen = UnlockScreen(self, self.vault, self.on_unlock_success)
        self.layout.addWidget(self.current_screen)
    
    def show_dashboard(self):
        if self.current_screen:
            self.current_screen.setParent(None)
            self.current_screen.deleteLater()
        self.current_screen = DashboardScreen(self, self.vault, self.on_lock)
        self.layout.addWidget(self.current_screen)
    
    def on_unlock_success(self):
        self.show_dashboard()
    
    def on_lock(self):
        self.vault.lock()
        self.show_unlock_screen()


def run():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = LDCMApp()
    window.show()
    sys.exit(app.exec())
