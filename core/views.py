from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse # Added reverse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.contrib import messages
from jobs.models import Category, Job
from .forms import NewsletterSubscriptionForm, ContactForm # Import forms
from .models import NewsletterSubscription, ContactMessage, ContactInfo, FAQ, Article # Import models
from django.views.decorators.http import require_POST # Import decorator

# Create your views here.

class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch categories (consider adding job counts later)
        # Fetch 6 random categories
        context['categories'] = Category.objects.order_by('?')[:6]
        # Fetch recent jobs (replace with recommended/featured logic later)
        context['recent_jobs'] = Job.objects.filter(is_published=True).select_related(
            'company', 'category', 'company__companyprofile'
        ).order_by('-created_at')[:4] # Limit to 4 recent jobs
        # Fetch featured articles for homepage
        context['featured_articles'] = Article.objects.filter(
            is_published=True, is_featured=True
        ).select_related('author').order_by('-published_at')[:3] # Limit to 3 featured articles
        # Add context for other sections later (featured, promoted etc.)
        return context

class AboutView(TemplateView): # Reverted to TemplateView
    """
    View for the About Us page.
    """
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the newsletter form to the context for display
        if 'newsletter_form' not in context:
             context['newsletter_form'] = NewsletterSubscriptionForm()
        # Add the contact form to the context for display
        if 'contact_form' not in context:
            context['contact_form'] = ContactForm()
        return context

# Separate view to handle newsletter subscription POST
@require_POST # Ensure this view only accepts POST requests
def newsletter_subscribe_view(request):
    form = NewsletterSubscriptionForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        subscription, created = NewsletterSubscription.objects.get_or_create(email=email)
        if created:
            messages.success(request, "Vă mulțumim pentru abonare!")
        else:
            messages.info(request, "Adresa de email este deja abonată.")
    else:
        # Add form errors to messages to display them on the redirected page
        for field, errors in form.errors.items():
            for error in errors:
                 messages.error(request, f"{form.fields[field].label if form.fields[field].label else field}: {error}") # Use field label
        # Or a generic error message
        # messages.error(request, "Vă rugăm introduceți o adresă de email validă.")

    # Redirect back to the 'about' page regardless of success/failure
    # The messages framework will display the appropriate message
    return redirect(reverse('core:about') + '#newsletter-form') # Redirect back to about page, potentially to an anchor

# Separate view to handle contact form submission from About page
@require_POST
def contact_submit_view(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Mesajul dumneavoastră a fost trimis cu succes! Vă vom contacta în curând.")
        # Redirect back to about page, clear form by redirecting
        return redirect(reverse('core:about') + '#contact-form')
    else:
        # If form is invalid, re-render the About page with the form containing errors
        messages.error(request, "A apărut o eroare la trimiterea mesajului. Vă rugăm verificați câmpurile.")
        # We need to pass the invalid form back to the AboutView context
        # This is a bit tricky with function views redirecting. A common pattern is to store errors in session
        # or re-render the template directly, but let's try passing it via messages for now
        # or better, re-render the AboutView with the invalid form
        view = AboutView()
        view.request = request # Set request for context processing
        context = view.get_context_data(contact_form=form) # Pass invalid form
        return render(request, AboutView.template_name, context)

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

class ContactView(FormView): # This remains for a potential dedicated /contact page
    """
    View for the dedicated Contact page (if needed).
    Handles Contact form submission for that page.
    """
    template_name = "core/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('core:contact') # Redirect back to contact page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add contact info from database
        context['contact_info'] = ContactInfo.objects.filter(is_active=True).order_by('order')
        return context

    def form_valid(self, form):
        # Save the message to the database
        form.save()
        messages.success(self.request, "Mesajul dumneavoastră a fost trimis cu succes! Vă vom contacta în curând.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "A apărut o eroare. Vă rugăm verificați câmpurile completate.")
        # Need to manually call get_context_data for FormView on invalid
        return self.render_to_response(self.get_context_data(form=form))

class FAQView(TemplateView):
    """
    View for the FAQ page.
    """
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add FAQ items from database
        context['faqs'] = FAQ.objects.filter(is_active=True).order_by('order')
        return context

class ArticleListView(ListView):
    """
    View for listing all published articles.
    """
    model = Article
    template_name = "core/article_list.html"
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('author').order_by('-published_at')

class ArticleDetailView(DetailView):
    """
    View for displaying a single article.
    """
    model = Article
    template_name = "core/article_detail.html"
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related('author')
