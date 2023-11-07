# urls.py
from django.urls import path
from .views import order_view

urlpatterns = [
    path('place_order/', order_view, name='place_order'),
    # ... other url patterns
]
