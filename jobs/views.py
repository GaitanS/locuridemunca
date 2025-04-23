from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView # Import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Job, Category
from .forms import JobForm # Import the new form
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

# --- Job Creation ---

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html' # We'll create this template next
    # Redirect to company dashboard after successful creation
    success_url = reverse_lazy('accounts:company_dashboard')

    def test_func(self):
        # Only allow users with user_type 'company' to access this view
        return self.request.user.user_type == 'company'

    def handle_no_permission(self):
        # Optional: Redirect non-company users or show an error
        messages.error(self.request, "Doar companiile pot posta anunțuri.")
        # Redirect to home or job list perhaps?
        return redirect('core:home')

    def form_valid(self, form):
        # Assign the logged-in company user to the job posting
        form.instance.company = self.request.user
        # Default to published, can add draft logic later
        form.instance.is_published = True
        messages.success(self.request, f"Anunțul '{form.instance.title}' a fost creat cu succes.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Postează un Anunț Nou" # Title for the template
        return context

# --- Job Update ---

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html' # Reuse the job form template
    # Redirect to company dashboard after successful update
    success_url = reverse_lazy('accounts:company_dashboard')

    def test_func(self):
        # Check if the logged-in user is the owner of the job
        job = self.get_object()
        return self.request.user == job.company

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să editați acest anunț.")
        return redirect('accounts:company_dashboard') # Redirect back to dashboard

    def form_valid(self, form):
        messages.success(self.request, f"Anunțul '{form.instance.title}' a fost actualizat cu succes.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editează Anunțul: {self.object.title}" # Dynamic title
        return context


# Add views for job deletion, category-specific lists later
