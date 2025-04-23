from django import forms
from .models import Job, Category
# No need to import CountryField form field explicitly here
from django_countries.widgets import CountrySelectWidget # Import the widget if needed for Meta

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
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Descrieți responsabilitățile, cerințele, beneficiile...', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Descriere Job"
    )
    # Removed explicit country definition - ModelForm handles it
    city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ex: București', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Oraș"
    )
    job_type = forms.ChoiceField(
        choices=Job.JOB_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Tip Job"
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
    salary_currency = forms.CharField(
        initial='RON',
        required=False, # Make optional if default is RON
        widget=forms.TextInput(attrs={'placeholder': 'RON', 'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="Valută Salariu (Opțional)"
    )

    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'country', 'city', 'job_type', # country is now handled by ModelForm
            'salary_min', 'salary_max', 'salary_currency'
        ]
        labels = {
            'country': 'Țară', # Set label here
            'city': 'Oraș', # Ensure city label is correct
        }
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        }
        # Exclude 'company', 'is_published', 'is_featured' as they will be handled in the view or later
