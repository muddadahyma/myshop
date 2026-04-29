# ============================================================
# In-Memory Data Store — replaces the database for now.
# All data lives in RAM and resets when the server restarts.
# In a real production app, this would be a database (MySQL/PostgreSQL).
# ============================================================

# ---------- PRODUCT CATALOG ----------
# Each product is a Python dict: { id, name, price, category, emoji, description, stock }
PRODUCTS = [
    {'id': 1,  'name': 'Wireless Headphones',  'price': 2999,  'category': 'Electronics', 'emoji': '🎧', 'description': 'Premium sound quality with active noise cancellation and 20hr battery.', 'stock': 50},
    {'id': 2,  'name': 'Laptop Stand',          'price': 1499,  'category': 'Electronics', 'emoji': '💻', 'description': 'Ergonomic aluminium laptop stand for better posture and cooling.', 'stock': 30},
    {'id': 3,  'name': 'Mechanical Keyboard',   'price': 4999,  'category': 'Electronics', 'emoji': '⌨️', 'description': 'Tactile mechanical keyboard with RGB backlight and USB-C.', 'stock': 15},
    {'id': 4,  'name': 'Smartwatch',            'price': 7999,  'category': 'Electronics', 'emoji': '⌚', 'description': 'Fitness tracking smartwatch with heart rate & sleep monitor.', 'stock': 20},
    {'id': 5,  'name': 'Bluetooth Speaker',     'price': 1999,  'category': 'Electronics', 'emoji': '🔊', 'description': 'Portable waterproof speaker with 12hr playtime.', 'stock': 40},
    {'id': 6,  'name': 'Running Shoes',         'price': 3499,  'category': 'Clothing',    'emoji': '👟', 'description': 'Lightweight running shoes for everyday training.', 'stock': 25},
    {'id': 7,  'name': 'Backpack',              'price': 1999,  'category': 'Clothing',    'emoji': '🎒', 'description': 'Water-resistant 30L backpack with laptop compartment.', 'stock': 35},
    {'id': 8,  'name': 'Hoodie',                'price': 1299,  'category': 'Clothing',    'emoji': '🧥', 'description': 'Soft fleece hoodie, available in multiple colours.', 'stock': 60},
    {'id': 9,  'name': 'Python Programming',    'price': 699,   'category': 'Books',       'emoji': '📗', 'description': 'Learn Python programming from scratch — beginner to advanced.', 'stock': 100},
    {'id': 10, 'name': 'Data Structures',       'price': 799,   'category': 'Books',       'emoji': '📘', 'description': 'Master data structures and algorithms with real examples.', 'stock': 60},
    {'id': 11, 'name': 'Django for Beginners',  'price': 899,   'category': 'Books',       'emoji': '📙', 'description': 'Build web apps with Django step by step.', 'stock': 45},
    {'id': 12, 'name': 'Yoga Mat',              'price': 999,   'category': 'Sports',      'emoji': '🧘', 'description': 'Non-slip eco-friendly yoga mat, 6mm thick.', 'stock': 40},
    {'id': 13, 'name': 'Water Bottle',          'price': 599,   'category': 'Sports',      'emoji': '🍶', 'description': 'Insulated stainless steel water bottle, 1 Litre.', 'stock': 90},
    {'id': 14, 'name': 'Dumbbells (5kg pair)', 'price': 1599,  'category': 'Sports',      'emoji': '🏋️', 'description': 'Rubber-coated dumbbell set, easy-grip handle.', 'stock': 30},
    {'id': 15, 'name': 'Desk Lamp',             'price': 1299,  'category': 'Home',        'emoji': '🪔', 'description': 'LED desk lamp with 3 brightness levels and USB charging port.', 'stock': 45},
    {'id': 16, 'name': 'Coffee Mug',            'price': 399,   'category': 'Home',        'emoji': '☕', 'description': 'Ceramic coffee mug that keeps drinks warm for hours.', 'stock': 80},
    {'id': 17, 'name': 'Wall Clock',            'price': 849,   'category': 'Home',        'emoji': '🕐', 'description': 'Minimalist silent wall clock with wooden frame.', 'stock': 55},
    {'id': 18, 'name': 'Scented Candle',        'price': 449,   'category': 'Home',        'emoji': '🕯️', 'description': 'Soy wax scented candle — lavender & vanilla blend.', 'stock': 70},
]

# ---------- CATEGORIES ----------
CATEGORIES = ['All', 'Electronics', 'Clothing', 'Books', 'Sports', 'Home']

# ---------- USER STORE ----------
# Structure: { email: { 'name': str, 'password': str, 'role': str } }
# Roles: 'Customer', 'Admin', 'Vendor'
USERS = {
    # Demo admin account (pre-loaded)
    'admin@myshop.com': {'name': 'Admin User', 'password': 'admin123', 'role': 'Admin'},
}

# ---------- ORDERS ----------
# Structure: [{ 'order_id', 'user_email', 'user_name', 'address', 'phone', 'items', 'total', 'date', 'status' }]
ORDERS = []


# ============================================================
# Helper Functions
# ============================================================

def get_product(product_id):
    """Return a product dict by its id, or None if not found."""
    for p in PRODUCTS:
        if p['id'] == product_id:
            return p
    return None


def search_products(query='', category='All'):
    """Filter products by search query and/or category."""
    results = PRODUCTS
    if category and category != 'All':
        results = [p for p in results if p['category'] == category]
    if query:
        q = query.lower()
        results = [p for p in results if q in p['name'].lower() or q in p['description'].lower()]
    return results


def get_cart_items(cart_dict):
    """
    Given cart dict { str(product_id): qty },
    return list of { ...product, qty, subtotal } and grand total.
    """
    items = []
    total = 0
    for pid, qty in cart_dict.items():
        product = get_product(int(pid))
        if product:
            subtotal = product['price'] * qty
            total += subtotal
            items.append({**product, 'qty': qty, 'subtotal': subtotal})
    return items, total


def cart_count(cart_dict):
    """Total number of items in the cart."""
    return sum(cart_dict.values())
