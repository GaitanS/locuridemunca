from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Job, Category
from django.db.models import Q # Import Q for complex lookups

# Create your views here.

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html' # Template for listing jobs
    context_object_name = 'jobs'
    paginate_by = 10 # Show 10 jobs per page

    def get_queryset(self):
        queryset = Job.objects.filter(is_published=True).select_related('company', 'category', 'company__companyprofile')

        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        category_slug = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company__companyprofile__company_name__icontains=query)
            )

        if location:
            queryset = queryset.filter(
                Q(location__icontains=location)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-created_at') # Order by creation date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # Pass all categories for the filter dropdown
        # Pass current query params back to template for preserving filter state (already handled by request.GET in template)
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html' # Template for job details
    context_object_name = 'job'

    def get_queryset(self):
        # Ensure we can only view published jobs, prefetch related data
        return Job.objects.filter(is_published=True).select_related('company', 'category', 'company__companyprofile')

# Add views for category-specific lists, job creation/management later
