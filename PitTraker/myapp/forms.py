# PitTraker/myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import LoanedTool, CustomUser


class LoanedToolForm(forms.ModelForm):
    class Meta:
        model = LoanedTool
        fields = ["team_number", "tool_name", "description"]
        widgets = {
            "team_number": forms.TextInput(attrs={"placeholder": "e.g., 1234"}),
            "tool_name": forms.TextInput(
                attrs={"placeholder": "e.g., Socket Wrench Set"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Additional details about the tool (optional)",
                    "rows": 3,
                }
            ),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "form-input"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-input"}
        )
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_admin = forms.BooleanField(
        required=False,
        label="Make this user an admin",
        help_text="Admin users can manage other users and have full access to the system.",
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2", "is_admin")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = self.cleaned_data["is_admin"]
        user.is_superuser = self.cleaned_data["is_admin"]
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    is_admin = forms.BooleanField(
        required=False,
        label="Admin privileges",
        help_text="Admin users can manage other users and have full access to the system.",
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_admin")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["is_admin"].initial = self.instance.is_staff

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data["is_admin"]
        user.is_superuser = self.cleaned_data["is_admin"]
        if commit:
            user.save()
        return user
