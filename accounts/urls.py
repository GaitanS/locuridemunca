from django.urls import path, include # Import include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/jobseeker/', views.JobSeekerSignUpView.as_view(), name='jobseeker_signup'),
    path('signup/company/', views.CompanySignUpView.as_view(), name='company_signup'),
    path('signup/done/', views.SignUpDoneView.as_view(), name='signup_done'),
    path('activate/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activate'),

    # Dashboards
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'), # Generic dashboard redirector
    path('dashboard/jobseeker/', views.JobSeekerDashboardView.as_view(), name='jobseeker_dashboard'),
    path('dashboard/company/', views.CompanyDashboardView.as_view(), name='company_dashboard'),

    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.CompanyProfileUpdateView.as_view(), name='company_profile_edit'), # Company profile edit URL

    # Include default auth urls (login, logout, password_reset, etc.)
    # These expect templates in a 'registration' directory
    path('', include('django.contrib.auth.urls')),
]
