from django.shortcuts import render
from core.store_data import CATEGORIES, search_products, cart_count


def home_page(request):
    """
    Home page:
    - Shows all products (filtered by search/category if provided)
    - Passes cart count and logged-in user to the template
    """
    q        = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All')

    products = search_products(query=q, category=category)

    # Cart lives in the session (persists across requests)
    cart = request.session.get('cart', {})

    context = {
        'products': products,
        'categories': CATEGORIES,
        'search_query': q,
        'selected_category': category,
        'cart_count': cart_count(cart),
        'user': request.session.get('user'),        # None if not logged in
    }
    return render(request, 'index.html', context)
