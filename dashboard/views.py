from django.shortcuts import render, redirect
from core.store_data import USERS, ORDERS, PRODUCTS, cart_count


def dashboard_page(request):
    user = request.session.get('user')
    if not user:
        return redirect('login')   # must be logged in

    # Filter orders belonging to this user
    user_orders = [o for o in ORDERS if o['user_email'] == user['email']]

    cart = request.session.get('cart', {})

    context = {
        'user': user,
        'orders': user_orders,
        'cart_count': cart_count(cart),
        # Admin stats
        'total_products': len(PRODUCTS),
        'total_users':    len(USERS),
        'total_orders':   len(ORDERS),
    }
    return render(request, 'dashboard.html', context)


def logout_page(request):
    """Clear the session and redirect to home."""
    request.session.flush()
    return redirect('home')
