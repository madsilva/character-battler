from django import forms

from .models import Origin


class CustomBattleForm(forms.Form):
    include_same_origin_matchups = forms.BooleanField(required=False)


class OriginOptionsForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Origin.objects.all())