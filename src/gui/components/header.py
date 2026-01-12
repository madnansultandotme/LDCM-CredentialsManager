"""
Header component for the application
"""
import os
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.gui.styles import button_style


class Header(QFrame):
    def __init__(self, colors, title, on_theme_toggle, on_lock=None, theme="dark"):
        super().__init__()
        self.colors = colors
        self.theme = theme
        
        self.setFixedHeight(60)
        self.setStyleSheet(f"background-color: {colors['primary']}; border: none;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo image
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "images", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaledToHeight(40, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(logo_label)
        
        layout.addSpacing(10)
        
        # Dashboard text
        dash_label = QLabel("Dashboard")
        dash_label.setFont(QFont("Segoe UI", 14))
        dash_label.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        layout.addWidget(dash_label)
        
        layout.addStretch()
        
        # Theme toggle
        theme_icon = "☀️" if theme == "dark" else "🌙"
        self.theme_btn = QPushButton(theme_icon)
        self.theme_btn.setFixedSize(40, 36)
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setStyleSheet(button_style(
            colors['secondary'], 
            colors['accent_cyan']
        ) + "font-size: 16px;")
        self.theme_btn.clicked.connect(on_theme_toggle)
        layout.addWidget(self.theme_btn)
        
        # Lock button (optional)
        if on_lock:
            lock_btn = QPushButton("🔒 Lock")
            lock_btn.setFixedSize(80, 36)
            lock_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            lock_btn.setStyleSheet(button_style(
                colors['accent_red'], 
                "#C0392B"
            ) + "font-size: 13px;")
            lock_btn.clicked.connect(on_lock)
            layout.addWidget(lock_btn)
            layout.addWidget(lock_btn)
