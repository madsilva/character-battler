from django.contrib import admin
from .models import Character, Matchup, Origin

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    fields = (('name', 'origin', 'bio', 'more_info_url'), ('total_wins', 'total_losses'), 'image')

admin.site.register(Matchup)
admin.site.register(Origin)