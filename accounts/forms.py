from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, CompanyProfile

class JobSeekerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # Add any other fields needed at signup for job seekers

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name') # Add email, first_name, last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_seeker'
        if commit:
            user.save()
            # Profile is created automatically by signal
        return user

class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(required=True, max_length=255)
    # Add any other fields needed at signup for companies

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) # Only email needed for User model here

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        if commit:
            user.save()
            # Update the company profile created by the signal
            company_profile = user.companyprofile # Access profile via related_name
            company_profile.company_name = self.cleaned_data.get('company_name')
            # Add other company profile fields from the form here
            company_profile.save()
        return user
