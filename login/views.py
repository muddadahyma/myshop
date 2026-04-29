from django.shortcuts import render, redirect
from core.store_data import USERS, cart_count


def login_page(request):
    error = ''
    if request.method == 'POST':
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # Check against in-memory USERS dict
        if email in USERS and USERS[email]['password'] == password:
            request.session['user'] = {
                'email': email,
                'name':  USERS[email]['name'],
                'role':  USERS[email]['role'],
            }
            return redirect('dashboard')
        else:
            error = 'Invalid email or password. Please try again.'

    cart = request.session.get('cart', {})
    return render(request, 'login_signup.html', {
        'error': error,
        'show': 'login',
        'cart_count': cart_count(cart),
    })
