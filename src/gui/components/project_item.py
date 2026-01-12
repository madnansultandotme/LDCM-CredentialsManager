"""
Project item component for sidebar
"""
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from src.gui.styles import button_style


class ProjectItem(QPushButton):
    def __init__(self, colors, project, on_click):
        super().__init__(f"📁 {project.name}")
        self.colors = colors
        self.project = project
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_card']};
                color: {colors['text_primary']};
                border: none;
                border-radius: 6px;
                text-align: left;
                padding-left: 15px;
                font-size: 13px;
                outline: none;
            }}
            QPushButton:hover {{
                background-color: {colors['primary']};
                color: #FFFFFF;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        self.clicked.connect(lambda: on_click(project))
