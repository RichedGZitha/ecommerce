from django.core.validators import MaxLengthValidator
from django.db import models
from main.models import CustomUser
from products.models import Product

# Create your models here.
# invoice model
class Invoice(models.Model):
    Tax = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    Discount = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ShipmentCost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    SubTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    GrandTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    InvoiceDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to = CustomUser, on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    def __str__(self) -> str:

        if(self.user):
            return self.user.username + "'s invoice of " + str(self.GrandTotal) 
        return "Hanging invoice of " + str(self.GrandTotal) 


# order model
class Order(models.Model):

    invoice = models.ForeignKey(to  = Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    Quantity = models.IntegerField(default=0)
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    OrderPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product = models.ForeignKey(to = Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.product.Name + " for invoice " + str(self.invoice) + " worth " + str(self.OrderPrice)


# shipment model
class Shipment(models.Model):

    invoice = models.ForeignKey(to = Invoice, on_delete = models.SET_NULL, null = True, blank = True)
    
    # auto created first time models is created an cannot be changed.
    ShipmentDate = models.DateTimeField(auto_now_add = True)

    # maximum value: 99 999 999.99 , 2 decimal palces and 8 other degits.
    ShipmentCost = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    Address = models.TextField()
    isArrived = models.BooleanField(default=False)
    Phone = models.CharField(max_length=20, validators=[MaxLengthValidator])
    Email = models.EmailField()
    Firstname = models.CharField(max_length=100, validators=[MaxLengthValidator])
    Lastname = models.CharField(max_length=100, validators=[MaxLengthValidator])

    def __str__(self) -> str:
        return "Shipment for " + self.Firstname + " at " + self.Email + " and Phone number: " + self.Phone