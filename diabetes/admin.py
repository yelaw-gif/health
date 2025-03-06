from django.contrib import admin
from .models import InsulinType, InjectionSites, Medication


@admin.register(InsulinType)
class InsulinTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(InjectionSites)
class InjectionSitesAdmin(admin.ModelAdmin):
    list_display = ['name', 'sites']
    search_fields = ['name', 'sites']


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'is_insulin', 'insulin_type', 'is_pill']
    search_fields = ['user', 'name', 'is_insulin', 'insulin_type', 'is_pill']
