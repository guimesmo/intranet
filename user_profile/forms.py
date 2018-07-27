from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from user_profile.models import USER_PROFILE_CHOICES, USER_PROFILE_COMMON
from .models import UserProfile

User = get_user_model()


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


class UserProfileAdminForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'profile_type',
            'full_address', 'city_state',
            'password', 'password_confirmation',
            'upload_volume_limit', 'upload_number_limit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def clean(self):
        password = self.cleaned_data.get('password')
        if password:
            password_confirmation = self.cleaned_data.get('password_confirmation')
            if password != password_confirmation:
                raise forms.ValidationError("As senhas não coincidem")
        print(self.cleaned_data)
        return self.cleaned_data

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exclude(userprofile__id=self.instance.id).exists():
            raise forms.ValidationError("Já existe um usuário cadastrado com este email")
        return self.cleaned_data.get('email')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            validate_password(password)
        else:
            if not self.instance.id:
                raise forms.ValidationError("Você precisa definir uma senha")
        return password

    def save(self, commit=True):
        password = self.cleaned_data.pop("password")
        self.cleaned_data.pop("password_confirmation")
        first_name = self.cleaned_data.pop("first_name")
        last_name = self.cleaned_data.pop("last_name")
        email = self.cleaned_data.pop("email")

        staff_group = Group.objects.filter(name="FUNCIONARIO")
        managers_group = Group.objects.filter(name="GESTOR")
        target_groups = staff_group if self.cleaned_data['profile_type'] == USER_PROFILE_COMMON else managers_group

        if not self.instance.id:
            user = User.objects.create(username=email,
                                       email=email,
                                       first_name=first_name,
                                       last_name=last_name,
                                       )
            user.set_password(password)
            user.groups.set(target_groups)

            instance = super().save(commit=False)
            instance.user = user
            instance.save()
        else:
            instance = super().save(commit=commit)
            if password:
                instance.user.set_password(password)
            instance.user.username = email
            instance.user.email = email
            instance.user.first_name = first_name
            instance.user.last_name = last_name
            if commit:
                instance.user.save()
                instance.user.groups.set(target_groups)

        return instance
