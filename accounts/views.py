from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, View
from .forms import JobSeekerSignUpForm, CompanySignUpForm, CompanyProfileForm, JobSeekerProfileForm # Import JobSeekerProfileForm
from .models import User, JobSeekerProfile, CompanyProfile # Import profile models
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from jobs.models import Job, Application # Import Job and Application models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Import UserPassesTestMixin
from django.views.generic.edit import UpdateView # Import UpdateView

# Basic signup choice view (can be expanded later)
class SignUpView(TemplateView):
    template_name = 'registration/signup.html' # We'll use Django's default registration template dir

class JobSeekerSignUpView(CreateView):
    model = User
    form_class = JobSeekerSignUpForm
    template_name = 'registration/signup_form.html' # Generic form template
    success_url = reverse_lazy('accounts:signup_done') # Redirect to a 'check email' page

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'job_seeker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # print("--- JobSeekerSignUpView: form_valid called ---") # Removed Debug print
        user = form.save(commit=False)
        user.is_active = False # User is inactive until email confirmation
        user.save()

        # Send activation email
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your JoburiPentruRomani account.'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.success(self.request, 'Please check your email to complete the registration.')
        return redirect(self.success_url)

    def form_invalid(self, form):
        # print("--- JobSeekerSignUpView: form_invalid called ---") # Removed Debug print
        # print("Form Errors:", form.errors.as_json()) # Removed Debug print errors
        return super().form_invalid(form)


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'registration/signup_form.html' # Generic form template
    success_url = reverse_lazy('accounts:signup_done') # Redirect to a 'check email' page

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # User is inactive until email confirmation
        user.save() # Save user first
        # Update profile *after* user is saved
        company_profile = user.companyprofile
        company_profile.company_name = form.cleaned_data.get('company_name')
        company_profile.save()

        # Send activation email
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your JoburiPentruRomani account.'
        message = render_to_string('registration/account_activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.success(self.request, 'Please check your email to complete the registration.')
        return redirect(self.success_url)

# View to show after signup email is sent
class SignUpDoneView(TemplateView):
    template_name = 'registration/signup_done.html'

# View to handle account activation link
class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user) # Optionally log in user directly
            messages.success(request, 'Your account has been confirmed successfully! You can now log in.')
            return redirect('login') # Redirect to login page
        else:
            messages.error(request, 'The confirmation link was invalid, possibly because it has already been used or expired.')
            return redirect('login') # Redirect to login or a specific error page

