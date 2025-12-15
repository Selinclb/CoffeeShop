from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify


class EmailUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Ad", max_length=150, required=True)
    last_name = forms.CharField(label="Soyad", max_length=150, required=True)
    email = forms.EmailField(label="E-posta", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Bu e-posta ile hesap zaten mevcut.")
        return email

    def _generate_username(self, first_name: str, last_name: str) -> str:
        base = slugify(f"{first_name}-{last_name}") or "user"
        candidate = base
        counter = 1

        while User.objects.filter(username__iexact=candidate).exists():
            counter += 1
            candidate = f"{base}-{counter}"

        return candidate

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"].strip()
        user.last_name = self.cleaned_data["last_name"].strip()
        user.email = self.cleaned_data["email"].lower()
        user.username = self._generate_username(user.first_name, user.last_name)

        if commit:
            user.save()
        return user
