from django.shortcuts import render
from core.store_data import CATEGORIES, search_products, cart_count


def products_page(request):
    """All products page with category filter and search."""
    q        = request.GET.get('q', '').strip()
    category = request.GET.get('category', 'All')
    products = search_products(query=q, category=category)
    cart     = request.session.get('cart', {})
    return render(request, 'products.html', {
        'products': products,
        'categories': CATEGORIES,
        'selected_category': category,
        'search_query': q,
        'cart_count': cart_count(cart),
        'user': request.session.get('user'),
    })
