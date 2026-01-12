"""
Dialog components for the application
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QFileDialog, QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from src.gui.styles import button_style, input_style
from src.injector import InjectionEngine


class AddProjectDialog(QDialog):
    def __init__(self, parent, colors):
        super().__init__(parent)
        self.colors = colors
        self.setWindowTitle("Add Project")
        self.setFixedSize(500, 320)
        self.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Create New Project")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['primary']}; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Enter a name for your new project")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet(f"color: {colors['text_secondary']}; border: none;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(10)
        
        # Project name input
        name_label = QLabel("Project Name")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(name_label)
        
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("e.g., My Awesome Project")
        self.name_entry.setFixedHeight(45)
        self.name_entry.setStyleSheet(input_style(colors) + "font-size: 14px;")
        layout.addWidget(self.name_entry)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(45)
        cancel_btn.setMinimumWidth(140)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(button_style(colors['secondary'], colors['primary']) + "font-size: 14px;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn, 1)
        
        create_btn = QPushButton("Create Project")
        create_btn.setFixedHeight(45)
        create_btn.setMinimumWidth(140)
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.setStyleSheet(button_style(colors['accent_green'], "#1E8449") + "font-size: 14px; font-weight: bold;")
        create_btn.clicked.connect(self.accept)
        btn_layout.addWidget(create_btn, 1)
        
        layout.addLayout(btn_layout)
    
    def get_result(self):
        return self.name_entry.text().strip()


class AddSecretDialog(QDialog):
    def __init__(self, parent, colors):
        super().__init__(parent)
        self.colors = colors
        self.setWindowTitle("Add Secret")
        self.setFixedSize(450, 300)
        self.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Add New Secret")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['primary']}; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Key input
        key_label = QLabel("Key")
        key_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        key_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(key_label)
        
        self.key_entry = QLineEdit()
        self.key_entry.setPlaceholderText("e.g., API_KEY")
        self.key_entry.setFixedHeight(40)
        self.key_entry.setStyleSheet(input_style(colors))
        layout.addWidget(self.key_entry)
        
        # Value input
        value_label = QLabel("Value")
        value_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(value_label)
        
        self.value_entry = QLineEdit()
        self.value_entry.setPlaceholderText("Secret value")
        self.value_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.value_entry.setFixedHeight(40)
        self.value_entry.setStyleSheet(input_style(colors))
        layout.addWidget(self.value_entry)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(button_style(colors['secondary'], colors['primary']))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn, 1)
        
        add_btn = QPushButton("Add Secret")
        add_btn.setFixedHeight(42)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(button_style(colors['accent_green'], "#1E8449") + "font-weight: bold;")
        add_btn.clicked.connect(self.accept)
        btn_layout.addWidget(add_btn, 1)
        
        layout.addLayout(btn_layout)
    
    def get_result(self):
        return self.key_entry.text().strip(), self.value_entry.text()


class EditSecretDialog(QDialog):
    def __init__(self, parent, colors, secret, decrypted_value):
        super().__init__(parent)
        self.colors = colors
        self.setWindowTitle("Edit Secret")
        self.setFixedSize(450, 300)
        self.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit Secret")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['primary']}; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Key input
        key_label = QLabel("Key")
        key_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        key_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(key_label)
        
        self.key_entry = QLineEdit()
        self.key_entry.setText(secret.key)
        self.key_entry.setFixedHeight(40)
        self.key_entry.setStyleSheet(input_style(colors))
        layout.addWidget(self.key_entry)
        
        # Value input
        value_label = QLabel("Value")
        value_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(value_label)
        
        self.value_entry = QLineEdit()
        self.value_entry.setText(decrypted_value)
        self.value_entry.setFixedHeight(40)
        self.value_entry.setStyleSheet(input_style(colors))
        layout.addWidget(self.value_entry)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(42)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(button_style(colors['secondary'], colors['primary']))
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn, 1)
        
        save_btn = QPushButton("Save Changes")
        save_btn.setFixedHeight(42)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(button_style(colors['accent_cyan'], colors['primary']) + "font-weight: bold;")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn, 1)
        
        layout.addLayout(btn_layout)
    
    def get_result(self):
        return self.key_entry.text().strip(), self.value_entry.text()


class InjectDialog(QDialog):
    def __init__(self, parent, colors, secrets):
        super().__init__(parent)
        self.colors = colors
        self.secrets = secrets
        self.selected_folder = None
        self.setWindowTitle("Inject Secrets")
        self.setFixedSize(550, 480)
        self.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Inject & Run")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {colors['primary']}; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Folder selection section
        folder_label = QLabel("Working Directory")
        folder_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        folder_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(folder_label)
        
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(10)
        
        self.folder_entry = QLineEdit()
        self.folder_entry.setPlaceholderText("Select a folder...")
        self.folder_entry.setFixedHeight(40)
        self.folder_entry.setReadOnly(True)
        self.folder_entry.setStyleSheet(input_style(colors))
        folder_layout.addWidget(self.folder_entry, 1)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
        browse_btn.setIconSize(QSize(16, 16))
        browse_btn.setFixedSize(100, 40)
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet(button_style(colors['secondary'], colors['primary']))
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(browse_btn)
        
        layout.addLayout(folder_layout)
        
        # Command input section
        cmd_label = QLabel("Command to Run")
        cmd_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        cmd_label.setStyleSheet(f"color: {colors['text_primary']}; border: none;")
        layout.addWidget(cmd_label)
        
        self.cmd_entry = QLineEdit()
        self.cmd_entry.setPlaceholderText("e.g., npm start, python app.py")
        self.cmd_entry.setFixedHeight(40)
        self.cmd_entry.setStyleSheet(input_style(colors))
        layout.addWidget(self.cmd_entry)
        
        layout.addSpacing(15)
        
        # Run command button (primary action)
        run_btn = QPushButton("  Run Command with Secrets")
        run_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        run_btn.setIconSize(QSize(18, 18))
        run_btn.setFixedHeight(48)
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.setStyleSheet(button_style(colors['accent_green'], "#1E8449") + "font-size: 14px; font-weight: bold;")
        run_btn.clicked.connect(self.run_command)
        layout.addWidget(run_btn)
        
        layout.addSpacing(10)
        
        # Secondary actions in a row
        secondary_layout = QHBoxLayout()
        secondary_layout.setSpacing(10)
        
        # Open terminal button
        terminal_btn = QPushButton("  Open Terminal")
        terminal_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        terminal_btn.setIconSize(QSize(16, 16))
        terminal_btn.setFixedHeight(42)
        terminal_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        terminal_btn.setStyleSheet(button_style(colors['accent_cyan'], colors['primary']) + "font-size: 13px;")
        terminal_btn.clicked.connect(self.open_terminal)
        secondary_layout.addWidget(terminal_btn, 1)
        
        # Generate .env button
        env_btn = QPushButton("  Generate .env")
        env_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        env_btn.setIconSize(QSize(16, 16))
        env_btn.setFixedHeight(42)
        env_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        env_btn.setStyleSheet(button_style(colors['secondary'], colors['primary']) + "font-size: 13px;")
        env_btn.clicked.connect(self.generate_env)
        secondary_layout.addWidget(env_btn, 1)
        
        layout.addLayout(secondary_layout)
        
        layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(button_style(colors['bg_main'], colors['secondary']) + f"color: {colors['text_secondary']};")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Working Directory")
        if folder:
            self.selected_folder = folder
            self.folder_entry.setText(folder)
    
    def open_terminal(self):
        InjectionEngine.inject_shell(self.secrets, working_dir=self.selected_folder)
        self.accept()
    
    def generate_env(self):
        if self.selected_folder:
            import os
            output_path = os.path.join(self.selected_folder, '.env')
            InjectionEngine.generate_env_file(self.secrets, output_path)
        else:
            InjectionEngine.generate_env_file(self.secrets)
        self.accept()
    
    def run_command(self):
        cmd = self.cmd_entry.text().strip()
        if cmd:
            InjectionEngine.inject_shell(self.secrets, command=cmd, working_dir=self.selected_folder)
            self.accept()
