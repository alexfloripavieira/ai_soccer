from django.contrib import admin

from scouting.models import ScoutedPlayer, ScoutingReport


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


@admin.register(ScoutingReport)
class ScoutingReportAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'report_date',
        'created_by',
        'technical_score',
        'physical_score',
        'tactical_score',
        'mental_score',
        'potential_score',
    )
    list_filter = ('report_date', 'created_by', 'player')
    search_fields = ('player__name', 'match_or_event', 'created_by__email')
    autocomplete_fields = ('player', 'created_by')
    readonly_fields = ('created_at', 'updated_at')
