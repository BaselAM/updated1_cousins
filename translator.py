# translator.py

TRANSLATIONS = {
    'products_table': {
        'en': "Parts Table",
        'he': "טבלת חלקים"
    },
    'usd': {'en': "USD", 'he': "דולר אמריקאי"},
    'eur': {'en': "EUR", 'he': "יורו"},
    'gbp': {'en': "GBP", 'he': "לירה שטרלינג"},
    'ils': {'en': "ILS", 'he': "שקל ישראלי"},

    # Update products button text
    'products_button': {
        'en': "Products Table",  # Updated from "Products"
        'he': "טבלת חלקים"  # Changed from "חלקים"
    },'products_table': {
        'en': "Products Table",
        'he': "טבלת חלקים"
    },
'graph_placeholder': {
        'en': "Graph will be displayed here",
        'he': "גרף יוצג כאן"
    },
    'stats_info': {
        'en': "Additional statistics information can be shown here.",
        'he': "ניתן להציג כאן מידע סטטיסטי נוסף."
    },
    'refresh_statistics': {
        'en': "Refresh Statistics",
        'he': "רענן סטטיסטיקות"
    },
'invalid_number': {
        'en': "Please enter a valid number",
        'he': "אנא הזן מספר תקין"
    },
    'success': {
        'en': "Success",
        'he': "הצלחה"
    },
    'settings_saved': {
        'en': "Settings saved successfully",
        'he': "ההגדרות נשמרו בהצלחה"
    },
'copyright': {'en': "Copyright © 2025 Abu Mukh Car Parts", 'he': "זכויות יוצרים © 2025 אבו מוך חלפי רכב"},
'language_change_error': {
        'en': "Failed to change language",
        'he': "שגיאה בשינוי שפה"
    },
    'operation_failed': {
        'en': "Operation failed",
        'he': "הפעולה נכשלה"
    },
    'window_title': {'en': "Car Parts Management", 'he': "ניהול חלקי רכב"},
    'save': {'en': "Save", 'he': "שמור"},
    'cancel': {'en': "Cancel", 'he': "בטל"},
    'language_settings': {'en': "Language Settings", 'he': "הגדרות שפה"},
    'interface_language': {'en': "Interface Language", 'he': "שפת ממשק"},
    'english': {'en': "English", 'he': "אנגלית"},
    'hebrew': {'en': "Hebrew", 'he': "עברית"},
    'appearance': {'en': "Appearance", 'he': "מראה"},
    'color_theme': {'en': "Color Theme", 'he': "ערכת צבעים"},
    'dark_theme': {'en': "Dark Theme", 'he': "ערכת נושא כהה"},
    'light_theme': {'en': "Light Theme", 'he': "ערכת נושא בהיר"},
    'system_default': {'en': "System Default", 'he': "ברירת מערכת"},
    'primary_color': {'en': "Primary Color", 'he': "צבע ראשי"},
    'secondary_color': {'en': "Secondary Color", 'he': "צבע משני"},
    'technical_settings': {'en': "Technical Settings", 'he': "הגדרות טכניות"},
    'auto_backup': {'en': "Auto Backup", 'he': "גיבוי אוטומטי"},
    'daily': {'en': "Daily", 'he': "יומי"},
    'weekly': {'en': "Weekly", 'he': "שבועי"},
    'monthly': {'en': "Monthly", 'he': "חודשי"},
    'measurement_units': {'en': "Measurement Units", 'he': "יחידות מדידה"},
    'metric_system': {'en': "Metric", 'he': "מערכת מטרית"},
    'imperial_system': {'en': "Imperial", 'he': "מערכת אימפריאלית"},
    'select_invoice_template': {'en': "Select Invoice Template", 'he': "בחר תבנית חשבונית"},
    'inventory_settings': {'en': "Inventory Settings", 'he': "הגדרות מלאי"},
    'low_stock_threshold': {'en': "Low Stock Threshold", 'he': "סף מלאי נמוך"},
    'default_currency': {'en': "Default Currency", 'he': "מטבע ברירת מחדל"},
    'enable_auto_restock': {'en': "Enable Auto Restock", 'he': "הפעל חידוש אוטומטי"},
    'products_button': {'en': "Products", 'he': "חלקים"},
    'products_list_button': {'en': "Products List", 'he': "רשימת חלקים"},
    'statistics_button': {'en': "Statistics", 'he': "סטטיסטיקה"},
    'settings_button': {'en': "Settings", 'he': "הגדרות"},
    'help_button': {'en': "Help", 'he': "עזרה"},
    'exit_button': {'en': "Exit", 'he': "יציאה"},
    'search_placeholder': {'en': "Search...", 'he': "חפש..."},
    'error': {'en': "Error", 'he': "שגיאה"},
    'settings_save_error': {'en': "Failed to save settings", 'he': "שמירת ההגדרות נכשלה"},
    'add_product': {'en': "Add Product", 'he': "הוסף חלק"},
    'select_button': {'en': "Select", 'he': "בחר"},
    'remove': {'en': "Remove", 'he': "מחק"},
    'filter_button': {'en': "Filter", 'he': "סינון"},
    'id': {'en': "ID", 'he': "מזהה"},
    'category': {'en': "Category", 'he': "קטגוריה"},
    'car': {'en': "Car", 'he': "רכב"},
    'model': {'en': "Model", 'he': "דגם"},
    'product_name': {'en': "Product Name", 'he': "שם חלק"},
    'quantity': {'en': "Quantity", 'he': "כמות"},
    'price': {'en': "Price", 'he': "מחיר"},
    'overwrite_title': {'en': "Overwrite Product", 'he': "דרוש אישור לעדכון חלק"},
    'overwrite_message': {'en': "A product with this name exists. Overwrite?", 'he': "קיים מוצר עם שם זה. לעדכן?"},
    'save_error': {'en': "Save error", 'he': "שגיאה בשמירה"},
    'required_field': {'en': "This field is required", 'he': "שדה חובה"},

    # Add the missing keys here:
    'Abu Mukh Car Parts': {'en': "Abu Mukh Car Parts", 'he': "אבו מוך חלפי רכב"},
    'footer_content': {'en': "All rights reserved.", 'he': "כל הזכויות שמורות."},
    'help_documentation': {'en': "Help Documentation", 'he': "תיעוד עזרה"},
    'help_description': {'en': "Find all documentation about the app here.", 'he': "מצא כאן את כל התיעוד על האפליקציה."},
    'contact_support': {'en': "Contact Support", 'he': "צור קשר עם תמיכה"},
    'quick_steps': {'en': "Quick Steps", 'he': "שלבים מהירים"},
    'email_us': {'en': "Email Us", 'he': "שלחו לנו אימייל"},
    'user_guide': {'en': "User Guide", 'he': "מדריך למשתמש"},
    'help_footer_note': {'en': "This is the footer note for help section.", 'he': "זו הערת תחתית עבור החלק של עזרה."},
    'header_title': {'en': "Welcome to Abu Mukh Car Parts", 'he': "ברוכים הבאים לאבו מוך חלפי רכב"}
}


class Translator:
    def __init__(self, language='en'):
        self.language = language

    def t(self, key):
        translation = TRANSLATIONS.get(key, {}).get(self.language)
        if translation is None:
            print(
                f"Warning: Missing translation for key '{key}' in language '{self.language}'")
            return key
        return translation

    def set_language(self, language):
        self.language = language


if __name__ == '__main__':
    print("Translation for 'window_title':", Translator().t('window_title'))
