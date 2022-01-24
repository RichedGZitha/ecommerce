from django.db.models import fields
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from .models import Invoice, Shipment, Order

# order serializer
class OrderSerializer(serializers.ModelSerializer):

    invoice = serializers.SerializerMethodField(read_only = True)
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'UnitPrice', 'OrderPrice', 'Quntity', 'invoice', 'product']

    
    def get_product(self, obj):
        return obj.product

    def get_invoice(self, obj):
        return obj.invoice



# invoice serializer
class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['id', 'SubTotal', 'GrandTotal', 'Discount', 'Tax', 'ShipmentCost', 'InvoiceDate', 'user']


# shipment serializer
class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shipment
        fields = ['id','code', 'cost', 'street_address', 'lastname', 'firstname', 'city', 'province', 
        'postal_code', 'country', 'email', 'phone', 'is_arrived', 'invoice', 'shipment_date']
        