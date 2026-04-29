"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from home      import views as home_views
from login     import views as login_views
from signup    import views as signup_views
from dashboard import views as dashboard_views
from menu      import views as menu_views
from orders    import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Main pages ─────────────────────────────────────
    path('',           home_views.home_page,       name='home'),
    path('products/',  menu_views.products_page,   name='products'),

    # ── Auth ───────────────────────────────────────────
    path('login/',     login_views.login_page,     name='login'),
    path('signup/',    signup_views.signup_page,   name='signup'),
    path('logout/',    dashboard_views.logout_page, name='logout'),
    path('dashboard/', dashboard_views.dashboard_page, name='dashboard'),

    # ── Cart ───────────────────────────────────────────
    path('cart/',                          order_views.cart_page,       name='cart'),
    path('cart/add/<int:product_id>/',     order_views.add_to_cart,     name='add_to_cart'),
    path('cart/remove/<int:product_id>/',  order_views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/',  order_views.update_cart,     name='update_cart'),

    # ── Checkout & Orders ──────────────────────────────
    path('checkout/',      order_views.checkout_page,  name='checkout'),
    path('order/success/', order_views.order_success,  name='order_success'),
]

