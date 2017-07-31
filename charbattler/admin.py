from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Character, Matchup, Origin


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ['total_wins', 'total_losses', 'total_origin_wins', 'total_origin_losses']

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
    list_display = ('name', 'isHidden', 'obscurity_rating')
    list_editable = ('isHidden', 'obscurity_rating')
    readonly_fields = ('total_wins', 'total_losses')

admin.site.register(Matchup)
admin.site.register(Origin)

from django.contrib.sessions.models import Session
class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)