from django.shortcuts import render, redirect
from core.store_data import USERS, cart_count


def signup_page(request):
    error = ''
    if request.method == 'POST':
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm  = request.POST.get('confirm', '')
        role     = request.POST.get('role', 'Customer')

        # Validate inputs
        if not name or not email or not password:
            error = 'All fields are required.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif email in USERS:
            error = 'Email already registered. Please login instead.'
        else:
            # Save user to in-memory USERS dict
            USERS[email] = {'name': name, 'password': password, 'role': role}
            # Automatically log them in
            request.session['user'] = {'email': email, 'name': name, 'role': role}
            return redirect('dashboard')

    cart = request.session.get('cart', {})
    return render(request, 'login_signup.html', {
        'error': error,
        'show': 'signup',
        'cart_count': cart_count(cart),
    })
