from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, CompanyProfile

# Common Romanian error messages
error_messages_ro = {
    'required': "Acest câmp este obligatoriu.",
    'invalid_email': "Introduceți o adresă de email validă.",
    # Add more common messages if needed
}

class JobSeekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ex. Ion'}),
        error_messages={'required': error_messages_ro['required']}
    )
    last_name = forms.CharField(
        max_length=150, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ex. Popescu'}),
        error_messages={'required': error_messages_ro['required']}
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'ex. ion.popescu@email.com'}),
        error_messages={'required': error_messages_ro['required'], 'invalid': error_messages_ro['invalid_email']}
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'ZZ/LL/AAAA'}),
        label="Data nașterii",
        error_messages={'required': error_messages_ro['required'], 'invalid': 'Introduceți o dată validă.'}
    )
    city_of_residence = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ex. București'}),
        label="Oraș de reședință",
        error_messages={'required': error_messages_ro['required']}
    )
    phone_number = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'ex. 0712345678'}),
        label="Număr de telefon"
    )
    cv = forms.FileField(
        required=False,
        label="CV"
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'O scurtă descriere despre tine...'}),
        label="Despre mine / Bio"
    )
    terms_agreement = forms.BooleanField(
        required=True,
        label="Sunt de acord cu",
        error_messages={'required': "Trebuie să fiți de acord cu termenii și condițiile."}
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # Add custom error messages for UserCreationForm fields if needed
        # error_messages = {
        #     'username': {'required': error_messages_ro['required']},
        #     # ...
        # }

    # Override default UserCreationForm error messages if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: Customize password mismatch error
        if 'password2' in self.fields:
            self.fields['password2'].help_text = "" # Remove default help text if desired
            self.error_messages['password_mismatch'] = 'Cele două parole introduse nu se potrivesc.'
        # Customize other UserCreationForm errors here

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'job_seeker'
        # Salvez datele din formular în modelul User
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            # Actualizez profilul existent (creat de semnal)
            try:
                profile = user.jobseekerprofile
                profile.date_of_birth = self.cleaned_data.get('date_of_birth')
                profile.city_of_residence = self.cleaned_data.get('city_of_residence')
                profile.phone_number = self.cleaned_data.get('phone_number')
                profile.cv = self.cleaned_data.get('cv')
                profile.bio = self.cleaned_data.get('bio')
                profile.save()
            except JobSeekerProfile.DoesNotExist:
                # Dacă profilul nu există, îl creez
                JobSeekerProfile.objects.create(
                    user=user,
                    date_of_birth=self.cleaned_data.get('date_of_birth'),
                    city_of_residence=self.cleaned_data.get('city_of_residence'),
                    phone_number=self.cleaned_data.get('phone_number'),
                    cv=self.cleaned_data.get('cv'),
                    bio=self.cleaned_data.get('bio')
                )
        return user

# --- Profile Forms ---

class CompanyProfileForm(forms.ModelForm):
    # Add fields from User model if needed (e.g., email, first/last name)
    # email = forms.EmailField(required=True)

    class Meta:
        model = CompanyProfile
        # Include fields from CompanyProfile that should be editable
        fields = [
            'company_name', 'street_address', 'city', 'country', 'location', 'industry',
            'website', 'description', 'logo'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Numele companiei'}),
            'street_address': forms.TextInput(attrs={'placeholder': 'Strada, numărul...'}),
            'city': forms.TextInput(attrs={'placeholder': 'Oraș'}),
            'country': forms.TextInput(attrs={'placeholder': 'România'}), # Consider CountrySelectWidget if needed
            'website': forms.URLInput(attrs={'placeholder': 'https://exemplu.com'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descrierea companiei...'}),
            'logo': forms.ClearableFileInput(), # Use ClearableFileInput for image uploads
            'location': forms.TextInput(attrs={'placeholder': 'ex. București, Sector 1'}),
            'industry': forms.TextInput(attrs={'placeholder': 'ex. IT, Software'}),
        }
        labels = {
            'company_name': "Numele companiei",
            'street_address': "Adresă sediu social",
            'city': "Oraș",
            'country': "Țară",
            'website': "Website",
            'description': "Descriere companie",
            'logo': "Logo companie",
            'location': "Locație sediu principal",
            'industry': "Industrie",
        }

    # If editing User fields too, you'd need a separate User form or combine logic carefully.

class JobSeekerProfileForm(forms.ModelForm):
    # Fields from User model
    first_name = forms.CharField(required=False, label="Prenume")
    last_name = forms.CharField(required=False, label="Nume")
    email = forms.EmailField(required=True, label="E-mail")

    # Fields from JobSeekerProfile model
    class Meta:
        model = JobSeekerProfile
        fields = [
            'city_of_residence', 'date_of_birth', 'phone_number', 'cv', 'bio'
        ]
        widgets = {
            'city_of_residence': forms.TextInput(attrs={'placeholder': 'Ex: București'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+40...'}),
            'cv': forms.ClearableFileInput(),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Scurtă descriere despre tine...'}),
        }
        labels = {
            'city_of_residence': "Oraș de reședință",
            'date_of_birth': "Data nașterii",
            'phone_number': "Număr de telefon",
            'cv': "CV (.pdf, .doc, .docx)",
            'bio': "Despre mine / Bio",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate User fields from the instance's user
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Save JobSeekerProfile fields
        profile = super().save(commit=commit)
        # Save User fields
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return profile


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={'required': error_messages_ro['required'], 'invalid': error_messages_ro['invalid_email']}
    )
    company_name = forms.CharField(
        required=True, max_length=255, label="Numele companiei",
        widget=forms.TextInput(attrs={'placeholder': 'Numele companiei'}),
        error_messages={'required': error_messages_ro['required']}
    )
    street_address = forms.CharField(
        required=True, max_length=255, label="Adresă sediu social",
        widget=forms.TextInput(attrs={'placeholder': 'Strada, numărul...'}),
        error_messages={'required': error_messages_ro['required']}
    )
    location = forms.CharField(
        required=False, max_length=255, label="Locație sediu principal",
        widget=forms.TextInput(attrs={'placeholder': 'ex. Clădire birouri, etaj, etc.'}),
    )
    industry = forms.CharField(
        required=False, max_length=100, label="Industrie",
        widget=forms.TextInput(attrs={'placeholder': 'ex. IT, Construcții, Retail'}),
    )
    city = forms.CharField(
        required=True, max_length=100, label="Oraș",
        widget=forms.TextInput(attrs={'placeholder': 'Oraș'}),
        error_messages={'required': error_messages_ro['required']}
    )
    country = forms.CharField(
        required=True, max_length=100, initial="România", label="Țară",
        widget=forms.TextInput(attrs={'placeholder': 'România'}),
        error_messages={'required': error_messages_ro['required']}
    )
    website = forms.URLField(
        required=False, label="Website",
        widget=forms.URLInput(attrs={'placeholder': 'https://exemplu.com'}),
    )
    description = forms.CharField(
        required=False, label="Descriere companie",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descrierea companiei...'}),
    )
    logo = forms.ImageField(
        required=False, label="Logo companie",
        widget=forms.ClearableFileInput(),
    )
    terms_agreement = forms.BooleanField(
        required=True,
        label="Sunt de acord cu",
        error_messages={'required': "Trebuie să fiți de acord cu termenii și condițiile."}
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email',)
        # error_messages = {
        #     'username': {'required': error_messages_ro['required']},
        # }

    # Override default UserCreationForm error messages if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ""
            self.error_messages['password_mismatch'] = 'Cele două parole introduse nu se potrivesc.'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        # Salvez email-ul din formular în modelul User
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            # Actualizez profilul existent (creat de semnal)
            try:
                profile = user.companyprofile
                profile.company_name = self.cleaned_data.get('company_name')
                profile.street_address = self.cleaned_data.get('street_address')
                profile.city = self.cleaned_data.get('city')
                profile.country = self.cleaned_data.get('country')
                profile.location = self.cleaned_data.get('location')
                profile.industry = self.cleaned_data.get('industry')
                profile.website = self.cleaned_data.get('website')
                profile.description = self.cleaned_data.get('description')
                profile.logo = self.cleaned_data.get('logo')
                profile.save()
            except CompanyProfile.DoesNotExist:
                # Dacă profilul nu există, îl creez
                CompanyProfile.objects.create(
                    user=user,
                    company_name=self.cleaned_data.get('company_name'),
                    street_address=self.cleaned_data.get('street_address'),
                    city=self.cleaned_data.get('city'),
                    country=self.cleaned_data.get('country'),
                    location=self.cleaned_data.get('location'),
                    industry=self.cleaned_data.get('industry'),
                    website=self.cleaned_data.get('website'),
                    description=self.cleaned_data.get('description'),
                    logo=self.cleaned_data.get('logo')
                )
        return user
