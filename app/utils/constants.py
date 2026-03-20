"""
    App configurations and constants
"""

# #########################   APP INFO   ###########################
APP_NAME = ""
APP_VERSION = ""
APP_WIDTH = 1200
APP_HEIGHT = 900
MIN_WIDTH = 900
MIN_HEIGHT = 500

#  ######################## APP THEME    ###########################

DEFAULT_THEME = ""
DEFAULT_COLOR = ""


#  ######################## SIDEBAR MENU ITEMS   ########################

SIDEBAR_MENU = [
    {"label": "Dashboard",         "icon": "🏠", "screen": "dashboard"},
    {"label": "POS / Sales",       "icon": "🧾", "screen": "pos"},
    {"label": "Inventory",         "icon": "📦", "screen": "inventory"},
    {"label": "Tailoring Orders",  "icon": "✂️",  "screen": "tailoring"},
    {"label": "Customers",         "icon": "👥", "screen": "customers"},
    {"label": "Measurements",      "icon": "📐", "screen": "measurements"},
    {"label": "Suppliers",         "icon": "🏭", "screen": "suppliers"},
    {"label": "Purchases",         "icon": "🛒", "screen": "purchases"},
    {"label": "Reports",           "icon": "📊", "screen": "reports"},
    {"label": "Notifications",     "icon": "🔔", "screen": "notifications"},
    {"label": "Settings",          "icon": "⚙️",  "screen": "settings"},
]