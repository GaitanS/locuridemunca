from django import forms
from .models import Job, Category, JobReport # Added JobReport
from django_countries.widgets import CountrySelectWidget

class JobForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        required=True,
        label="Categorie"
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ex: Inginer Software Senior', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Titlu Job"
    )
    # New description fields
    ideal_candidate = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descrieți candidatul ideal, cerințe specifice...', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Candidatul Ideal",
        required=True,
        error_messages={'required': 'Vă rugăm să descrieți candidatul ideal.'}
    )
    what_we_offer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Descrieți oferta, beneficii, program...', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Ce oferim?",
        required=True,
        error_messages={'required': 'Vă rugăm să descrieți ce oferiți.'}
    )
    responsibilities = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 8, 'placeholder': 'Descrieți responsabilitățile principale ale postului...', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Descrierea jobului / Responsabilități",
        required=True, # Make main description required
        error_messages={'required': 'Vă rugăm să completați descrierea jobului sau responsabilitățile.'}
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ex: București', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Oraș"
    )
    job_type = forms.ChoiceField(
        choices=Job.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Tip Job"
    )
    # New fields
    experience_level = forms.ChoiceField(
        choices=Job.EXPERIENCE_LEVEL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Nivel Experiență"
    )
    positions_available = forms.IntegerField(
        min_value=1,
        initial=1,
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': '1', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Număr Poziții Deschise"
    )
    salary_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 5000', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Salariu Minim (Opțional)"
    )
    salary_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Ex: 8000', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Salariu Maxim (Opțional)"
    )
    salary_currency = forms.ChoiceField(
        choices=Job.CURRENCY_CHOICES,
        initial='RON',
        required=True,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Valută Salariu"
    )

    class Meta:
        model = Job
        # Updated fields list
        fields = [
            'title', 'category', 'country', 'city', 'job_type', 'experience_level',
            'positions_available', 'salary_min', 'salary_max', 'salary_currency',
            'ideal_candidate', 'what_we_offer', 'responsibilities'
        ]
        labels = {
            'country': 'Țară',
            'city': 'Oraș',
        }
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }

class JobReportForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Vă rugăm descrieți motivul raportării...'}),
        label="Motivul Raportării",
        required=True,
        error_messages={'required': "Vă rugăm specificați motivul raportării."}
    )
