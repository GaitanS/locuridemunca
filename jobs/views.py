from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse # Import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView # Import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Job, Category, Application, JobReport # Import Application and JobReport models
from .forms import JobForm, JobReportForm # Import JobForm and JobReportForm
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
        location = self.request.GET.get('location') # This filter might need updating to use city/country
        category_slug = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(company__companyprofile__company_name__icontains=query)
            )

        if location:
            # TODO: Update location filter to search city and/or country
            queryset = queryset.filter(
                 Q(city__icontains=location) # Simple city search for now
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
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    slug_field = 'slug' # Specify the field to use for lookup
    slug_url_kwarg = 'slug' # Specify the URL keyword argument

    def get_queryset(self):
        # Ensure we can only view published jobs, prefetch related data
        return Job.objects.filter(is_published=True).select_related('company', 'category', 'company__companyprofile')

# --- Job Creation ---

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('accounts:company_dashboard')

    def test_func(self):
        return self.request.user.user_type == 'company'

    def handle_no_permission(self):
        messages.error(self.request, "Doar companiile pot posta anunțuri.")
        return redirect('core:home')

    def form_valid(self, form):
        form.instance.company = self.request.user
        form.instance.is_published = True
        messages.success(self.request, f"Anunțul '{form.instance.title}' a fost creat cu succes.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Postează un Anunț Nou"
        return context

# --- Job Update ---

class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('accounts:company_dashboard')

    def test_func(self):
        job = self.get_object()
        return self.request.user == job.company

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să editați acest anunț.")
        return redirect('accounts:company_dashboard')

    def form_valid(self, form):
        messages.success(self.request, f"Anunțul '{form.instance.title}' a fost actualizat cu succes.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editează Anunțul: {self.object.title}"
        return context

# --- Job Application ---

class ApplyToJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('accounts:login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker'

    def handle_no_permission(self):
        messages.error(self.request, "Doar candidații autentificați pot aplica la joburi.")
        return redirect('accounts:login')

    def post(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, pk=job_id, is_published=True)
        applicant = request.user

        if not hasattr(applicant, 'jobseekerprofile') or not applicant.jobseekerprofile.cv:
             messages.warning(request, "Vă rugăm să încărcați un CV în profilul dumneavoastră înainte de a aplica.")
             return redirect('jobs:job_detail', pk=job.pk)

        if Application.objects.filter(job=job, applicant=applicant).exists():
            messages.info(request, "Ați aplicat deja la acest job.")
            return redirect('jobs:job_detail', pk=job.pk)

        try:
            Application.objects.create(job=job, applicant=applicant)
            messages.success(request, f"Aplicația dumneavoastră pentru '{job.title}' a fost trimisă cu succes!")
            return redirect('accounts:jobseeker_dashboard')
        except IntegrityError:
             messages.error(request, "A apărut o eroare. Se pare că ați aplicat deja.")
             return redirect('jobs:job_detail', pk=job.pk)
        except Exception as e:
            messages.error(request, f"A apărut o eroare la trimiterea aplicației: {e}")
            return redirect('jobs:job_detail', pk=job.pk)

# --- Save/Unsave Job ---

class SaveJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('accounts:login')

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

        return redirect(request.META.get('HTTP_REFERER', reverse('jobs:job_detail', kwargs={'pk': job.pk})))


class UnsaveJobView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('accounts:login')

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

        return redirect(request.META.get('HTTP_REFERER', reverse('jobs:job_detail', kwargs={'pk': job.pk})))

# --- View Applications for a Job ---

class JobApplicationsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'jobs/job_applications.html'
    context_object_name = 'applications'
    paginate_by = 10

    def test_func(self):
        job = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        return self.request.user.is_authenticated and self.request.user == job.company

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să vizualizați aplicațiile pentru acest job.")
        return redirect('accounts:company_dashboard')

    def get_queryset(self):
        job = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        return Application.objects.filter(job=job).select_related(
            'applicant', 'applicant__jobseekerprofile'
        ).order_by('-applied_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        return context

# --- Report Job ---

class ReportJobView(LoginRequiredMixin, FormView):
    form_class = JobReportForm
    template_name = 'jobs/job_report_form.html' # New template for reporting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        context['page_title'] = f"Raportează Anunțul: {context['job'].title}"
        return context

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs['job_pk'])
        reporter = self.request.user if self.request.user.is_authenticated else None
        reason = form.cleaned_data['reason']

        try:
            JobReport.objects.create(
                job=job,
                reporter=reporter,
                reason=reason
            )
            messages.success(self.request, "Vă mulțumim! Raportarea a fost trimisă și va fi analizată.")
            # Redirect back to job detail page
            return redirect('jobs:job_detail', pk=job.pk)
        except Exception as e:
            messages.error(self.request, f"A apărut o eroare la trimiterea raportării: {e}")
            # Render the form again with an error
            return super().form_invalid(form)

    # No need for test_func or handle_no_permission if anonymous reports are allowed
    # If login is required, LoginRequiredMixin handles it.

# Add views for job deletion later
