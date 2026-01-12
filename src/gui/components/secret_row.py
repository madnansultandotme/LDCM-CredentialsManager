"""
Secret row component for secrets table
"""
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QStyle
from PyQt6.QtCore import Qt, QSize
from src.gui.styles import button_style


class SecretRow(QFrame):
    def __init__(self, colors, secret, vault, on_delete, on_edit):
        super().__init__()
        self.colors = colors
        self.secret = secret
        self.vault = vault
        self.on_edit = on_edit
        self.revealed = False
        
        self.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 8, 15, 8)
        
        # Key
        key_label = QLabel(secret.key)
        key_label.setFixedWidth(200)
        key_label.setStyleSheet(f"color: {colors['text_primary']}; background: transparent; border: none;")
        layout.addWidget(key_label)
        
        # Value
        self.value_label = QLabel("••••••••")
        self.value_label.setFixedWidth(300)
        self.value_label.setStyleSheet(f"color: {colors['text_secondary']}; background: transparent; border: none;")
        layout.addWidget(self.value_label)
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(5)
        
        # Reveal button
        reveal_btn = self.create_action_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView),
            colors['secondary']
        )
        reveal_btn.clicked.connect(self.toggle_reveal)
        actions_layout.addWidget(reveal_btn)
        
        # Edit button
        edit_btn = self.create_action_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView),
            colors['accent_cyan']
        )
        edit_btn.clicked.connect(self.edit_secret)
        actions_layout.addWidget(edit_btn)
        
        # Copy button
        copy_btn = self.create_action_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
            colors['secondary']
        )
        copy_btn.clicked.connect(self.copy_secret)
        actions_layout.addWidget(copy_btn)
        
        # Delete button
        delete_btn = self.create_action_button(
            self.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon),
            colors['accent_red']
        )
        delete_btn.clicked.connect(lambda: on_delete(secret.id))
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)
        layout.addStretch()
    
    def create_action_button(self, icon, hover_color):
        btn = QPushButton()
        btn.setIcon(icon)
        btn.setIconSize(QSize(16, 16))
        btn.setFixedSize(32, 32)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 4px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:focus {{
                outline: none;
            }}
        """)
        return btn
    
    def toggle_reveal(self):
        if self.revealed:
            self.value_label.setText("••••••••")
            self.revealed = False
        else:
            decrypted = self.vault.decrypt_secret(self.secret.encrypted_value)
            self.value_label.setText(decrypted)
            self.revealed = True
    
    def edit_secret(self):
        self.on_edit(self.secret)
    
    def copy_secret(self):
        import pyperclip
        decrypted = self.vault.decrypt_secret(self.secret.encrypted_value)
        pyperclip.copy(decrypted)
