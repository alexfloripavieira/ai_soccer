from django.contrib import admin

from .models import Club, FinancialRecord, Revenue


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Admin configuration for Club model."""

    list_display = ['name', 'country', 'city', 'division', 'created_at']
    list_filter = ['division', 'country', 'created_at']
    search_fields = ['name', 'country', 'city']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'country', 'city', 'division')
        }),
        ('Mídia', {
            'fields': ('logo',),
            'classes': ('collapse',)
        }),
        ('Auditoria', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user on creation."""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FinancialRecord)
class FinancialRecordAdmin(admin.ModelAdmin):
    """Admin configuration for FinancialRecord model (10.1.13)."""

    list_display = [
        'record_date',
        'club',
        'transaction_type',
        'category',
        'amount',
        'created_by',
        'created_at'
    ]
    list_filter = [
        'transaction_type',
        'category',
        'record_date',
        'club',
        'created_at'
    ]
    search_fields = [
        'description',
        'club__name',
        'created_by__email'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'record_date'

    fieldsets = (
        ('Informações da Transação', {
            'fields': ('club', 'record_date', 'transaction_type', 'category', 'amount')
        }),
        ('Detalhes', {
            'fields': ('description',)
        }),
        ('Auditoria', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user on creation."""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    """Admin configuration for Revenue model (10.3.16)."""

    list_display = [
        'club',
        'year',
        'month',
        'get_month_name',
        'ticketing',
        'sponsorship',
        'broadcasting',
        'merchandising',
        'get_total_revenue',
        'created_at'
    ]
    list_filter = [
        'year',
        'month',
        'club',
        'created_at'
    ]
    search_fields = [
        'club__name',
        'year'
    ]
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Período', {
            'fields': ('club', 'year', 'month')
        }),
        ('Receitas', {
            'fields': ('ticketing', 'sponsorship', 'broadcasting', 'merchandising')
        }),
        ('Auditoria', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Automatically set created_by to current user on creation."""
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_month_name(self, obj):
        """Display month name in Portuguese for list_display."""
        return obj.get_month_display()
    get_month_name.short_description = 'Mês (Nome)'

    def get_total_revenue(self, obj):
        """Display calculated total revenue for list_display."""
        total = obj.total_revenue()
        return f'R$ {total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    get_total_revenue.short_description = 'Total de Receitas'