# --- Dashboards ---

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Redirects user to the appropriate dashboard based on user_type.
    """
    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'job_seeker':
            return redirect('accounts:jobseeker_dashboard')
        elif request.user.user_type == 'company':
            return redirect('accounts:company_dashboard')
        else:
            # Handle unexpected user type or redirect to a generic page
            return redirect('core:home') # Or raise an error

@method_decorator(login_required, name='dispatch')
class JobSeekerDashboardView(TemplateView):
    template_name = 'accounts/jobseeker_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Ensure profile exists, handle potential DoesNotExist
            profile = self.request.user.jobseekerprofile
            context['profile'] = profile
        except JobSeekerProfile.DoesNotExist:
             context['profile'] = None
        else:
            # Fetch saved jobs if profile exists
            context['saved_jobs_list'] = profile.saved_jobs.all().select_related('company__companyprofile', 'category') # Fetch related data
            context['saved_jobs_count'] = context['saved_jobs_list'].count()

        # Fetch actual applications
        try:
            # Need to import Application model from jobs app
            from jobs.models import Application
            applications = Application.objects.filter(applicant=self.request.user).select_related('job', 'job__company__companyprofile').order_by('-applied_at')
            context['applications'] = applications
            context['applications_count'] = applications.count()
        except Exception as e: # Catch potential errors during query
            print(f"Error fetching applications: {e}") # Basic error logging
            context['applications'] = []
            context['applications_count'] = 0
        
        # Ensure saved jobs context exists even if profile doesn't (though unlikely for logged-in seeker)
        if 'saved_jobs_list' not in context:
             context['saved_jobs_list'] = []
             context['saved_jobs_count'] = 0

        return context

@method_decorator(login_required, name='dispatch')
class CompanyDashboardView(TemplateView):
    template_name = 'accounts/company_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_profile = self.request.user.companyprofile
        context['profile'] = company_profile
        # Fetch jobs posted by this company
        posted_jobs = Job.objects.filter(company=self.request.user).order_by('-created_at')
        context['posted_jobs'] = posted_jobs
        # Calculate stats
        context['active_job_count'] = posted_jobs.filter(is_published=True).count()
        # Calculate total applications received for all posted jobs
        context['total_applications_count'] = Application.objects.filter(job__in=posted_jobs).count()
        # Fetch subscription details (assuming CompanySubscription model exists and is linked)
        # try:
        #     context['subscription'] = CompanySubscription.objects.get(company=company_profile)
        # except CompanySubscription.DoesNotExist:
        #     context['subscription'] = None
        # Add other context like applications received later
        return context


# --- Profile View ---

@method_decorator(login_required, name='dispatch') # Ensure user is logged in
class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        if user.user_type == 'job_seeker':
            try:
                context['profile'] = user.jobseekerprofile
            except JobSeekerProfile.DoesNotExist:
                context['profile'] = None # Handle case where profile might not exist yet
        elif user.user_type == 'company':
            try:
                context['profile'] = user.companyprofile
            except CompanyProfile.DoesNotExist:
                context['profile'] = None # Handle case where profile might not exist yet
        else:
            context['profile'] = None
        return context


# Add Login, Logout, Password Reset views later (some are included via django.contrib.auth.urls)

# --- Profile Edit View ---

@method_decorator(login_required, name='dispatch')
class CompanyProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = CompanyProfile
    form_class = CompanyProfileForm
    template_name = 'accounts/profile_edit_form.html' # New template for editing
    success_url = reverse_lazy('accounts:company_dashboard') # Redirect to dashboard after update

    def test_func(self):
        # Ensure the logged-in user is a company and is editing their own profile
        profile = self.get_object()
        return self.request.user.is_authenticated and self.request.user.user_type == 'company' and profile.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să editați acest profil.")
        # Redirect to their own dashboard or profile view
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'company':
                 return redirect('accounts:company_dashboard')
            elif self.request.user.user_type == 'job_seeker':
                 return redirect('accounts:jobseeker_dashboard')
        return redirect('core:home') # Fallback redirect

    def get_object(self, queryset=None):
        # Get the profile object associated with the logged-in user
        # This assumes a CompanyProfile always exists for a company user (created by signal)
        return self.request.user.companyprofile

    def form_valid(self, form):
        messages.success(self.request, "Profilul companiei a fost actualizat cu succes.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Editează Profilul Companiei"
        return context

# Add JobSeekerProfileUpdateView later
@method_decorator(login_required, name='dispatch')
class JobSeekerProfileUpdateView(UserPassesTestMixin, UpdateView):
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'accounts/profile_edit_form.html' # Reuse the same template for now
    success_url = reverse_lazy('accounts:jobseeker_dashboard') # Redirect to job seeker dashboard

    def test_func(self):
        # Ensure the logged-in user is a job seeker and is editing their own profile
        profile = self.get_object()
        return self.request.user.is_authenticated and self.request.user.user_type == 'job_seeker' and profile.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "Nu aveți permisiunea să editați acest profil.")
        # Redirect to their own dashboard or profile view
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 'job_seeker':
                 return redirect('accounts:jobseeker_dashboard')
            elif self.request.user.user_type == 'company':
                 return redirect('accounts:company_dashboard')
        return redirect('core:home') # Fallback redirect

    def get_object(self, queryset=None):
        # Get the profile object associated with the logged-in user
        # This assumes a JobSeekerProfile always exists for a job seeker user (created by signal)
        return self.request.user.jobseekerprofile

    def form_valid(self, form):
        messages.success(self.request, "Profilul a fost actualizat cu succes.")
        # The form's save method handles saving both User and Profile fields
        form.save()
        return super().form_valid(form) # Let UpdateView handle the redirect

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Editează Profilul Candidat"
        return context
