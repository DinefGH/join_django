from django import forms
from .models import Contact




class ContactForm(forms.ModelForm):
    """
ContactForm:

A ModelForm that facilitates the creation and editing of Contact instances, 
allowing users to input and validate data for the fields: name, email, phone, and color.
"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'color'] 