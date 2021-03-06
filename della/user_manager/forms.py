from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator, validate_email
from django.conf import settings

from .models import UserProfile

alphanumericu = RegexValidator(
    regex=r'^[0-9a-zA-Z_]*$',
    message='Only alphanumeric characters and underscore are allowed.')


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, validators=[alphanumericu])
    email = forms.EmailField(max_length=254, required=True)
    invite_code = forms.CharField(max_length=120)

    class Meta:
        model = User
        fields = ['email', 'username', ]

    def clean_invite_code(self):
        error_message = 'Invalid invite code'
        invite_code = self.cleaned_data.get('invite_code')
        if not invite_code == settings.INVITE_CODE:
            raise forms.ValidationError(error_message)
        return invite_code

    def clean_email(self):
        error_message = 'An user with that email already exists'
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
                raise forms.ValidationError(error_message)
        return email


class UserProfileForm(ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile
        exclude = ['is_enabled_exchange', 'user']


class RequestActivationCodeForm(ModelForm):

    class Meta:
        model = User
        fields = ['email']


class MassEmailForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    recipients = forms.CharField(widget=forms.Textarea, required=False)
    for_all_active_users = forms.BooleanField(required=False)
    for_all_enabled_users = forms.BooleanField(required=False)

    def clean_recipients(self):
        recipients = self.cleaned_data.get('recipients')
        if not recipients:
            return recipients
        emails = recipients.split()
        for email in emails:
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError('Enter emails in valid format')
        return emails

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        for_all_active_users = cleaned_data['for_all_active_users']
        for_all_enabled_users = cleaned_data['for_all_enabled_users']
        recipients = cleaned_data['recipients']
        if for_all_active_users and for_all_enabled_users:
            raise forms.ValidationError('You can cannot check both options')
        if recipients and (for_all_active_users or for_all_enabled_users):
            raise forms.ValidationError('Either enter emails or check one box')
        if recipients:
            return cleaned_data
        if for_all_active_users:
            queryset = User.objects.filter(is_active=True)
        else:
            queryset = User.objects.filter(
                userprofile__is_enabled_exchange=True)
        cleaned_data['recipients'] = list(queryset.values_list(
            'email', flat=True))
        return cleaned_data
