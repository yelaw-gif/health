from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.utils.timezone import localtime, now
from .models import Bloodcheck, InjectionSites, Medication, InsulinInjection, InsulinType, Food


class Bloodcheckform(forms.ModelForm):
    class Meta:
        model = Bloodcheck
        fields = ['bloodsugar', 'time', 'date', 'event']

    def __init__(self, *args, **kwargs):
        super(Bloodcheckform, self).__init__(*args, **kwargs)
        self.fields["date"] = JalaliDateField(
            label=('تاریخ'), widget=AdminJalaliDateWidget, initial=localtime(now()).date)
        self.fields["time"] = forms.TimeField(
            input_formats=['%H:%M'],
            widget=forms.TextInput(
                attrs={'class': 'time-input', 'placeholder': 'HH:MM (e.g., 14:30)'})
        )
        self.fields["time"].initial = localtime(now()).strftime('%H:%M')
        self.fields["bloodsugar"].required = False
        self.fields["event"].required = False

    def clean(self):
        cleaned_data = super().clean()
        bloodsugar = cleaned_data.get('bloodsugar')
        event = cleaned_data.get('event')

        if not bloodsugar and not event:
            raise forms.ValidationError("لطفا قند یا رویداد را وارد کنید")
        return cleaned_data


class InsulinFoodForm(forms.Form):
    insulin_type = forms.ChoiceField(
        label="Insulin Type", choices=[], required=False)
    insulin_dose = forms.DecimalField(
        max_digits=4, decimal_places=2, required=False)
    # time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    time = forms.TimeField(
        input_formats=['%H:%M'],
        widget=forms.TextInput(
            attrs={'class': 'time-input', 'placeholder': 'HH:MM (e.g., 14:30)'})
    )
    date = JalaliDateField(
        label='تاریخ',
        widget=AdminJalaliDateWidget,
        initial=localtime(now()).date
    )
    # date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    injection_site = forms.ChoiceField(
        label="Injection Site", choices=[], required=False)
    food = forms.CharField(widget=forms.Textarea, required=False)
    carbs = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Populate insulin_type with user's insulin medications
        medications = Medication.objects.filter(
            user_id=user.id, is_insulin=True, insulin_type__isnull=False)
        self.fields['insulin_type'].choices = [
            (med.insulin_type, med.insulin_type) for med in medications]

        # Populate injection_site with InjectionSites with name 'default'
        injection_sites = InjectionSites.objects.filter(name='default')
        self.fields['injection_site'].choices = [
            (site.sites, site.sites) for site in injection_sites]
        self.fields["time"].initial = localtime(now()).strftime('%H:%M')

    def save(self, user):
        # Save InsulinInjection if insulin_type and dose are provided
        if self.cleaned_data['insulin_type'] and self.cleaned_data['insulin_dose']:
            InsulinInjection.objects.create(
                user=user,
                insulin_type=self.cleaned_data['insulin_type'],
                insulin_dose=self.cleaned_data['insulin_dose'],
                time=self.cleaned_data['time'],
                date=self.cleaned_data['date'],
                injection_site=self.cleaned_data['injection_site'],
            )

        # Save Food if food or carbs are provided
        if self.cleaned_data['food'] or self.cleaned_data['carbs']:
            Food.objects.create(
                user=user,
                food=self.cleaned_data['food'],
                carbs=self.cleaned_data['carbs'],
                time=self.cleaned_data['time'],
                date=self.cleaned_data['date'],
            )
