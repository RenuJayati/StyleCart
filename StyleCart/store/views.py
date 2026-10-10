from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect
from .models import Product, Order, ContactMessage


def home(request):
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()

    products = Product.objects.all().order_by(
        Case(
            When(category__iexact='Women', then=Value(1)),
            When(category__iexact='Men', then=Value(2)),
            When(category__iexact='Footwear', then=Value(3)),
            When(category__iexact='Bags', then=Value(4)),
            When(category__iexact='Beauty', then=Value(5)),
            When(category__iexact='Watches', then=Value(6)),
            default=Value(7),
            output_field=IntegerField(),
        ),
        'created_at'
    )

    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    if category:
        products = products.filter(
            category__iexact=category
        )

    categories = Product.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(
        request,
        'store/home.html',
        {
            'products': products,
            'search_query': search_query,
            'categories': categories,
            'selected_category': category,
        }
    )


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(
        request,
        'store/cart.html',
        {
            'products': products,
            'total': total,
        }
    )


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def checkout(request):
    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    products = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total += item_total

        products.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')

        order = Order.objects.create(
            customer_name=customer_name,
            mobile=mobile,
            address=address,
            city=city,
            total_amount=total
        )

        request.session['cart'] = {}

        return redirect('order_success', order_id=order.id)

    return render(
        request,
        'store/checkout.html',
        {
            'products': products,
            'total': total,
        }
    )


def order_success(request, order_id):
    order = Order.objects.get(id=order_id)

    return render(
        request,
        'store/order_success.html',
        {'order': order}
    )

def increase_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        return redirect('contact')

    return render(request, 'store/contact.html')

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)

    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )