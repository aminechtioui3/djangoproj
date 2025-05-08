from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Category, Product, Table, Waiter,
    Order, OrderItem
)
from .forms import (
    CategoryForm, ProductForm, TableForm,
    WaiterForm, OrderForm, OrderItemForm,
    OrderItemFormSet
)

# ─── CATEGORY ───────────────────────────────────────────────────────────────
@login_required
def index_category(request):
    categories = Category.objects.all()
    return render(request, 'index_category.html', {'categories': categories})

@login_required
def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created.', 'alert-success')
            return redirect('index_category')
    else:
        form = CategoryForm()
    return render(request, 'new_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated.', 'alert-success')
            return redirect('index_category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

@login_required
def destroy_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Category deleted.', 'alert-success')
    return redirect('index_category')

# ─── PRODUCT ────────────────────────────────────────────────────────────────
@login_required
def index_product(request):
    products = Product.objects.filter(active=True)
    return render(request, 'index_product.html', {'products': products})

@login_required
def new_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created.', 'alert-success')
            return redirect('index_product')
    else:
        form = ProductForm()
    return render(request, 'new_product.html', {'product_form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated.', 'alert-success')
            return redirect('index_product')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {
               'product_form': form,
               'product': product,
    })

@login_required
def destroy_product(request, product_id):
    Product.objects.filter(id=product_id).update(active=False)
    messages.success(request, 'Product deleted.', 'alert-success')
    return redirect('index_product')

# ─── TABLE ──────────────────────────────────────────────────────────────────
@login_required
def index_table(request):
    tables = Table.objects.all()
    return render(request, 'index_table.html', {'tables': tables})

@login_required
def new_table(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Table created.', 'alert-success')
            return redirect('index_table')
    else:
        form = TableForm()
    return render(request, 'new_table.html', {'form': form})

@login_required
def edit_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, 'Table updated.', 'alert-success')
            return redirect('index_table')
    else:
        form = TableForm(instance=table)
    return render(request, 'edit_table.html', {'form': form})

@login_required
def destroy_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.delete()
    messages.success(request, 'Table destroyed.', 'alert-success')
    return redirect('index_table')

# ─── WAITER ─────────────────────────────────────────────────────────────────
@login_required
def index_waiter(request):
    waiters = Waiter.objects.all()
    return render(request, 'index_waiter.html', {'waiters': waiters})

@login_required
def new_waiter(request):
    if request.method == 'POST':
        form = WaiterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waiter created.', 'alert-success')
            return redirect('index_waiter')
    else:
        form = WaiterForm()
    return render(request, 'new_waiter.html', {'form': form})

@login_required
def edit_waiter(request, waiter_id):
    waiter = get_object_or_404(Waiter, id=waiter_id)
    if request.method == 'POST':
        form = WaiterForm(request.POST, request.FILES, instance=waiter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Waiter updated.', 'alert-success')
            return redirect('index_waiter')
    else:
        form = WaiterForm(instance=waiter)
    return render(request, 'edit_waiter.html', {'form': form})

@login_required
def destroy_waiter(request, waiter_id):
    waiter = get_object_or_404(Waiter, id=waiter_id)
    waiter.delete()
    messages.success(request, 'Waiter deleted.', 'alert-success')
    return redirect('index_waiter')

# ─── ORDER ──────────────────────────────────────────────────────────────────
@login_required
def index_order(request):
    orders = Order.objects.all()
    return render(request, 'index_order.html', {'orders': orders})

@login_required
def show_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.select_related('product').all()
    return render(request, 'show_order.html', {'order': order, 'items': items})

@login_required
def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save()
            formset.instance = order
            formset.save()
            messages.success(request, 'Order created.', 'alert-success')
            return redirect('index_order')
    else:

        form = OrderForm(initial={'order_status': 'Confirm'})
        formset = OrderItemFormSet()
    return render(request, 'new_order.html', {'form': form, 'formset': formset})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        formset = OrderItemFormSet(request.POST, instance=order)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Order updated.', 'alert-success')
            return redirect('index_order')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    return render(request, 'edit_order.html', {'form': form, 'formset': formset})

@login_required
def destroy_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, 'Order deleted.', 'alert-success')
    return redirect('index_order')

# ─── ORDER ITEM ──────────────────────────────────────────────────────────────
@login_required
def new_order_item(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
            messages.success(request, 'Item added.', 'alert-success')
            return redirect('show_order', order_id)
    else:
        form = OrderItemForm()
    return render(request, 'new_order_item.html', {'form': form, 'order': order})

@login_required
def edit_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        form = OrderItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated.', 'alert-success')
            return redirect('show_order', item.order.id)
    else:
        form = OrderItemForm(instance=item)
    return render(request, 'edit_order_item.html', {'form': form, 'order': item.order})

@login_required
def destroy_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)
    order_id = item.order.id
    item.delete()
    messages.success(request, 'Item deleted.', 'alert-success')
    return redirect('show_order', order_id)
