from django.contrib import admin

from scouting.models import ScoutedPlayer


@admin.register(ScoutedPlayer)
class ScoutedPlayerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'position',
        'current_club',
        'status',
        'market_value',
        'created_by',
        'created_at',
    )
    list_filter = ('position', 'status', 'created_by')
    search_fields = ('name', 'current_club', 'nationality')
    autocomplete_fields = ('created_by',)
    readonly_fields = ('created_at', 'updated_at')
