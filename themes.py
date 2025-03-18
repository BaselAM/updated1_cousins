from PyQt5.QtGui import QColor

THEMES = {
    "classic": {
        # Sophisticated blue theme with depth and elegance
        "primary": "#1A365D",  # Rich navy primary
        "secondary": "#2A4365",  # Slightly lighter navy secondary
        "background": "#0F2942",  # Deep blue background
        "text": "#E2E8F0",  # Soft white text with slight blue tint
        "button": "#3182CE",  # Vibrant blue button
        "button_hover": "#4299E1",  # Lighter vibrant blue on hover
        "button_pressed": "#2B6CB0",  # Deeper blue when pressed
        "border": "#2C5282",  # Refined border color
        "input_bg": "#1E3A5F",  # Slightly elevated input fields
        "header": "#0F2942",  # Match with background
        "footer": "#0F2942",  # Match with background
        "sidebar_bg": "#0F2942",  # Match with background
        "sidebar_button": "#1E3A5F",  # Slightly raised button
        "stats_card": "#2A4D6A",  # Rich blue for cards with slight green tint
        "warning": "#ECC94B",  # Gold warning
        "success": "#38B2AC",  # Teal success
        "error": "#E53E3E",  # Clean red error
        "card_bg": "#1E3A5F",  # Card background
        "shadow": "#00000066",  # Subtle shadow
        "highlight": "#4299E1",  # Selection highlight
        "divider": "#2C5282",  # Subtle divider
        "accent": "#805AD5",  # Purple accent for special elements
        "overlay": "#0F2942DD",  # Semi-transparent overlay
        "title": "#E2E8F0"  # Title text color matching text color
    },

    "dark": {
        # Refined dark theme with subtle depth
        "primary": "#121212",  # Near black primary with hint of warmth
        "secondary": "#1E1E1E",  # Dark gray secondary with warmth
        "background": "#000000",  # Pure black background
        "text": "#F7FAFC",  # Crisp white text
        "button": "#2D3748",  # Deep slate button
        "button_hover": "#4A5568",  # Medium slate hover
        "button_pressed": "#1A202C",  # Very deep slate when pressed
        "border": "#2D3748",  # Matching border with buttons
        "input_bg": "#1E1E1E",  # Slightly elevated input fields
        "header": "#000000",  # Match with background
        "footer": "#000000",  # Match with background
        "sidebar_bg": "#121212",  # Slightly lighter than background
        "sidebar_button": "#1E1E1E",  # Raised button
        "stats_card": "#1A202C",  # Card background
        "success": "#38A169",  # Forest green success
        "warning": "#DD6B20",  # Burnt orange warning
        "error": "#E53E3E",  # Clean red error
        "card_bg": "#1E1E1E",  # Card background
        "shadow": "#00000080",  # Pronounced shadow
        "highlight": "#5A67D8",  # Royal blue highlight
        "divider": "#2D3748",  # Subtle divider
        "accent": "#9F7AEA",  # Rich purple accent
        "overlay": "#000000E6",  # Near-opaque overlay
        "title": "#F7FAFC"  # Title text color matching text color
    },

    "light": {
        # Elevated modern light theme
        "primary": "#FFFFFF",  # Pure white primary
        "secondary": "#F7FAFC",  # Very light blue-gray secondary
        "background": "#EDF2F7",  # Light blue-gray background
        "text": "#1A202C",  # Deep gray-blue text for contrast
        "button": "#4299E1",  # Sky blue button
        "button_hover": "#63B3ED",  # Lighter sky blue hover
        "button_pressed": "#3182CE",  # Darker blue when pressed
        "border": "#CBD5E0",  # Soft gray border
        "input_bg": "#FFFFFF",  # White input background
        "header": "#FFFFFF",  # White header
        "footer": "#FFFFFF",  # White footer
        "sidebar_bg": "#FFFFFF",  # White sidebar
        "sidebar_button": "#F7FAFC",  # Very light sidebar buttons
        "stats_card": "#F7FAFC",  # Very light card
        "success": "#38A169",  # Forest green success
        "warning": "#DD6B20",  # Burnt orange warning
        "error": "#E53E3E",  # Clean red error
        "card_bg": "#FFFFFF",  # White card background
        "shadow": "#00000015",  # Very subtle shadow
        "highlight": "#90CDF4",  # Light blue highlight
        "divider": "#E2E8F0",  # Very light divider
        "accent": "#9F7AEA",  # Rich purple accent
        "overlay": "#EDF2F7E6",  # Light translucent overlay
        "title": "#1A202C"  # Title text color matching text color
    }
}

# Function implementations remain the same
from contextlib import contextmanager

_current_theme = "classic"


def set_theme(theme_name):
    global _current_theme
    _current_theme = theme_name if theme_name in THEMES else "classic"


@contextmanager
def temp_theme(theme_name):
    """Temporary theme context manager"""
    original = _current_theme
    set_theme(theme_name)
    try:
        yield
    finally:
        set_theme(original)


def get_color(color_key):
    return THEMES[_current_theme].get(color_key, QColor(0, 0, 0))