from django.db import models
from django.utils.text import slugify

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True) # e.g., Free, Standard, Business
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True) # Optional description
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default='€') # Assuming Euro for now

    # Feature Limits & Access
    max_active_jobs = models.PositiveIntegerField(default=1, help_text="Maximum number of jobs a company can have active at once. Use 0 for unlimited (handle in logic).")
    visibility_days = models.PositiveIntegerField(default=30, help_text="Number of days a job posting remains visible.")
    has_company_dashboard = models.BooleanField(default=True, help_text="Does this plan include access to the company dashboard?")
    has_cv_access = models.BooleanField(default=False, help_text="Does this plan allow access to candidate CVs?")
    promoted_jobs_limit = models.PositiveIntegerField(default=0, help_text="Maximum number of jobs that can be promoted simultaneously.")
    has_priority_support = models.BooleanField(default=False, help_text="Does this plan include priority support?")

    # Special Flags
    is_active = models.BooleanField(default=True, help_text="Allow disabling plans from being selected.")
    is_featured = models.BooleanField(default=False, help_text="Mark this plan as 'Popular' or featured.")
    is_promoted_only = models.BooleanField(default=False, help_text="Is this a special plan only for promoting existing jobs?")

    class Meta:
        ordering = ['price'] # Order plans by price by default

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        # Handle 'unlimited' representation if needed (e.g., store 0 or None)
        if self.name == "Enterprise": # Example: Set a high number for Enterprise 'unlimited'
             self.max_active_jobs = 9999 # Or use None if field allows null=True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price}{self.currency})"


class CompanySubscription(models.Model):
    """
    Links a CompanyProfile to a SubscriptionPlan and tracks its status.
    """
    company = models.OneToOneField('accounts.CompanyProfile', on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='company_subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True, help_text="Date when the subscription expires. Null for non-expiring plans.")
    is_active = models.BooleanField(default=False, help_text="Is the subscription currently active?")
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe Subscription ID for recurring payments.")
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe Payment Intent ID for one-time payments.")
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe Checkout Session ID used for the purchase.")

    class Meta:
        verbose_name = "Company Subscription"
        verbose_name_plural = "Company Subscriptions"
        ordering = ['-start_date']

    def __str__(self):
        plan_name = self.plan.name if self.plan else "No Plan"
        status = "Active" if self.is_active else "Inactive"
        return f"{self.company.company_name} - {plan_name} ({status})"
