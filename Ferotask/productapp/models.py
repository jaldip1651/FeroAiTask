from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False, error_messages={'unique': "Name is already exists"})
    contact_number = models.CharField(max_length=25, null=True)
    email = models.EmailField(max_length=254, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tbl_customer"


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False, error_messages={'unique': "product name is already exists"})
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message="Weight must be a positive number"),
            MaxValueValidator(25, message="Weight must not more then 25kg")
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tbl_product"


def increment_order_number():
    global order_number
    last_Order = Order.objects.all().order_by('id').last()
    if not last_Order:
        return 'ORD00001'

    if last_Order.order_number == '':
        pass
    else:
        order_number = last_Order.order_number

    order_int = int(order_number.split('ORD')[-1])

    width = 4
    new_order_int = order_int + 1
    formatted = (width - len(str(new_order_int))) * "0" + str(new_order_int)
    new_order_no = 'ORD' + str(formatted)
    return new_order_no


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=500, default=increment_order_number, null=False, blank=False)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = "tbl_Order"


class Order_Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = "tbl_Order_Item"
