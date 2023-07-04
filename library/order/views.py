from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order

from .models import Order
from book.models import Book


@staff_member_required
def all_orders(request):
    orders = Order.get_all()
    context = {'orders': orders}
    return render(request, 'order/orders_admin.html', context)


@login_required(login_url='login/')
def my_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    context = {'orders': orders}
    return render(request, 'order/orders_user.html', context)


@login_required(login_url='login/')
def create_order(request):
    books = Book.objects.all()
    if request.method == 'POST':
        book_id = request.POST.get('book')
        book = Book.objects.get(id=book_id)
        user = request.user
        plated_end_at = request.POST.get('plated_end_at')
        orders = Order.objects.filter(book=book, end_at=None)
        if book.count == len(orders):
            messages.warning(request, "No available copies of the selected book.")
            return redirect('order:create_order')

        book.count -= 1
        book.save()

        order = Order.create(user=user, book=book, plated_end_at=plated_end_at)
        if order:
            messages.success(request, "Order created successfully.")
            return redirect('order:my_orders')
        else:
            messages.error(request, "Failed to create order.")
            return redirect('order:create_order')
    else:
        context = {'books': books}
        return render(request, 'order/create_order.html', context=context)


@staff_member_required
def close_order(request, pk):
    order = Order.get_by_id(pk)
    if order:
        if request.method == 'POST':
            end_at = timezone.now()
            order.update(end_at=end_at)
            order.save()
            return redirect('order:all_orders')
        else:
            return render(request, 'order/close_order.html', {'order': order})
    else:
        return redirect('order:all_orders')
