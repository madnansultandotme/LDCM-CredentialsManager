"""
Sidebar component for projects list
"""
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.gui.styles import button_style, frame_style
from src.gui.components.project_item import ProjectItem


class Sidebar(QFrame):
    def __init__(self, colors, on_add_project, on_select_project):
        super().__init__()
        self.colors = colors
        self.on_select_project = on_select_project
        
        self.setFixedWidth(280)
        self.setStyleSheet(frame_style(colors['bg_card'], radius=10))
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QFrame()
        header.setStyleSheet(frame_style(colors['secondary'], radius=8))
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 10, 15, 10)
        
        title = QLabel("Projects")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent; border: none;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        add_btn = QPushButton("+")
        add_btn.setFixedSize(30, 30)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(button_style(
            colors['accent_cyan'],
            colors['primary']
        ) + "font-size: 18px; font-weight: bold;")
        add_btn.clicked.connect(on_add_project)
        header_layout.addWidget(add_btn)
        
        layout.addWidget(header)
        
        # Projects container
        self.projects_container = QWidget()
        self.projects_container.setStyleSheet(f"background-color: {colors['bg_card']}; border: none;")
        self.projects_layout = QVBoxLayout(self.projects_container)
        self.projects_layout.setContentsMargins(10, 10, 10, 10)
        self.projects_layout.setSpacing(5)
        self.projects_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(self.projects_container, 1)
    
    def load_projects(self, projects):
        """Load projects into the sidebar"""
        # Clear existing
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add project items
        for project in projects:
            item = ProjectItem(self.colors, project, self.on_select_project)
            self.projects_layout.addWidget(item)
