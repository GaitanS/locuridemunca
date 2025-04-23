from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('post/', views.JobCreateView.as_view(), name='job_post'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_edit'),
    path('<int:pk>/apply/', views.ApplyToJobView.as_view(), name='job_apply'),
    path('<int:pk>/save/', views.SaveJobView.as_view(), name='job_save'),
    path('<int:pk>/unsave/', views.UnsaveJobView.as_view(), name='job_unsave'),
    path('<int:job_pk>/applications/', views.JobApplicationsListView.as_view(), name='job_applications'), # URL to view applications for a job
    # Add URLs for category lists, job deletion/management later
]
