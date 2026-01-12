"""
Main dashboard screen
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from src.gui.styles import button_style, frame_style
from src.gui.components.header import Header
from src.gui.components.sidebar import Sidebar
from src.gui.components.secret_row import SecretRow
from src.gui.components.dialogs import AddProjectDialog, AddSecretDialog, EditSecretDialog, InjectDialog
from src.injector import InjectionEngine
import pyperclip


class DashboardScreen(QWidget):
    def __init__(self, app, vault, on_lock_callback):
        super().__init__()
        self.app = app
        self.vault = vault
        self.on_lock = on_lock_callback
        self.colors = app.colors
        self.selected_project = None
        self.selected_env = None
        self.env_buttons = {}
        
        self.setup_ui()
        self.load_projects()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = Header(
            self.colors,
            "🔐 LDCM Dashboard",
            self.app.toggle_theme,
            self.on_lock,
            self.app.current_theme
        )
        layout.addWidget(header)
        
        # Main content
        content = QWidget()
        content.setStyleSheet(f"background-color: {self.colors['bg_main']}; border: none;")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        
        # Sidebar
        self.sidebar = Sidebar(self.colors, self.add_project_dialog, self.select_project)
        content_layout.addWidget(self.sidebar)
        
        # Main area
        self.main_area = QFrame()
        self.main_area.setStyleSheet(frame_style(self.colors['bg_card'], radius=10))
        self.main_layout = QVBoxLayout(self.main_area)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        content_layout.addWidget(self.main_area, 1)
        layout.addWidget(content, 1)
        
        self.show_welcome()
    
    def load_projects(self):
        """Load projects into sidebar"""
        projects = self.vault.get_projects()
        self.sidebar.load_projects(projects)
    
    def show_welcome(self):
        """Show welcome message"""
        self.clear_layout(self.main_layout)
        
        welcome = QLabel("Select a project to manage secrets")
        welcome.setFont(QFont("Segoe UI", 16))
        welcome.setStyleSheet(f"color: {self.colors['text_secondary']}; background: transparent; border: none;")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addStretch()
        self.main_layout.addWidget(welcome)
        self.main_layout.addStretch()
    
    def clear_layout(self, layout):
        """Clear all widgets from layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def select_project(self, project):
        """Handle project selection"""
        self.selected_project = project
        self.show_project_view()
    
    def show_project_view(self):
        """Show project details view"""
        self.clear_layout(self.main_layout)
        
        # Project header
        header_layout = QHBoxLayout()
        
        title = QLabel(self.selected_project.name)
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {self.colors['text_primary']}; background: transparent; border: none;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        delete_btn = QPushButton("Delete")
        delete_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(100, 36)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet(button_style(self.colors['accent_red'], "#C0392B"))
        delete_btn.clicked.connect(self.delete_project)
        header_layout.addWidget(delete_btn)
        
        self.main_layout.addLayout(header_layout)
        
        # Environment tabs
        self.setup_environment_tabs()
    
    def setup_environment_tabs(self):
        """Setup environment tab buttons"""
        env_layout = QHBoxLayout()
        env_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        envs = self.vault.get_environments(self.selected_project.id)
        self.env_buttons = {}
        
        for env in envs:
            btn = QPushButton(env.name.upper())
            btn.setFixedSize(100, 36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(button_style(
                self.colors['secondary'],
                self.colors['primary']
            ) + "font-weight: bold;")
            btn.clicked.connect(lambda checked, e=env: self.select_environment(e))
            env_layout.addWidget(btn)
            self.env_buttons[env.id] = btn
        
        self.main_layout.addLayout(env_layout)
        
        if envs:
            self.select_environment(envs[0])
    
    def select_environment(self, env):
        """Handle environment selection"""
        self.selected_env = env
        
        # Update button styles
        for env_id, btn in self.env_buttons.items():
            if env_id == env.id:
                btn.setStyleSheet(button_style(
                    self.colors['accent_cyan'],
                    self.colors['accent_cyan']
                ) + "font-weight: bold;")
            else:
                btn.setStyleSheet(button_style(
                    self.colors['secondary'],
                    self.colors['primary']
                ) + "font-weight: bold;")
        
        self.show_secrets_view()
    
    def show_secrets_view(self):
        """Show secrets table for selected environment"""
        # Remove old secrets widget and action bars
        for i in range(self.main_layout.count() - 1, -1, -1):
            item = self.main_layout.itemAt(i)
            if item.widget() and hasattr(item.widget(), '_is_secrets'):
                item.widget().deleteLater()
            elif item.layout() and hasattr(item.layout(), '_is_actions'):
                # Remove action bar layout
                layout = item.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                self.main_layout.removeItem(layout)
        
        # Actions bar
        self.setup_actions_bar()
        
        # Secrets table
        self.setup_secrets_table()

    def setup_actions_bar(self):
        """Setup action buttons bar"""
        actions = QHBoxLayout()
        actions._is_actions = True
        actions.setAlignment(Qt.AlignmentFlag.AlignLeft)
        actions.setSpacing(10)
        
        # Add Secret button
        add_btn = QPushButton("Add Secret")
        add_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder))
        add_btn.setIconSize(QSize(16, 16))
        add_btn.setFixedHeight(36)
        add_btn.setMinimumWidth(120)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(button_style(
            self.colors['accent_green'],
            "#1E8449"
        ) + "padding: 0 20px; font-weight: bold;")
        add_btn.clicked.connect(self.add_secret_dialog)
        actions.addWidget(add_btn)
        
        # Inject button
        inject_btn = QPushButton("Inject & Run")
        inject_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        inject_btn.setIconSize(QSize(16, 16))
        inject_btn.setFixedHeight(36)
        inject_btn.setMinimumWidth(130)
        inject_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        inject_btn.setStyleSheet(button_style(
            self.colors['accent_cyan'],
            self.colors['primary']
        ) + "padding: 0 20px; font-weight: bold;")
        inject_btn.clicked.connect(self.inject_dialog)
        actions.addWidget(inject_btn)
        
        # Copy ENV button
        copy_btn = QPushButton("Copy as ENV")
        copy_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        copy_btn.setIconSize(QSize(16, 16))
        copy_btn.setFixedHeight(36)
        copy_btn.setMinimumWidth(140)
        copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        copy_btn.setStyleSheet(button_style(
            self.colors['secondary'],
            self.colors['primary']
        ) + "padding: 0 20px;")
        copy_btn.clicked.connect(self.copy_as_env)
        actions.addWidget(copy_btn)
        
        self.main_layout.addLayout(actions)
    
    def setup_secrets_table(self):
        """Setup secrets table"""
        table = QFrame()
        table._is_secrets = True
        table.setStyleSheet(f"""
            QFrame {{
                background-color: {self.colors['bg_card']};
                border: 1px solid {self.colors['secondary']};
                border-radius: 8px;
            }}
        """)
        table_layout = QVBoxLayout(table)
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)
        
        # Table header
        header = QFrame()
        header.setStyleSheet(f"background-color: {self.colors['primary']}; border: none; border-radius: 0;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        for text, width in [("KEY", 200), ("VALUE", 300), ("ACTIONS", 150)]:
            lbl = QLabel(text)
            lbl.setFixedWidth(width)
            lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            lbl.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
            header_layout.addWidget(lbl)
        header_layout.addStretch()
        
        table_layout.addWidget(header)
        
        # Secrets rows
        secrets = self.vault.get_secrets(self.selected_env.id)
        if not secrets:
            empty = QLabel("No secrets yet. Click '+ Add Secret' to create one.")
            empty.setStyleSheet(f"color: {self.colors['text_secondary']}; padding: 20px; background: transparent; border: none;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            table_layout.addWidget(empty)
        else:
            for secret in secrets:
                row = SecretRow(self.colors, secret, self.vault, self.delete_secret, self.edit_secret)
                table_layout.addWidget(row)
        
        table_layout.addStretch()
        self.main_layout.addWidget(table, 1)

    # Dialog methods
    def add_project_dialog(self):
        """Show add project dialog"""
        dialog = AddProjectDialog(self, self.colors)
        if dialog.exec():
            name = dialog.get_result()
            if name:
                self.vault.create_project(name)
                self.load_projects()
    
    def delete_project(self):
        """Delete current project"""
        if self.selected_project:
            self.vault.delete_project(self.selected_project.id)
            self.selected_project = None
            self.load_projects()
            self.show_welcome()
    
    def add_secret_dialog(self):
        """Show add secret dialog"""
        dialog = AddSecretDialog(self, self.colors)
        if dialog.exec():
            key, value = dialog.get_result()
            if key and value:
                self.vault.add_secret(self.selected_env.id, key, value)
                self.show_project_view()
    
    def delete_secret(self, secret_id):
        """Delete a secret"""
        self.vault.delete_secret(secret_id)
        self.show_project_view()
    
    def edit_secret(self, secret):
        """Show edit secret dialog"""
        decrypted_value = self.vault.decrypt_secret(secret.encrypted_value)
        dialog = EditSecretDialog(self, self.colors, secret, decrypted_value)
        if dialog.exec():
            key, value = dialog.get_result()
            if key and value:
                self.vault.update_secret(secret.id, key, value)
                self.show_project_view()
    
    def get_decrypted_secrets(self):
        """Get all secrets decrypted"""
        secrets = self.vault.get_secrets(self.selected_env.id)
        return {s.key: self.vault.decrypt_secret(s.encrypted_value) for s in secrets}
    
    def copy_as_env(self):
        """Copy secrets as ENV format"""
        secrets = self.get_decrypted_secrets()
        env_str = InjectionEngine.generate_shell_export(secrets)
        pyperclip.copy(env_str)
    
    def inject_dialog(self):
        """Show inject dialog"""
        dialog = InjectDialog(self, self.colors, self.get_decrypted_secrets())
        dialog.exec()
