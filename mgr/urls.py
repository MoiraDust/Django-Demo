from django.urls import path

from mgr import customer, medicine
from mgr.sign_in_out import signin, signout

urlpatterns = [
    path('customers', customer.dispatcher),
    path('signin', signin),
    path('signout', signout),
    path('medicines', medicine.dispatcher)
]
