from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Character, Matchup, Origin

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ['total_losses']

    # override
    def clean(self):
        cleaned_data = super().clean()
        bio = cleaned_data.get('bio')
        more_info_url = cleaned_data.get('more_info_url')
        if not bio and not more_info_url:
            raise ValidationError('Character must have bio and/or info link.')
        return cleaned_data


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    form = CharacterForm

admin.site.register(Matchup)
admin.site.register(Origin)