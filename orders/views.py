import datetime
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from core.store_data import ORDERS, get_product, get_cart_items, cart_count


# ── ADD TO CART ──────────────────────────────────────────────
def add_to_cart(request, product_id):
    """Add one unit of a product to the session cart."""
    cart = request.session.get('cart', {})
    key  = str(product_id)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    # Go back to the page user was on (product list, home, etc.)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ── REMOVE FROM CART ─────────────────────────────────────────
def remove_from_cart(request, product_id):
    """Remove a product entirely from the session cart."""
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


# ── UPDATE QUANTITY ──────────────────────────────────────────
@require_POST
def update_cart(request, product_id):
    """Update the quantity of a product in the cart."""
    cart = request.session.get('cart', {})
    key  = str(product_id)
    qty  = int(request.POST.get('qty', 1))
    if qty <= 0:
        cart.pop(key, None)
    else:
        cart[key] = qty
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


# ── CART PAGE ────────────────────────────────────────────────
def cart_page(request):
    """Show all items currently in the cart."""
    cart  = request.session.get('cart', {})
    items, total = get_cart_items(cart)
    return render(request, 'cart.html', {
        'cart_items': items,
        'total': total,
        'cart_count': cart_count(cart),
        'user': request.session.get('user'),
    })


# ── CHECKOUT ─────────────────────────────────────────────────
def checkout_page(request):
    """Show checkout form (GET) or place the order (POST)."""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')   # nothing to checkout

    items, total = get_cart_items(cart)
    user = request.session.get('user')

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        phone   = request.POST.get('phone', '').strip()

        if not name or not address or not phone:
            return render(request, 'checkout.html', {
                'cart_items': items, 'total': total,
                'cart_count': cart_count(cart), 'user': user,
                'error': 'Please fill in all delivery details.',
            })

        # Save order to in-memory ORDERS list
        order = {
            'order_id':   len(ORDERS) + 1,
            'user_email': user['email'] if user else 'guest',
            'user_name':  name,
            'address':    address,
            'phone':      phone,
            'items':      items,
            'total':      total,
            'date':       datetime.datetime.now().strftime('%d %b %Y, %I:%M %p'),
            'status':     'Confirmed ✅',
        }
        ORDERS.append(order)

        # Clear the cart after placing order
        request.session['cart'] = {}
        request.session['last_order_id'] = order['order_id']
        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart_items': items,
        'total': total,
        'cart_count': cart_count(cart),
        'user': user,
    })


# ── ORDER SUCCESS ─────────────────────────────────────────────
def order_success(request):
    """Thank-you page shown after a successful order."""
    order_id = request.session.get('last_order_id')
    # Find the order from ORDERS list
    order = next((o for o in ORDERS if o['order_id'] == order_id), None)
    return render(request, 'order_success.html', {
        'order': order,
        'cart_count': 0,
        'user': request.session.get('user'),
    })
