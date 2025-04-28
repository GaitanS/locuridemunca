from django.urls import path, include, reverse_lazy # Import reverse_lazy
from django.contrib.auth import views as auth_views # Import auth views
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
    path('profile/', views.ProfileView.as_view(), name='profile'), # Generic profile view (maybe remove later if dashboards are sufficient)
    path('profile/company/edit/', views.CompanyProfileUpdateView.as_view(), name='company_profile_edit'), # Company profile edit URL
    path('profile/jobseeker/edit/', views.JobSeekerProfileUpdateView.as_view(), name='jobseeker_profile_edit'),

    # Company Detail View
    path('company/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),

    # Auth URLs - Override password_change to set success_url
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html', # Use our custom template
            success_url=reverse_lazy('accounts:password_change_done') # Explicitly set namespaced success URL
        ),
        name='password_change'
    ),
    path( # Keep the rest of the default auth URLs
        '',
        include('django.contrib.auth.urls')
    ),
    # Note: password_change_done URL name is included via the line above
]
