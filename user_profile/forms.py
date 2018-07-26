from django import forms
from django.contrib.auth.password_validation import validate_password

from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    password = forms.CharField(required=False, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['full_address', 'city_state', 'password', 'password_confirmation']

    def clean(self):
        password = self.cleaned_data.get('password')
        if password:
            password_confirmation = self.cleaned_data.get('password_confirmation')
            if password != password_confirmation:
                raise forms.ValidationError("As senhas não coincidem")
        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        return password

    def save(self, commit=True):
        password = self.cleaned_data.pop("password")
        self.cleaned_data.pop("password_confirmation")
        instance = super().save(commit=commit)
        if password:
            instance.user.set_password(password)
            instance.user.save()
        return instance

