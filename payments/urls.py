from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('plans/', views.plan_list, name='plan_list'),
    # Stripe Checkout URLs (Commented out temporarily)
    # path('create-checkout-session/<int:plan_id>/', views.create_checkout_session, name='create_checkout_session'),
    # path('success/', views.payment_success, name='payment_success'),
    # path('cancel/', views.payment_cancel, name='payment_cancel'),
    # path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'), # Optional: Add webhook URL
]
