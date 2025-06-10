# impact/admin.py
from django.contrib import admin
from django import forms
from .models import ImpactStats

class ImpactStatsForm(forms.ModelForm):
    class Meta:
        model = ImpactStats
        fields = '__all__'

    def clean_user(self):
        user = self.cleaned_data['user']
        if ImpactStats.objects.filter(user=user).exists() and not self.instance.pk:
            raise forms.ValidationError("This user already has an impact record.")
        return user

@admin.register(ImpactStats)
class ImpactStatsAdmin(admin.ModelAdmin):
    form = ImpactStatsForm
    list_display = ('user', 'carbon_saved_kg', 'trees_planted', 'distance_covered_km')
    search_fields = ('user__username', 'user__email')
    list_filter = ('carbon_saved_kg',)
