from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Shopping cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart_quantity'),

    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),

    # Admin pages
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/products/', views.admin_products, name='admin_products'),
    path('admin-panel/products/add/', views.add_product, name='add_product'),
    path('admin-panel/products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('admin-panel/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('admin-panel/orders/', views.admin_orders, name='admin_orders'),
    path('admin-panel/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admin-panel/categories/', views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/add/', views.add_category, name='add_category'),
    path('admin-panel/categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('admin-panel/categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('admin-panel/messages/', views.admin_messages, name='admin_messages'),
    path('admin-panel/messages/<int:message_id>/reply/', views.reply_message, name='reply_message'),

    # Customer dashboard
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.update_profile, name='update_profile'),
    path('my-messages/', views.customer_messages, name='customer_messages'),
    path('my-messages/<int:message_id>/', views.customer_message_detail, name='customer_message_detail'),
    path('api/chat-messages/<int:message_id>/', views.get_chat_messages, name='get_chat_messages'),

    # Wishlist
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Dynamic pages
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
]
