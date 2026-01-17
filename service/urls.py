from django.urls import path
from .views import ContactEmail, index

urlpatterns = [
    path('api/contact/', ContactEmail.as_view(), name='contact'),
    path('', index, name='index'),
]