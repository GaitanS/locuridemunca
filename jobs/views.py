from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse # Import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Job, Category, Application # Import Application model
from .forms import JobForm
from django.db.models import Q
from django.db import IntegrityError # To handle duplicate applications

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

# --- Job Application ---

class ApplyToJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Handles the job application submission (POST request).
    """
    def test_func(self):
        # Only allow logged-in job seekers to apply
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker'

    def handle_no_permission(self):
        messages.error(self.request, "Doar candidații autentificați pot aplica la joburi.")
        # Redirect to login or job detail page
        return redirect('accounts:login') # Or redirect back to job detail?

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=job_id, is_published=True)
        applicant = request.user

        # Optional: Check if applicant has a CV uploaded
        if not hasattr(applicant, 'jobseekerprofile') or not applicant.jobseekerprofile.cv:
             messages.warning(request, "Vă rugăm să încărcați un CV în profilul dumneavoastră înainte de a aplica.")
             # Redirect to profile edit page (needs to be created)
             # return redirect('accounts:jobseeker_profile_edit')
             return redirect('jobs:job_detail', pk=job.pk) # Redirect back for now

        # Check if already applied
        if Application.objects.filter(job=job, applicant=applicant).exists():
            messages.info(request, "Ați aplicat deja la acest job.")
            return redirect('jobs:job_detail', pk=job.pk)

        # Create the application
        try:
            Application.objects.create(job=job, applicant=applicant)
            messages.success(request, f"Aplicația dumneavoastră pentru '{job.title}' a fost trimisă cu succes!")
            # Redirect to job seeker dashboard or job detail page
            return redirect('accounts:jobseeker_dashboard')
        except IntegrityError: # Should be caught by the exists() check, but as a fallback
             messages.error(request, "A apărut o eroare. Se pare că ați aplicat deja.")
             return redirect('jobs:job_detail', pk=job.pk)
        except Exception as e:
            messages.error(request, f"A apărut o eroare la trimiterea aplicației: {e}")
            return redirect('jobs:job_detail', pk=job.pk)

# --- Save/Unsave Job ---

# Removed redundant decorator - LoginRequiredMixin handles login check
class SaveJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    """ Handles saving a job for a job seeker """
    login_url = reverse_lazy('accounts:login') # Specify login URL for LoginRequiredMixin

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker'

    def handle_no_permission(self):
        messages.error(self.request, "Doar candidații autentificați pot salva joburi.")
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.jobseekerprofile

        if job not in profile.saved_jobs.all():
            profile.saved_jobs.add(job)
            messages.success(request, f"Jobul '{job.title}' a fost salvat.")
        else:
            messages.info(request, f"Jobul '{job.title}' este deja salvat.")

        # Redirect back to the previous page or job detail
        return redirect(request.META.get('HTTP_REFERER', reverse('jobs:job_detail', kwargs={'pk': job.pk})))


# Removed redundant decorator - LoginRequiredMixin handles login check
class UnsaveJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    """ Handles unsaving a job for a job seeker """
    login_url = reverse_lazy('accounts:login') # Specify login URL for LoginRequiredMixin

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker'

    def handle_no_permission(self):
        messages.error(self.request, "Doar candidații autentificați pot anula salvarea joburilor.")
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=job_id)
        profile = request.user.jobseekerprofile

        if job in profile.saved_jobs.all():
            profile.saved_jobs.remove(job)
            messages.success(request, f"Salvarea pentru jobul '{job.title}' a fost anulată.")
        else:
            messages.info(request, f"Jobul '{job.title}' nu era salvat.")

        # Redirect back to the previous page or job detail
        return redirect(request.META.get('HTTP_REFERER', reverse('jobs:job_detail', kwargs={'pk': job.pk})))

# --- View Applications for a Job ---

class JobApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'jobs/job_applications.html' # New template
    context_object_name = 'applications'
    paginate_by = 10 # Paginate applications if needed

    def test_func(self):
        # Ensure user is the company that owns the job
        job = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        return self.request.user.is_authenticated and self.request.user == job.company

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să vizualizați aplicațiile pentru acest job.")
        return redirect('accounts:company_dashboard')

    def get_queryset(self):
        # Filter applications for the specific job
        job = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        # Optimize by fetching related applicant and profile data
        return Application.objects.filter(job=job).select_related(
            'applicant', 'applicant__jobseekerprofile'
        ).order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the job object to the context to display its title etc.
        context['job'] = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        return context


# Add views for job deletion, category-specific lists later
