from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.Form):
    REGIONS = [
        ('', 'Select Region'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('AU', 'Oceania'),
        ('AF', 'Africa'),
        ('PH', 'Local (PH)'),
    ]

    GENDERS = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SCHOOL_DOMAIN = '@firstasia.edu.ph'

    username = forms.CharField(label='Username', max_length=100, min_length=5,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=35, min_length=5,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password',
                                max_length=50, min_length=5,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    region = forms.ChoiceField(label='Region', choices=REGIONS, widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDERS, widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_region(self):
        region = self.cleaned_data['region']
        if region == '':
            raise forms.ValidationError('Please select a region.')
        return region

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender == '':
            raise forms.ValidationError('Please select a gender.')
        return gender