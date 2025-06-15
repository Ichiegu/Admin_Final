from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Staff


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username',
        'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
        'autocomplete': 'current-password'
    }))
    remember_me = forms.BooleanField(required=False, initial=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower().strip()
        return username


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()  # Force lowercase

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()  # Ensure lowercase in DB
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(user=user)
        return user


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['name', 'employee_id', 'position', 'department', 'email', 'phone', 'image', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter staff name'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee ID'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter position'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }