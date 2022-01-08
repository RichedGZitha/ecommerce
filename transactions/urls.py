from django.urls import path
from . import views

urlpatterns = [
    path('get-user-invoices/', view=views.getUserInvoices, name='get-user-invoices' ),
    path('get-orders-for-invoice/<slug:pk>/', view=views.getOrdersForInvoice, name='get-user-orders-for-invoice'),
    path('make-transaction/', view = views.makeTransaction, name='make-transaction'),
    path('create-shipment/<slug:pk>/', view=views.createShipment, name='create-shipment'),
    path('calculate-purchase/', view=views.CalculateGrandTotal,  name='calculate-purchase'),
]
