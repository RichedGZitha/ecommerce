from datetime import datetime
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status, generics
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema  
from main import serializers
from main.models import Coupon
from transactions.models import Invoice, Order, Shipment
from transactions.serializers import InvoiceSerializer, OrderSerializer, ShipmentSerializer


# get invoice(s)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def getUserInvoices(request):

    # get all invoices belonging to a user.
    invoices = Invoice.objects.filter(user = request.user)

    # serialize these.
    invoicesSerializer = InvoiceSerializer(invoices, many= True)

    return Response(invoicesSerializer.data, status=status.HTTP_200_OK)



# get orders belonging to an invoice
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def getOrdersForInvoice(request, pk = None):

    # pk - is the invoice id.
    orders = Order.objects.filter(invoice = pk)
    ordersSerilizer = OrderSerializer(orders, many = True)

    return Response(ordersSerilizer.data, status = status.HTTP_200_OK)


# create invoice and orders given the array of objects (order)
# order object {quantity, product}
# plus coupon code / referral code (promocode).  
'''@swagger_auto_schema(method='post', 
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, # object because the data is in json format
    properties={
        'orders': openapi.Schema(type=openapi.TYPE_ARRAY, description='This is an array of objects with {quantity:value, product:value', items=openapi.Items(type=openapi.TYPE_OBJECT)),
        'coupon': openapi.Schema(type=openapi.TYPE_STRING, description='Option coupon code to redeem for this purchase.')
    },
    
), operation_id="maketransactions_view_id")'''
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def makeTransaction(request):

    user = request.user
    data = request.data

    if data:

        ordersArray = data.get('orders')
        discountcode = data.get('coupon')

        # if the orders were supplied.
        if ordersArray:
            # create invoice
            invoice  = Invoice.objects.create(user = user)

            # create all order from array
            # Quantity, unitPrice, product

            tax = float(0.00)
            discount = float(0.00)
            subtotal = float(0.00)
            grandtotal = float(0.00)
            
            for order in ordersArray:
                
                # used for the invoice.
                tax += (order.quantity * order.unitprice) * 0.15
                subtotal +=  (order.quantity * order.unitprice)

                # create order
                Order.objects.create(Quantity = order.quantity, UnitPrice = order.unitprice, OrderPrice = order.unitprice * order.quantity, product = order.product)

            # apply a coupon
            if discountcode:
                try:
                    coupon = Coupon.objects.get(Code = discountcode, expiredDate__lte = datetime.now(), isValid = True)
                    discount += coupon.amount

                    # invalidate the coupon.
                    coupon.isValid = False
                    coupon.save()

                except Coupon.DoesNotExist:
                    pass
                 
            # update the invoice tax, discount, subtotal, grandtotal.
            grandtotal = (subtotal + tax) - discount

            invoice.Tax = tax
            invoice.Discount = discount
            invoice.SubTotal = subtotal
            invoice.GrandTotal = grandtotal
            invoice.save() 

            return Response({'success':'Your purchase was successful.', 'invoice': invoice.pk}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Could not make purchase'}, status=status.HTTP_400_BAD_REQUEST)


# create shipment or user
swagger_auto_schema(method='post', 
    request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, # object because the data is in json format
    properties={
        'pk': openapi.Schema(type=openapi.TYPE_INTEGER, description='The invoice primary key.'),
        'firstname': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the customer.'),
        'lastname': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the customer.'),
        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the customer. Used for communication.'),
        'address': openapi.Schema(type=openapi.TYPE_STRING, description='Address of the customer. Used for shipping and delivery.'),
        'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the customer. Used for elivery and communication')
    },
    required=['firstname', 'lastname', 'email', 'address', 'phone', 'pk'],
    
), operation_id='createshipment_view_id')
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([BrowsableAPIRenderer, JSONRenderer])
def createShipment(request, pk = None):

    data = request.data

    # if data is provided.
    if data:

        address = data.get('address')
        phone = data.get('phone')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')

        # if the data is given.
        isDataGiven = address and phone and firstname and lastname and email

        if isDataGiven:

            try:
                invoice = Invoice.objects.get(pk = pk)

                # TODO: based on address we need to determine the shipping cost.
                # Based on weight, region, price and amount.

                # but for now we will use hardcoded values.
                shipmentCost = float(25.00)


                # create new shipment.
                shipment = Shipment.objects.create(Address = address, Firstname = firstname, Lastname = lastname, Email = email, invoice = invoice.pk, ShipmentCost = shipmentCost)
                
                # update the invoice.
                invoice.ShipmentCost = shipmentCost
                invoice.save()

                shipmentSerializer = ShipmentSerializer(instance=shipment, many = False)

                return Response(shipmentSerializer.data, status=status.HTTP_200_OK)

            except Invoice.DoesNotExist:
                return Response({'error': 'Could not find invoice.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Could not create a shipment.'}, status=status.HTTP_400_BAD_REQUEST)
