from django.contrib import messages
from django.shortcuts import render

from orders.forms import OrderForm
from .models import Product, OrderItem, Order
from .utils import calculate_order_summary  # Assume you have a utility function to calculate
from django.db.models import Sum
from django.shortcuts import render
from .forms import OrderForm
from .models import Product
from decimal import Decimal, ROUND_HALF_UP


def order_view(request):
    # Prepare the product and bundles information to be displayed with the form
    products = Product.objects.all().prefetch_related('bundles')
    products_with_bundles = []
    for product in products:
        bundles = product.bundles.all()
        product_info = {
            'name': product.name,
            'code': product.code,
            'bundles': bundles
        }
        products_with_bundles.append(product_info)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print('Inside form')
        if form.is_valid():
            order_data = form.cleaned_data['order_data']
            customer_name = form.cleaned_data['customer_name']
            customer_phone = form.cleaned_data['customer_phone']
            customer_address = form.cleaned_data['customer_address']
            customer_email = form.cleaned_data['customer_email']
            # calculate_order_summary should be a function that takes the order data,
            # parses it, and returns a summary of the order including line items and prices
            summary = calculate_order_summary(order_data)
            order = Order.objects.create(customer_name=customer_name, customer_email=customer_email,
                                         customer_phone=customer_phone, customer_address=customer_address)
            total_price = 0.0
            for item in summary:
                product = Product.objects.get(code=item['code'])
                total_price += item['total_price']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
            context = {
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'customer_address': customer_address,
                'summary': summary,  # This is the list of dictionaries returned from your summary function
                'total_price': total_price
            }
            return render(request, 'order_summary.html', context)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = OrderForm()  # instantiate a new, empty form

    return render(request, 'order_form.html', {
        'form': form,
        'products_with_bundles': products_with_bundles
    })


def order_history(request):
    # Order the orders by date in descending order
    orders = Order.objects.annotate(total_price=Sum('order_items__total_price')).order_by('-order_date')
    total_sales = orders.aggregate(total_sales=Sum('total_price'))['total_sales']
    total_sales = total_sales.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if total_sales else Decimal('0.00')
    context = {
        'orders': orders,
        'total_sales': total_sales,
    }

    return render(request, 'order_history.html', context)
