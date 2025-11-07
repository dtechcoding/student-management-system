from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'age', 'branch']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter roll number'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter branch'}),
        }
