from django.urls import path
from . import views

app_name = 'joburi'

urlpatterns = [
    path('', views.JobListView.as_view(), name='lista_joburi'),
    path('creeaza/', views.JobCreateView.as_view(), name='postare_job'),
    path('<slug:slug>/', views.JobDetailView.as_view(), name='detalii_job'), # Use slug for detail view
    path('<int:pk>/editeaza/', views.JobUpdateView.as_view(), name='editare_job'), # Keep pk for actions for simplicity
    path('<int:pk>/aplica/', views.ApplyToJobView.as_view(), name='aplicare_job'), # Keep pk for actions
    path('<int:pk>/salveaza/', views.SaveJobView.as_view(), name='salvare_job'), # Keep pk for actions
    path('<int:pk>/elimina-salvat/', views.UnsaveJobView.as_view(), name='anulare_salvare_job'), # Keep pk for actions
    path('<int:job_pk>/aplicatii/', views.JobApplicationsListView.as_view(), name='aplicatii_job'), # Keep pk for actions
    path('<int:job_pk>/raporteaza/', views.ReportJobView.as_view(), name='raportare_job'), # Keep pk for actions
    # Add URLs for category lists, job deletion/management later
]
