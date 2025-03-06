from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
    )
    phone_number = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={"placeholder": "9360043104"})
    )
    password1 = forms.CharField(
        label="رمز",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password"})
    )
    password2 = forms.CharField(
        label="تکرار رمز",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Re-enter your password"})
    )
    is_doctor = forms.BooleanField(
        required=False,  # Checkbox should be optional
        widget=forms.CheckboxInput(),  # Ensures it renders as a checkbox
        label="دکتر هستید؟"  # Optional: Custom label
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number',
                  'is_doctor', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number']


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = None
