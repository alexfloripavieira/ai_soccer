from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ScoutedPlayer(models.Model):
    """Represent a player identified by the scouting team."""

    POSITION_GOALKEEPER = 'GK'
    POSITION_RIGHT_BACK = 'RB'
    POSITION_LEFT_BACK = 'LB'
    POSITION_CENTER_BACK = 'CB'
    POSITION_DEFENSIVE_MIDFIELDER = 'DM'
    POSITION_CENTRAL_MIDFIELDER = 'CM'
    POSITION_ATT_MIDFIELDER = 'AM'
    POSITION_RIGHT_WINGER = 'RW'
    POSITION_LEFT_WINGER = 'LW'
    POSITION_STRIKER = 'ST'

    POSITION_CHOICES = [
        (POSITION_GOALKEEPER, 'Goleiro'),
        (POSITION_RIGHT_BACK, 'Lateral direito'),
        (POSITION_LEFT_BACK, 'Lateral esquerdo'),
        (POSITION_CENTER_BACK, 'Zagueiro'),
        (POSITION_DEFENSIVE_MIDFIELDER, 'Volante'),
        (POSITION_CENTRAL_MIDFIELDER, 'Meia central'),
        (POSITION_ATT_MIDFIELDER, 'Meia ofensivo'),
        (POSITION_RIGHT_WINGER, 'Ponta direita'),
        (POSITION_LEFT_WINGER, 'Ponta esquerda'),
        (POSITION_STRIKER, 'Atacante'),
    ]

    STATUS_MONITORING = 'MONITORING'
    STATUS_INTERESTED = 'INTERESTED'
    STATUS_NEGOTIATING = 'NEGOTIATING'

    STATUS_CHOICES = [
        (STATUS_MONITORING, 'Monitorando'),
        (STATUS_INTERESTED, 'Interessado'),
        (STATUS_NEGOTIATING, 'Negociando'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scouted_players',
        verbose_name='Criado por',
    )
    name = models.CharField('Nome', max_length=200)
    birth_date = models.DateField('Data de nascimento')
    nationality = models.CharField('Nacionalidade', max_length=100)
    position = models.CharField(
        'Posição',
        max_length=2,
        choices=POSITION_CHOICES,
    )
    current_club = models.CharField('Clube atual', max_length=150, blank=True)
    market_value = models.DecimalField(
        'Valor de mercado',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField(
        'Status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_MONITORING,
    )
    notes = models.TextField('Observações', blank=True)
    photo = models.ImageField(
        'Foto',
        upload_to='scouting/players/',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Jogador observado'
        verbose_name_plural = 'Jogadores observados'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def age(self):
        """Return player age in full years."""
        today = date.today()
        has_had_birthday = (today.month, today.day) >= (
            self.birth_date.month,
            self.birth_date.day,
        )
        return today.year - self.birth_date.year - (0 if has_had_birthday else 1)

    def status_badge_class(self):
        """Return Tailwind classes used to style the status badge in templates."""
        mapping = {
            self.STATUS_MONITORING: 'border-blue-400/40 bg-blue-500/15 text-blue-200',
            self.STATUS_INTERESTED: 'border-amber-400/40 bg-amber-500/15 text-amber-200',
            self.STATUS_NEGOTIATING: 'border-green-400/40 bg-green-500/15 text-green-200',
        }
        return mapping.get(self.status, 'border-slate-700 bg-slate-800 text-slate-200')


class ScoutingReport(models.Model):
    """Store a detailed scouting report for a player."""

    player = models.ForeignKey(
        ScoutedPlayer,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Jogador observado',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scouting_reports',
        verbose_name='Observador',
    )
    report_date = models.DateField('Data do relatório')
    match_or_event = models.CharField('Partida ou evento observado', max_length=200)
    technical_score = models.IntegerField(
        'Avaliação técnica',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    physical_score = models.IntegerField(
        'Avaliação física',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    tactical_score = models.IntegerField(
        'Avaliação tática',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    mental_score = models.IntegerField(
        'Avaliação mental',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    potential_score = models.IntegerField(
        'Potencial',
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    strengths = models.TextField('Pontos fortes')
    weaknesses = models.TextField('Pontos a desenvolver')
    recommendation = models.TextField('Recomendação final')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Relatório de scouting'
        verbose_name_plural = 'Relatórios de scouting'
        ordering = ['-report_date', '-created_at']

    def __str__(self):
        return f'Relatório de {self.player.name} ({self.report_date:%d/%m/%Y})'

    def overall_score(self):
        """Return average score considering all evaluation metrics."""
        scores = [
            self.technical_score,
            self.physical_score,
            self.tactical_score,
            self.mental_score,
            self.potential_score,
        ]
        return sum(scores) / len(scores)
