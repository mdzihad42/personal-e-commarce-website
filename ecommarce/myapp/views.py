from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.utils import timezone
import datetime
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from functools import wraps
import json

# Custom decorators
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.userprofile.role != 'admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Public views
def home(request):
    products = Product.objects.filter(stock__gt=0).select_related('category')[:8]  # Featured products
    categories = Category.objects.all()[:6]  # Featured categories

    # Statistics for home page
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()

    context = {
        'products': products,
        'categories': categories,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
    }
    return render(request, 'home.html', context)

def shop(request):
    products = Product.objects.filter(stock__gt=0).select_related('category')
    categories = Category.objects.all()

    # Filtering
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', 'name')

    if category_id and category_id != 'None':
        products = products.filter(category_id=category_id)

    if search_query and search_query != 'None':
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Price Filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and min_price != 'None':
        products = products.filter(price__gte=min_price)
    if max_price and max_price != 'None':
        products = products.filter(price__lte=max_price)

    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')

    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request,'shop.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id).select_related('category')[:4]

    # Check if product is in user's wishlist
    in_wishlist = False
    wishlist_item_id = None
    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()
        if wishlist_item:
            in_wishlist = True
            wishlist_item_id = wishlist_item.id

    # Determine if product is a "new arrival" (within the last 7 days)
    is_new = False
    try:
        if getattr(product, 'created_at', None):
            is_new = product.created_at >= (timezone.now() - datetime.timedelta(days=7))
    except Exception:
        is_new = False

    context = {
        'product': product,
        'related_products': related_products,
        'in_wishlist': in_wishlist,
        'wishlist_item_id': wishlist_item_id,
        'is_new': is_new,
    }
    return render(request, 'product_detail.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            if request.user.is_authenticated:
                contact_message.user = request.user
            contact_message.save()
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('contact')
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})

# Authentication views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile is created automatically via signal, ensure role is set
            user.userprofile.role = 'customer'
            user.userprofile.save()
            login(request, user)
            messages.success(request, f'Welcome to E-Shop, {user.first_name or user.username}!')
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

# Customer views
@login_required
def customer_dashboard(request):
    if request.user.userprofile.role != 'customer':
        return redirect('home')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        'orders': orders,
        'wishlist_count': wishlist_count,
    }
    return render(request, 'customer/dashboard.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if form.is_valid():
            # Update User model fields
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Save UserProfile fields
            form.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('customer_dashboard')
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'customer/profile.html', {'form': form})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'order_history.html', {'page_obj': page_obj})

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.select_related('product__category').all()
        total = cart.get_total()
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    # Admins cannot purchase items
    if request.user.userprofile.role == 'admin':
        messages.error(request, 'Admins cannot place orders.')
        return redirect('admin_dashboard')

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('product_detail', product_id=product_id)

    # Get quantity from POST, default to 1
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not item_created:
        # If item exists, add the new quantity to existing
        if cart_item.quantity + quantity > product.stock:
            messages.error(request, 'Cannot add items. Stock limit reached.')
        else:
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Added {quantity} x {product.name} to cart.')
    else:
        # If newly created, we just need to verify stock one more time (though get_or_create defaults handles init)
        if quantity > product.stock:
             # This is a rare edge case if defaults was used but quantity > stock
             cart_item.quantity = product.stock # MAX out
             cart_item.save()
             messages.warning(request, f'Stock limit reached. Added {product.stock} only.')
        else:
             messages.success(request, f'Added {quantity} x {product.name} to cart.')

    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > cart_item.product.stock:
            messages.error(request, 'Quantity exceeds available stock.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully.')

    return redirect('view_cart')

@login_required
def checkout(request):
    # Admins cannot purchase items
    if request.user.userprofile.role == 'admin':
        messages.error(request, 'Admins cannot place orders.')
        return redirect('admin_dashboard')

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        if not cart_items:
            messages.error(request, 'Your cart is empty.')
            return redirect('view_cart')
        total = cart.get_total()
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('view_cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                payment_method=form.cleaned_data['payment_method'],
                shipping_address=form.cleaned_data['shipping_address'],
                phone=form.cleaned_data['phone'],
            )

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                # Update stock
                item.product.stock -= item.quantity
                item.product.save()

            # Clear cart
            cart_items.delete()

            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('order_history')
    else:
        form = CheckoutForm(initial={'payment_method': 'cod'})

    context = {
        'cart_items': cart_items,
        'total': total,
        'form': form,
    }
    return render(request, 'checkout.html', context)

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product__category')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, f'{product.name} added to wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')

    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_wishlist(request, item_id):
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Item removed from wishlist.')
    return redirect('view_wishlist')

# Admin views
@admin_required
def admin_dashboard(request):
    # Statistics
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_revenue = Order.objects.filter(status__in=['shipped', 'delivered']).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Recent orders
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin/dashboard.html', context)

