from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django_countries.fields import CountryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    )
    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry-Level (< 2 ani)'),
        ('mid', 'Mid-Level (2-5 ani)'),
        ('senior', 'Senior-Level (5+ ani)'),
        ('manager', 'Manager / Director'),
        ('intern', 'Intern / Stagiar'),
        ('no_experience', 'Fără experiență'),
    )

    CURRENCY_CHOICES = (
        ('RON', 'RON (Leu Românesc)'),
        ('EUR', 'EUR (Euro)'),
        ('USD', 'USD (Dolar American)'),
        ('GBP', 'GBP (Liră Sterlină)'),
        # Adaugă alte valute după necesități
    )

    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs_posted', limit_choices_to={'user_type': 'company'})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True, blank=True, help_text="Leave blank to auto-generate from title.") # Added unique=True back

    # Replaced description with specific fields
    ideal_candidate = models.TextField("Candidatul Ideal", blank=True, null=True)
    what_we_offer = models.TextField("Ce oferim?", blank=True, null=True)
    responsibilities = models.TextField("Descrierea jobului / Responsabilități", blank=True, null=True) # Renamed from description

    country = CountryField(blank_label='(selectează țara)', default='RO')
    city = models.CharField("Oraș", max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField("Nivel Experiență", max_length=20, choices=EXPERIENCE_LEVEL_CHOICES) # Removed null=True, blank=True
    positions_available = models.PositiveIntegerField("Număr Poziții Deschise", default=1) # Removed null=True, blank=True

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Păstrăm opțional pentru salariu min/max
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Păstrăm opțional pentru salariu min/max
    salary_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='RON') # Removed blank=True, added choices

    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Basic check for uniqueness on initial save (more robust handling might be needed)
            # This won't fix existing duplicates from the migration, only prevent new ones on save.
            original_slug = self.slug
            counter = 1
            while Job.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        company_name = self.company.companyprofile.company_name if hasattr(self.company, 'companyprofile') else self.company.username
        return f"{self.title} at {company_name}"

    def get_absolute_url(self):
        # Use slug in the URL
        return reverse('jobs:job_detail', kwargs={'slug': self.slug})


class Application(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', limit_choices_to={'user_type': 'job_seeker'})
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    cover_letter = models.TextField(blank=True, null=True, help_text="Optional cover letter.")

    class Meta:
        ordering = ['-applied_at']
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"Application by {self.applicant.username} for {self.job.title}"

class JobReport(models.Model):
    REPORT_STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('action_taken', 'Action Taken'),
        ('dismissed', 'Dismissed'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_reports', help_text="User who reported the job (optional)")
    reason = models.TextField(help_text="Reason for reporting the job.")
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True, help_text="Notes from admin review.")

    class Meta:
        ordering = ['-reported_at']

    def __str__(self):
        return f"Report for '{self.job.title}' by {self.reporter.username if self.reporter else 'Anonymous'} on {self.reported_at.strftime('%Y-%m-%d')}"
