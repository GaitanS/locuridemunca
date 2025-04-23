from django.shortcuts import render
from django.views.generic import TemplateView
from jobs.models import Category, Job # Import job models

# Create your views here.

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch categories (consider adding job counts later)
        context['categories'] = Category.objects.all()[:6] # Limit to 6 popular categories for display
        # Fetch recent jobs (replace with recommended/featured logic later)
        context['recent_jobs'] = Job.objects.filter(is_published=True).select_related(
            'company', 'category', 'company__companyprofile'
        ).order_by('-created_at')[:4] # Limit to 4 recent jobs
        # Add context for other sections later (featured, promoted etc.)
        return context

class AboutView(TemplateView):
    """
    View for the About Us page.
    """
    template_name = "core/about.html"
    # Add get_context_data if specific context is needed for the about page later

class TermsView(TemplateView):
    """
    View for the Terms and Conditions page.
    """
    template_name = "core/terms.html"

class PrivacyView(TemplateView):
    """
    View for the Privacy Policy page.
    """
    template_name = "core/privacy.html"

class ContactView(TemplateView):
    """
    View for the Contact page.
    """
    template_name = "core/contact.html"
    # Add form handling logic here later if needed
