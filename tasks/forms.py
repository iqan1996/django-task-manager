from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter task title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter task description",
                "rows": 4,
            }),
            "status": forms.Select(attrs={
                "class": "form-select",
            }),
        }


class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
        })
    )