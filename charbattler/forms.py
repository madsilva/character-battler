from django import forms

from .models import Origin

class CustomBattleForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Origin.objects.all())