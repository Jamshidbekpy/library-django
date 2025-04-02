from django import forms
from .models import Contact, Subscribe

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        
        
class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'
