from django.urls import path, include, reverse_lazy # Import reverse_lazy
from django.contrib.auth import views as auth_views # Import auth views
from . import views

app_name = 'conturi'

urlpatterns = [
    path('inregistrare/', views.SignUpView.as_view(), name='inregistrare'),
    path('inregistrare/candidat/', views.JobSeekerSignUpView.as_view(), name='inregistrare_candidat'),
    path('inregistrare/companie/', views.CompanySignUpView.as_view(), name='inregistrare_companie'),
    path('inregistrare/finalizat/', views.SignUpDoneView.as_view(), name='inregistrare_finalizata'),
    path('activeaza/<uidb64>/<token>/', views.ActivateAccountView.as_view(), name='activare'),

    # Dashboards
    path('panou-control/', views.DashboardView.as_view(), name='panou_control'), # Generic dashboard redirector
    path('panou-control/candidat/', views.JobSeekerDashboardView.as_view(), name='panou_candidat'),
    path('panou-control/companie/', views.CompanyDashboardView.as_view(), name='panou_companie'),

    # Profile
    path('profil/', views.ProfileView.as_view(), name='profil'), # Generic profile view (maybe remove later if dashboards are sufficient)
    path('profil/companie/editeaza/', views.CompanyProfileUpdateView.as_view(), name='editare_profil_companie'), # Company profile edit URL
    path('profil/candidat/editeaza/', views.JobSeekerProfileUpdateView.as_view(), name='editare_profil_candidat'),

    # Company Detail View (using slug)
    path('companie/<slug:slug>/', views.CompanyDetailView.as_view(), name='detalii_companie'),

    # Authentication URLs with Romanian names
    path('autentificare/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='autentificare'),
    path('deconectare/', auth_views.LogoutView.as_view(), name='deconectare'),
    
    # Password reset URLs with Romanian names
    path('resetare-parola/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='resetare_parola'),
    path('resetare-parola/trimis/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='resetare_parola_trimis'),
    path('resetare-parola/confirma/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='resetare_parola_confirma'),
    path('resetare-parola/finalizat/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='resetare_parola_finalizat'),
    
    # Password change URLs with Romanian names
    path(
        'schimba-parola/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url=reverse_lazy('conturi:schimbare_parola_finalizata')
        ),
        name='schimbare_parola'
    ),
    path('schimba-parola/finalizat/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='schimbare_parola_finalizata'),
]
