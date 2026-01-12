"""
Centralized styling for the application
"""

def get_global_styles(colors):
    """Global styles to remove outlines and set base styling"""
    return f"""
        * {{
            outline: none;
        }}
        QWidget {{
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QWidget:focus {{
            outline: none;
        }}
        QPushButton:focus {{
            outline: none;
            border: none;
        }}
        QLineEdit:focus {{
            outline: none;
        }}
        QScrollArea {{
            border: none;
        }}
        QScrollBar:vertical {{
            background: {colors['bg_card']};
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {colors['secondary']};
            border-radius: 4px;
            min-height: 20px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
    """


def button_style(bg_color, hover_color, text_color="#FFFFFF", radius=4):
    """Generate button stylesheet"""
    return f"""
        QPushButton {{
            background-color: {bg_color};
            color: {text_color};
            border: none;
            border-radius: {radius}px;
            outline: none;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:focus {{
            outline: none;
            border: none;
        }}
    """


def input_style(colors):
    """Generate input field stylesheet"""
    return f"""
        QLineEdit {{
            background-color: {colors['bg_main']};
            color: {colors['text_primary']};
            border: 2px solid {colors['secondary']};
            border-radius: 6px;
            padding: 0 15px;
            font-size: 14px;
            outline: none;
        }}
        QLineEdit:focus {{
            border-color: {colors['accent_cyan']};
            outline: none;
        }}
    """


def frame_style(bg_color, radius=0, border=None):
    """Generate frame stylesheet"""
    border_style = f"border: 1px solid {border};" if border else "border: none;"
    return f"""
        QFrame {{
            background-color: {bg_color};
            border-radius: {radius}px;
            {border_style}
            outline: none;
        }}
    """
