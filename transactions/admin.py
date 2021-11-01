from django.contrib import admin
from .models import Order, Invoice, Shipment

# Register your models here.
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Shipment)

