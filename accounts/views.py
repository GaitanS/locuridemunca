from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, View
from .forms import JobSeekerSignUpForm, CompanySignUpForm
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages # For displaying messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        context['profile'] = self.request.user.jobseekerprofile
        # Add other context like saved jobs, applications later
        return context

@method_decorator(login_required, name='dispatch')
class CompanyDashboardView(TemplateView):
    template_name = 'accounts/company_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.companyprofile
        # Add other context like posted jobs, applications received later
        return context


# Add Login, Logout, Password Reset views later (some are included via django.contrib.auth.urls)
# Add Profile Edit views later
