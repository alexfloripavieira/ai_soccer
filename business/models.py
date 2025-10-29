from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Club(models.Model):
    """
    Represents a football/soccer club in the business domain.
    Stores basic information about clubs for financial tracking and athlete valuation.
    """

    # Division choices (9.1.5)
    DIVISION_CHOICES = [
        ('PRIMEIRA', 'Primeira Divisão'),
        ('SEGUNDA', 'Segunda Divisão'),
        ('TERCEIRA', 'Terceira Divisão'),
        ('QUARTA', 'Quarta Divisão'),
        ('OUTRA', 'Outra'),
    ]

    # Relational fields first (9.1.8)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Criado por',
        related_name='clubs'
    )

    # Main fields (9.1.2, 9.1.3, 9.1.4, 9.1.5, 9.1.6)
    name = models.CharField(
        'Nome',
        max_length=200,
        unique=True,
        help_text='Nome do clube'
    )
    country = models.CharField(
        'País',
        max_length=100,
        help_text='País onde o clube está localizado'
    )
    city = models.CharField(
        'Cidade',
        max_length=100,
        help_text='Cidade sede do clube'
    )
    division = models.CharField(
        'Divisão',
        max_length=20,
        choices=DIVISION_CHOICES,
        default='PRIMEIRA',
        help_text='Divisão em que o clube compete'
    )
    logo = models.ImageField(
        'Logo',
        upload_to='clubs/logos/',
        blank=True,
        null=True,
        help_text='Logo do clube (opcional)'
    )

    # Audit fields LAST (9.1.7 - MANDATORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Clube'
        verbose_name_plural = 'Clubes'
        ordering = ['-created_at']

    def __str__(self):
        """String representation showing club name and country (9.1.9)"""
        return f'{self.name} ({self.country})'


class FinancialRecord(models.Model):
    """
    Represents a financial transaction (revenue or expense) for a club.
    Tracks all financial activities with categorization and audit trail.
    """

    # Category choices (10.1.4)
    CATEGORY_CHOICES = [
        ('SALARIOS', 'Salários'),
        ('TRANSFERENCIAS', 'Transferências'),
        ('INFRAESTRUTURA', 'Infraestrutura'),
        ('MARKETING', 'Marketing'),
        ('OUTROS', 'Outros'),
    ]

    # Transaction type choices (10.1.6)
    TRANSACTION_TYPE_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]

    # Relational fields first (10.1.2, 10.1.9)
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        verbose_name='Clube',
        related_name='financial_records',
        help_text='Clube relacionado ao registro financeiro'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Criado por',
        related_name='financial_records'
    )

    # Main fields
    record_date = models.DateField(
        'Data do Registro',
        help_text='Data em que a transação ocorreu'
    )
    category = models.CharField(
        'Categoria',
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text='Categoria do registro financeiro'
    )
    amount = models.DecimalField(
        'Valor',
        max_digits=12,
        decimal_places=2,
        help_text='Valor da transação em reais (deve ser maior que 0)'
    )
    transaction_type = models.CharField(
        'Tipo de Transação',
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        help_text='Tipo de transação: receita ou despesa'
    )
    description = models.TextField(
        'Descrição',
        help_text='Descrição detalhada do registro financeiro'
    )

    # Audit fields LAST (10.1.8 - MANDATORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registro Financeiro'
        verbose_name_plural = 'Registros Financeiros'
        ordering = ['-record_date']

    def __str__(self):
        """String representation showing transaction type, category, amount and date (10.1.10)"""
        return f'{self.get_transaction_type_display()} - {self.get_category_display()}: R$ {self.amount} ({self.record_date})'

    def clean(self):
        """Validate that amount is greater than 0"""
        from django.core.exceptions import ValidationError

        if self.amount is not None and self.amount <= 0:
            raise ValidationError({
                'amount': 'O valor deve ser maior que zero.'
            })


class Revenue(models.Model):
    """
    Represents monthly revenue breakdown for a club.
    Tracks different revenue streams (ticketing, sponsorship, broadcasting, merchandising)
    with unique constraint to prevent duplicate entries for the same club/year/month.
    """

    # Month names mapping for get_month_display() (10.3.10)
    MONTH_NAMES = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro',
    }

    # Relational fields first (10.3.2, 10.3.12)
    club = models.ForeignKey(
        Club,
        on_delete=models.CASCADE,
        verbose_name='Clube',
        related_name='revenues',
        help_text='Clube relacionado às receitas'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Criado por',
        related_name='revenues'
    )

    # Main fields (10.3.3 to 10.3.8)
    year = models.IntegerField(
        'Ano',
        validators=[
            MinValueValidator(2000, message='O ano deve ser maior ou igual a 2000.'),
            MaxValueValidator(2100, message='O ano deve ser menor ou igual a 2100.')
        ],
        help_text='Ano da receita (entre 2000 e 2100)'
    )
    month = models.IntegerField(
        'Mês',
        validators=[
            MinValueValidator(1, message='O mês deve estar entre 1 e 12.'),
            MaxValueValidator(12, message='O mês deve estar entre 1 e 12.')
        ],
        help_text='Mês da receita (1-12)'
    )
    ticketing = models.DecimalField(
        'Bilheteria',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0, message='A bilheteria não pode ser negativa.')],
        help_text='Receita de venda de ingressos'
    )
    sponsorship = models.DecimalField(
        'Patrocínio',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0, message='O patrocínio não pode ser negativo.')],
        help_text='Receita de contratos de patrocínio'
    )
    broadcasting = models.DecimalField(
        'Direitos de Transmissão',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0, message='Os direitos de transmissão não podem ser negativos.')],
        help_text='Receita de direitos de transmissão de jogos'
    )
    merchandising = models.DecimalField(
        'Merchandising',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0, message='O merchandising não pode ser negativo.')],
        help_text='Receita de venda de produtos oficiais'
    )

    # Audit fields LAST (10.3.11 - MANDATORY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Receita Mensal'
        verbose_name_plural = 'Receitas Mensais'
        ordering = ['-year', '-month']
        unique_together = [['club', 'year', 'month']]  # 10.3.14

    def __str__(self):
        """String representation showing club name, month and year (10.3.13)"""
        return f'Receitas {self.club.name} - {self.month}/{self.year}'

    def total_revenue(self):
        """
        Calculate total revenue from all sources (10.3.9)

        Returns:
            Decimal: Sum of ticketing, sponsorship, broadcasting, and merchandising
        """
        return (
            self.ticketing +
            self.sponsorship +
            self.broadcasting +
            self.merchandising
        )

    def get_month_display(self):
        """
        Get month name in Portuguese (10.3.10)

        Returns:
            str: Portuguese month name (e.g., 'Janeiro', 'Fevereiro')
        """
        return self.MONTH_NAMES.get(self.month, f'Mês {self.month}')

    def clean(self):
        """Validate revenue fields are non-negative"""
        from django.core.exceptions import ValidationError

        errors = {}

        if self.ticketing is not None and self.ticketing < 0:
            errors['ticketing'] = 'A bilheteria não pode ser negativa.'

        if self.sponsorship is not None and self.sponsorship < 0:
            errors['sponsorship'] = 'O patrocínio não pode ser negativo.'

        if self.broadcasting is not None and self.broadcasting < 0:
            errors['broadcasting'] = 'Os direitos de transmissão não podem ser negativos.'

        if self.merchandising is not None and self.merchandising < 0:
            errors['merchandising'] = 'O merchandising não pode ser negativo.'

        if errors:
            raise ValidationError(errors)
