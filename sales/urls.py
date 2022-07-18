from django.urls import path

from sales.views import listorders, listorders2, getCustomers, getCustomerByName

urlpatterns = [
    path('orders', listorders),
    path('orders2', listorders2),
    path('customers', getCustomers),
    path('getCustomerByName/', getCustomerByName)
]
