import uuid
from django.core.validators import MaxLengthValidator
from django.db import models
from main.models import CustomUser
from products.models import Product

# Create your models here.
# invoice model
class Invoice(models.Model):
    tax = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    discount = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    shipment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grandtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invoice_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self) -> str:

        if(self.user):
            return self.user.username + "'s invoice of " + str(self.grandtotal) 
        return "Hanging invoice of " + str(self.grandtotal) 


# order model
class Order(models.Model):

    invoice = models.ForeignKey(to = Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product = models.ForeignKey(to = Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.name + " for invoice " + str(self.invoice) + " worth " + str(self.order_price)


# shipment model
class Shipment(models.Model):

    invoice = models.ForeignKey(to = Invoice, on_delete = models.SET_NULL, null = True, blank = True)
    
    # auto created first time models is created an cannot be changed.
    shipment_date = models.DateTimeField(auto_now_add = True)

    # maximum value: 99 999 999.99 , 2 decimal palces and 8 other degits.
    cost = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    
    street_address =  models.CharField(null=False, blank=False, max_length= 500 , validators=[MaxLengthValidator])
    suburb =  models.CharField(null=True, blank=True, max_length= 500 , validators=[MaxLengthValidator])
    city =  models.CharField(null=False, blank=False, max_length= 500 , validators=[MaxLengthValidator])
    province = models.CharField(null=False, blank=False, max_length= 500 , validators=[MaxLengthValidator])
    postal_code = models.CharField(null=False, blank=False, max_length= 500 , validators=[MaxLengthValidator])
    country = models.CharField(null=False, blank=False, max_length= 500 , validators=[MaxLengthValidator])
    
    is_arrived = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, validators=[MaxLengthValidator])
    email = models.EmailField()
    code = models.UUIDField(default=uuid.uuid4, unique=True)
    firstname = models.CharField(max_length=100, validators=[MaxLengthValidator])
    lastname = models.CharField(max_length=100, validators=[MaxLengthValidator])

    def __str__(self) -> str:
        return "Shipment for " + self.firstname + " at " + self.email + " and Phone number: " + str(self.phone)