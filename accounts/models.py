from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model inheriting from AbstractUser.
    Adds user_type to differentiate between Job Seekers and Companies.
    """
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('company', 'Company'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')

    # Add related_name to avoid clashes with default User model's groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set", # Changed related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set", # Changed related_name
        related_query_name="user",
    )

    # Set is_active to False by default for email verification
    is_active = models.BooleanField(
        'active',
        default=False, # Changed default to False
        help_text= (
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def __str__(self):
        return self.username

# Profile models

class JobSeekerProfile(models.Model):
    """
    Profile specific to Job Seekers.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='jobseekerprofile')
    # Note: first_name and last_name are on the User model itself
    # full_name = models.CharField(max_length=255, blank=True, null=True) # Consider removing if using User's fields
    city_of_residence = models.CharField("Oraș de reședință", max_length=100, blank=True, null=True) # Renamed from location
    date_of_birth = models.DateField("Data nașterii", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True) # Requires Pillow installation
    bio = models.TextField(blank=True, null=True)
    # Add other relevant fields like experience, education, skills etc. later

    def __str__(self):
        return f"{self.user.username}'s Job Seeker Profile"

class CompanyProfile(models.Model):
    """
    Profile specific to Companies.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='companyprofile')
    company_name = models.CharField("Numele companiei", max_length=255)
    # Address fields
    street_address = models.CharField("Adresă sediu social (stradă, număr...)", max_length=255, blank=True, null=True)
    city = models.CharField("Oraș", max_length=100, blank=True, null=True)
    country = models.CharField("Țară", max_length=100, default="România", blank=True, null=True) # Default to Romania?
    # Other fields
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True) # Requires Pillow installation
    # Corrected ForeignKey to point to SubscriptionPlan
    plan = models.ForeignKey('payments.SubscriptionPlan', on_delete=models.SET_NULL, null=True, blank=True, related_name='companies')
    # Add other relevant fields like industry, company size etc. later

    def __str__(self):
        return f"{self.company_name} ({self.user.username}) Company Profile"

# Signal to create profile automatically when a user is created (we'll add this later)