@admin_required
def admin_products(request):
    products = Product.objects.select_related('category').all()
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/products.html', {'page_obj': page_obj})

@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm()

    return render(request, 'admin/add_product.html', {'form': form})

@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('admin_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'admin/edit_product.html', {'form': form, 'product': product})

@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('admin_products')

    return render(request, 'admin/delete_product.html', {'product': product})

@admin_required
def admin_categories(request):
    categories = Category.objects.all()

    # Additional statistics
    total_products = Product.objects.count()
    active_categories = categories.count()
    empty_categories = categories.filter(product__isnull=True).distinct().count()

    return render(request, 'admin/categories.html', {
        'categories': categories,
        'total_products': total_products,
        'active_categories': active_categories,
        'empty_categories': empty_categories
    })

@admin_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm()

    return render(request, 'admin/add_category.html', {'form': form})

@admin_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('admin_categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'admin/edit_category.html', {'form': form, 'category': category})

@admin_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('admin_categories')

    return render(request, 'admin/delete_category.html', {'category': category})

@admin_required
def admin_orders(request):
    orders = Order.objects.select_related('user').all()
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/orders.html', {'page_obj': page_obj})

@admin_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {new_status}.')

    return redirect('admin_orders')

@admin_required
def admin_users(request):
    users = User.objects.select_related('userprofile').order_by('-date_joined')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/users.html', {'page_obj': page_obj})

@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.is_superuser:
        messages.error(request, 'Cannot delete superuser.')
        return redirect('admin_users')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('admin_users')
        
    return render(request, 'admin/delete_user.html', {'user_to_delete': user})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})

@login_required
def order_detail(request, order_id):
    if request.user.userprofile.role == 'admin':
        order = get_object_or_404(Order, id=order_id)
    else:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'order_detail.html', {'order': order})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, 'page.html', {'page': page})

from django.core.mail import send_mail
from django.conf import settings

@admin_required
def admin_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    paginator = Paginator(messages_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/messages.html', {'page_obj': page_obj})

@admin_required
def reply_message(request, message_id):
    contact_message = get_object_or_404(ContactMessage, id=message_id)
    
    if request.method == 'POST':
        reply_content = request.POST.get('reply_content')
        if reply_content:
            try:
                # 1. Create Reply Object
                MessageReply.objects.create(
                    message=contact_message,
                    user=request.user,
                    content=reply_content,
                    is_admin=True
                )
                
                # 2. Update Main Message Status
                contact_message.is_replied = True
                contact_message.replied_at = timezone.now()
                contact_message.save()

                # 3. Send Email Notification (Optional - keeping existing logic)
                subject = f"Reply to your message: {contact_message.subject}"
                send_mail(
                    subject,
                    reply_content,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@luxshop.com',
                    [contact_message.email],
                    fail_silently=True,
                )
                
                messages.success(request, 'Reply sent successfully!')
                return redirect('reply_message', message_id=message_id)
            except Exception as e:
                messages.error(request, f'Failed to send reply: {str(e)}')
        else:
             messages.error(request, 'Reply content cannot be empty.')
             
    return render(request, 'admin/reply_message.html', {'message': contact_message})

@login_required
def customer_messages(request):
    messages_list = ContactMessage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'customer/messages.html', {'messages': messages_list})

@login_required
def customer_message_detail(request, message_id):
    contact_message = get_object_or_404(ContactMessage, id=message_id, user=request.user)
    
    if request.method == 'POST':
        reply_content = request.POST.get('content')
        if reply_content:
            MessageReply.objects.create(
                message=contact_message,
                user=request.user,
                content=reply_content,
                is_admin=False
            )
            # Update status to pending so admin knows there is a new reply
            contact_message.is_replied = False 
            contact_message.save()
            
            messages.success(request, 'Reply sent!')
            return redirect('customer_message_detail', message_id=message_id)
            
    return render(request, 'customer/message_detail.html', {'message': contact_message})

from django.http import JsonResponse

@login_required
def get_chat_messages(request, message_id):
    """
    API to fetch replies for a specific message thread.
    Used for real-time polling in chat UI.
    """
    # Allow access if user is admin OR if user owns the message
    if request.user.userprofile.role == 'admin':
        contact_message = get_object_or_404(ContactMessage, id=message_id)
    else:
        contact_message = get_object_or_404(ContactMessage, id=message_id, user=request.user)
    
    replies = contact_message.replies.all().order_by('created_at')
    
    data = []
    data = []
    for reply in replies:
        user_name = "Unknown"
        if reply.is_admin:
            user_name = "Support Team"
        elif reply.user:
             user_name = reply.user.first_name or reply.user.username
             
        data.append({
            'user': user_name,
            'content': reply.content,
            'is_admin': reply.is_admin,
            'created_at': reply.created_at.strftime("%M %d, %Y %I:%M %p")
        })
        
    return JsonResponse({'replies': data})
