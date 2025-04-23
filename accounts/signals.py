from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, JobSeekerProfile, CompanyProfile
from payments.models import SubscriptionPlan # Corrected model name import

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a JobSeekerProfile or CompanyProfile
    when a new User instance is created.
    """
    if created:
        if instance.user_type == 'job_seeker':
            JobSeekerProfile.objects.create(user=instance)
        elif instance.user_type == 'company':
            # Try to find the default (cheapest, active) plan
            default_plan = SubscriptionPlan.objects.filter(is_active=True).order_by('price').first() # Corrected model name
            CompanyProfile.objects.create(
                user=instance,
                company_name=f"{instance.username}'s Company", # Placeholder, will be updated by form
                plan=default_plan # Assign the default plan if found
            )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the profile whenever the User instance is saved.
    """
    if hasattr(instance, 'jobseekerprofile'):
        instance.jobseekerprofile.save()
    if hasattr(instance, 'companyprofile'):
        instance.companyprofile.save()
