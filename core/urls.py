from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'), # Add About Us page URL
    # Add other core URL patterns here (e.g., for contact page)
]
