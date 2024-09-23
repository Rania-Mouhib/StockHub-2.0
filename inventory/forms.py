from django import forms
from .models import Type, Model

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['name', 'type']
        widgets = {
            'type': forms.Select()  # This creates a dropdown for the type field
        }
