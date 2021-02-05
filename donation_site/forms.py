from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from donation_site.models import Post, Donation

class CreateUserForm(UserCreationForm):
    """defining the CreateUserForm."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CreatePostForm(forms.ModelForm):
    """docstring for CreatePostForm."""
    class Meta:
        model = Post
        fields = ['author', 'title', 'image', 'description', 'date']
        widgets = {
            'author': forms.TextInput(attrs={'class': '', 'type': 'hidden'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'type': 'date'}),
        }

class CreateDonationForm(forms.ModelForm):
    """docstring for CreateDonationForm."""
    class Meta:
        model = Donation
        fields = ['name', 'amount', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name...'}),
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'If you want to send us any message'}),
        }
