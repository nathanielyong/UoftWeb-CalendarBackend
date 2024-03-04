from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=120, required=True, error_messages={
                               'required': 'This field is required'})
    email = forms.CharField(max_length=120, required=False)
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    password1 = forms.CharField(
        max_length=120, required=True, widget=forms.PasswordInput, error_messages={'required': 'This field is required'})
    password2 = forms.CharField(
        max_length=120, required=True, widget=forms.PasswordInput, error_messages={'required': 'This field is required'})

    def clean(self):
        cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if email:
            try:
                validate_email(email)
            except:
                raise forms.ValidationError('Enter a valid email address')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'A user with that username already exists')
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "This password is too short. It must contain at least 8 characters")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, required=False)
    password = forms.CharField(
        max_length=120, widget=forms.PasswordInput, required=False)


class ProfileEditForm(forms.Form):
    email = forms.CharField(max_length=120, required=False)
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    password1 = forms.CharField(
        max_length=120, required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(
        max_length=120, required=False, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if email:
            try:
                validate_email(email)
            except:
                raise forms.ValidationError('Enter a valid email address')
        if password1 and len(password1) < 8:
            raise forms.ValidationError(
                "This password is too short. It must contain at least 8 characters")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match")

        return cleaned_data
