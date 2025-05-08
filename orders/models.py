from django.db import models

# -- CATEGORY -----------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# -- PRODUCT ------------------------------------------------------------------
class Product(models.Model):
    product_name    = models.CharField(max_length=200)
    product_details = models.TextField()
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    active          = models.BooleanField(default=True)
    category        = models.ForeignKey(
       Category,
       on_delete=models.PROTECT,
       related_name='products',
       null=True,    # allow existing rows to be NULL for now
       blank=True,   # optional, lets forms leave it empty
   )

    def __str__(self):
        return f"{self.product_name} ({self.price} tk)"


# -- TABLE --------------------------------------------------------------------
class Table(models.Model):
    STATUS_AVAILABLE   = 'available'
    STATUS_RESERVED    = 'reserved'
    STATUS_OCCUPIED    = 'occupied'
    STATUS_UNAVAILABLE = 'unavailable'

    STATUS_CHOICES = [
        (STATUS_AVAILABLE,   'Available'),
        (STATUS_RESERVED,    'Reserved'),
        (STATUS_OCCUPIED,    'Occupied'),
        (STATUS_UNAVAILABLE, 'Unavailable'),
    ]

    code            = models.CharField(max_length=20, unique=True)
    number_of_seats = models.PositiveIntegerField()
    status          = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE
    )

    def __str__(self):
        return f"Table {self.code} ({self.get_status_display()})"


# -- WAITER -------------------------------------------------------------------
class Waiter(models.Model):
    STATUS_ON_DUTY  = 'on_duty'
    STATUS_OFF_DUTY = 'off_duty'

    STATUS_CHOICES = [
        (STATUS_ON_DUTY,  'On Duty'),
        (STATUS_OFF_DUTY, 'Off Duty'),
    ]

    name  = models.CharField(max_length=100)
    code  = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='waiters/')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ON_DUTY
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


# -- ORDER --------------------------------------------------------------------
class Order(models.Model):
    name           = models.CharField(max_length=200)
    phone          = models.CharField(max_length=20)
    address        = models.TextField()
    delivery_date  = models.DateField(blank=True, null=True)
    payment_option = models.CharField(max_length=50)
    order_status   = models.CharField(max_length=50)

    # Relationships
    table  = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    waiter = models.ForeignKey(
        Waiter,                     # ← the 'to' argument
        on_delete=models.PROTECT,   # ← what happens if a waiter is deleted
        related_name='orders',
        null=True,                  # allow NULL for existing data
        blank=True
    )

    created_at = models.DateTimeField(
       auto_now_add=True,
       null=True,    # allow NULL for old records
       blank=True,   # optional—lets forms leave it empty
    
    )

    def __str__(self):
        return f"Order #{self.id} for {self.name}"


# -- ORDER ITEM ---------------------------------------------------------------
class OrderItem(models.Model):
    order   = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Unit price at time of order"
    )

    def __str__(self):
        return f"{self.quantity}× {self.product.product_name} for Order #{self.order.id}"
