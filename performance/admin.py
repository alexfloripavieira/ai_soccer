from django.contrib import admin

from .models import Athlete


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

# Register your models here.
