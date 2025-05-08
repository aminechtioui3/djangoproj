from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import (
    Category, Product, Table,
    Waiter, Order, OrderItem
)


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_details',
            'price',
            'active',
            'category',
        ]


class TableForm(ModelForm):
    class Meta:
        model = Table
        fields = [
            'code',
            'number_of_seats',
            'status',
        ]


class WaiterForm(ModelForm):
    class Meta:
        model = Waiter
        fields = [
            'name',
            'code',
            'image',
            'status',
        ]


class OrderForm(ModelForm):
    PAYMENT_CHOICES = [
        ('Postpay',        'Postpay'),
        ('Prepay (Full)',  'Prepay (Full)'),
        ('Prepay (Half)',  'Prepay (Half)'),
    ]
    STATUS_CHOICES = [
        ('Confirm',   'Confirm'),
        ('Ready',     'Ready'),
        ('Send',      'Send'),
        ('Delivered', 'Delivered'),
        ('Returned',  'Returned'),
        ('Cancelled', 'Cancelled'),
    ]

    delivery_date  = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES)
    order_status   = forms.TypedChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect
    )
    table  = forms.ModelChoiceField(
        queryset=Table.objects.all(),
        empty_label="Select table"
    )
    waiter = forms.ModelChoiceField(
        queryset=Waiter.objects.all(),
        empty_label="Select waiter"
    )

    class Meta:
        model = Order
        fields = [
            'name',
            'phone',
            'address',
            'delivery_date',
            'payment_option',
            'order_status',
            'table',
            'waiter',
        ]


class OrderItemForm(ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(active=True),
        empty_label="Select product"
    )
    quantity = forms.IntegerField(min_value=1)
    price    = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Unit price at time of order"
    )

    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity',
            'price',
        ]


# Inline formset: in your view you can do
# formset = OrderItemFormSet(request.POST or None, instance=order)
OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True
)
