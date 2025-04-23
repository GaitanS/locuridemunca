from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('post/', views.JobCreateView.as_view(), name='job_post'), # URL for posting a new job
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    # Add URLs for category lists, job editing/management later
]
