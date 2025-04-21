from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.plan_list_view, name='plan_list'), # Add plan list URL
    # Add other URL patterns here (e.g., for checkout)
]
