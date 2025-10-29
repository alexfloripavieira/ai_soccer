from django.contrib import admin

from .models import Athlete, InjuryRecord, TrainingLoad


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'birth_date', 'nationality', 'created_at']
    list_filter = ['position', 'nationality', 'created_at']
    search_fields = ['name', 'nationality']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['created_by']

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('name', 'birth_date', 'nationality', 'position'),
        }),
        ('Dados Físicos', {
            'fields': ('height', 'weight'),
        }),
        ('Auditoria', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(TrainingLoad)
class TrainingLoadAdmin(admin.ModelAdmin):
    list_display = [
        'athlete',
        'training_date',
        'intensity_level',
        'duration_minutes',
        'distance_km',
        'created_at',
    ]
    list_filter = ['intensity_level', 'training_date']
    search_fields = ['athlete__name']
    date_hierarchy = 'training_date'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['athlete', 'created_by']


@admin.register(InjuryRecord)
class InjuryRecordAdmin(admin.ModelAdmin):
    list_display = [
        'athlete',
        'injury_date',
        'injury_type',
        'body_part',
        'severity_level',
        'expected_return',
        'actual_return',
        'created_at',
    ]
    list_filter = ['injury_type', 'body_part', 'severity_level', 'injury_date']
    search_fields = ['athlete__name', 'description']
    date_hierarchy = 'injury_date'
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['athlete', 'created_by']

    fieldsets = (
        ('Informações da Lesão', {
            'fields': (
                'athlete',
                'injury_date',
                'injury_type',
                'body_part',
                'severity_level',
            ),
        }),
        ('Recuperação', {
            'fields': ('expected_return', 'actual_return'),
        }),
        ('Detalhes Adicionais', {
            'fields': ('description',),
            'classes': ('collapse',),
        }),
        ('Auditoria', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# Register your models here.
