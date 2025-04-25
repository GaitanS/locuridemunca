from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('post/', views.JobCreateView.as_view(), name='job_post'),
    path('<slug:slug>/', views.JobDetailView.as_view(), name='job_detail'), # Use slug for detail view
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_edit'), # Keep pk for actions for simplicity
    path('<int:pk>/apply/', views.ApplyToJobView.as_view(), name='job_apply'), # Keep pk for actions
    path('<int:pk>/save/', views.SaveJobView.as_view(), name='job_save'), # Keep pk for actions
    path('<int:pk>/unsave/', views.UnsaveJobView.as_view(), name='job_unsave'), # Keep pk for actions
    path('<int:job_pk>/applications/', views.JobApplicationsListView.as_view(), name='job_applications'), # Keep pk for actions
    path('<int:job_pk>/report/', views.ReportJobView.as_view(), name='job_report'), # Keep pk for actions
    # Add URLs for category lists, job deletion/management later
]
