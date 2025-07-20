from django import forms
from .models import NewsletterSubscription, ContactMessage # Import models

# Common Romanian error messages (can be shared or defined per form)
error_messages_ro = {
    'required': "Acest câmp este obligatoriu.",
    'invalid_email': "Introduceți o adresă de email validă.",
}

class NewsletterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Adresa ta de email', 'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        label="", # Hide the default label
        error_messages={'required': error_messages_ro['required'], 'unique': "Această adresă de email este deja abonată."}
    )

    class Meta:
        model = NewsletterSubscription
        fields = ['email']

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        label="Nume complet",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'title': 'Vă rugăm să completați numele complet',
            'oninvalid': "this.setCustomValidity('Vă rugăm să completați numele complet')",
            'oninput': "this.setCustomValidity('')"
        }),
        error_messages={'required': error_messages_ro['required']}
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'title': 'Vă rugăm să introduceți o adresă de email validă',
            'oninvalid': "this.setCustomValidity('Vă rugăm să introduceți o adresă de email validă')",
            'oninput': "this.setCustomValidity('')"
        }),
        error_messages={'required': error_messages_ro['required'], 'invalid': error_messages_ro['invalid_email']}
    )
    subject = forms.CharField(
        max_length=200,
        label="Subiect",
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'title': 'Vă rugăm să completați subiectul mesajului',
            'oninvalid': "this.setCustomValidity('Vă rugăm să completați subiectul mesajului')",
            'oninput': "this.setCustomValidity('')"
        }),
        error_messages={'required': error_messages_ro['required']}
    )
    message = forms.CharField(
        label="Mesaj",
        widget=forms.Textarea(attrs={
            'rows': 4, 
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'title': 'Vă rugăm să scrieți mesajul dumneavoastră',
            'oninvalid': "this.setCustomValidity('Vă rugăm să scrieți mesajul dumneavoastră')",
            'oninput': "this.setCustomValidity('')"
        }),
        error_messages={'required': error_messages_ro['required']}
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
