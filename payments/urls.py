from django.urls import path
from . import views

app_name = 'plati'

urlpatterns = [
    path('planuri/', views.plan_list, name='planuri'),
    # Stripe Checkout URLs (Commented out temporarily)
    # path('creeaza-sesiune-plata/<int:plan_id>/', views.create_checkout_session, name='create_checkout_session'),
    # path('succes/', views.payment_success, name='plata_reusita'),
    # path('anulat/', views.payment_cancel, name='plata_anulata'),
    # path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'), # Optional: Add webhook URL
]
