"""
Unlock/Login screen
"""
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.gui.styles import button_style, input_style, frame_style
from src.gui.components.header import Header


class UnlockScreen(QWidget):
    def __init__(self, app, vault, on_success_callback):
        super().__init__()
        self.app = app
        self.vault = vault
        self.on_success = on_success_callback
        self.colors = app.colors
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header (minimal - just theme toggle)
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet(frame_style(self.colors['primary']))
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        theme_icon = "☀️" if self.app.current_theme == "dark" else "🌙"
        theme_btn = QPushButton(theme_icon)
        theme_btn.setFixedSize(40, 32)
        theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        theme_btn.setStyleSheet(button_style(
            self.colors['secondary'],
            self.colors['accent_cyan']
        ) + "font-size: 16px;")
        theme_btn.clicked.connect(self.app.toggle_theme)
        
        header_layout.addStretch()
        header_layout.addWidget(theme_btn)
        layout.addWidget(header)
        
        # Main content
        content = QWidget()
        content.setStyleSheet(f"background-color: {self.colors['bg_main']}; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Card
        card = QFrame()
        card.setFixedSize(420, 480)
        card.setStyleSheet(frame_style(self.colors['bg_card'], radius=12))
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(10)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo image
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "images", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet("background: transparent; border: none;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(logo_label)
        
        # Subtitle
        subtitle = QLabel("Local Developer Credentials Manager")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet(f"color: {self.colors['text_secondary']}; background: transparent; border: none;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        
        card_layout.addSpacing(20)
        
        # Form
        if self.vault.is_initialized():
            self.setup_unlock_form(card_layout)
        else:
            self.setup_init_form(card_layout)
        
        content_layout.addWidget(card)
        layout.addWidget(content, 1)
    
    def setup_unlock_form(self, layout):
        """Form for unlocking existing vault"""
        label = QLabel("Enter Master Password")
        label.setFont(QFont("Segoe UI", 14))
        label.setStyleSheet(f"color: {self.colors['text_primary']}; background: transparent; border: none;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Master Password")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setFixedHeight(45)
        self.password_entry.setStyleSheet(input_style(self.colors))
        self.password_entry.returnPressed.connect(self.unlock)
        layout.addWidget(self.password_entry)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {self.colors['accent_red']}; background: transparent; border: none;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        unlock_btn = QPushButton("Unlock Vault")
        unlock_btn.setFixedHeight(45)
        unlock_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        unlock_btn.setStyleSheet(button_style(
            self.colors['accent_cyan'],
            self.colors['primary'],
            radius=6
        ) + "font-size: 14px; font-weight: bold;")
        unlock_btn.clicked.connect(self.unlock)
        layout.addWidget(unlock_btn)
    
    def setup_init_form(self, layout):
        """Form for initializing new vault"""
        label = QLabel("Create Master Password")
        label.setFont(QFont("Segoe UI", 14))
        label.setStyleSheet(f"color: {self.colors['text_primary']}; background: transparent; border: none;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Master Password")
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setFixedHeight(45)
        self.password_entry.setStyleSheet(input_style(self.colors))
        layout.addWidget(self.password_entry)
        
        self.confirm_entry = QLineEdit()
        self.confirm_entry.setPlaceholderText("Confirm Password")
        self.confirm_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_entry.setFixedHeight(45)
        self.confirm_entry.setStyleSheet(input_style(self.colors))
        self.confirm_entry.returnPressed.connect(self.initialize)
        layout.addWidget(self.confirm_entry)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {self.colors['accent_red']}; background: transparent; border: none;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.error_label)
        
        create_btn = QPushButton("Create Vault")
        create_btn.setFixedHeight(45)
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.setStyleSheet(button_style(
            self.colors['accent_green'],
            "#1E8449",
            radius=6
        ) + "font-size: 14px; font-weight: bold;")
        create_btn.clicked.connect(self.initialize)
        layout.addWidget(create_btn)
    
    def unlock(self):
        password = self.password_entry.text()
        if not password:
            self.error_label.setText("Please enter your password")
            return
        
        if self.vault.unlock(password):
            self.on_success()
        else:
            self.error_label.setText("Invalid password")
            self.password_entry.clear()
    
    def initialize(self):
        password = self.password_entry.text()
        confirm = self.confirm_entry.text()
        
        if not password or not confirm:
            self.error_label.setText("Please fill in both fields")
            return
        
        if len(password) < 8:
            self.error_label.setText("Password must be at least 8 characters")
            return
        
        if password != confirm:
            self.error_label.setText("Passwords do not match")
            return
        
        if self.vault.initialize(password):
            self.on_success()
        else:
            self.error_label.setText("Failed to initialize vault")
