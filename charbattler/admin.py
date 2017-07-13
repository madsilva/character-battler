from django.contrib import admin
from .models import Character, Matchup

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    fields = (('name', 'bio'), ('total_wins', 'total_losses'), 'image')

admin.site.register(Matchup)