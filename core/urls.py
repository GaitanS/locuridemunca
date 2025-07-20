from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('despre-noi/', views.AboutView.as_view(), name='about'),
    path('termeni-si-conditii/', views.TermsView.as_view(), name='terms'),
    path('politica-confidentialitate/', views.PrivacyView.as_view(), name='privacy'),
    # Dedicated contact page URL (if needed in the future)
    path('contact/', views.ContactView.as_view(), name='contact'),
    # FAQ page URL
    path('faq/', views.FAQView.as_view(), name='faq'),
    # URL for newsletter subscription form submission (likely from footer or about page)
    path('newsletter/subscribe/', views.newsletter_subscribe_view, name='newsletter_subscribe'),
    # URL for contact form submission specifically from the About page
    path('contact/submit/', views.contact_submit_view, name='contact_submit'),
]
