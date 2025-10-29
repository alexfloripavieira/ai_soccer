from datetime import date

from django.conf import settings
from django.db import models


class Athlete(models.Model):
    """Store core information about an athlete."""

    POSITION_GOALKEEPER = 'GK'
    POSITION_DEFENDER = 'DF'
    POSITION_MIDFIELDER = 'MF'
    POSITION_FORWARD = 'FW'

    POSITION_CHOICES = [
        (POSITION_GOALKEEPER, 'Goleiro'),
        (POSITION_DEFENDER, 'Defensor'),
        (POSITION_MIDFIELDER, 'Meio-campo'),
        (POSITION_FORWARD, 'Atacante'),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='athletes',
        verbose_name='Criado por',
    )
    name = models.CharField('Nome', max_length=200)
    birth_date = models.DateField('Data de nascimento')
    position = models.CharField(
        'Posição',
        max_length=2,
        choices=POSITION_CHOICES,
    )
    nationality = models.CharField('Nacionalidade', max_length=100)
    height = models.FloatField('Altura (cm)')
    weight = models.FloatField('Peso (kg)')
    market_value = models.DecimalField(
        'Valor de Mercado',
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Valor estimado do atleta em Reais (R$)',
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def age(self):
        """Return athlete age in full years."""
        today = date.today()
        has_had_birthday = (today.month, today.day) >= (
            self.birth_date.month,
            self.birth_date.day,
        )
        return today.year - self.birth_date.year - (0 if has_had_birthday else 1)


class TrainingLoad(models.Model):
    """Training load record associated with an athlete."""

    INTENSITY_LOW = 'LOW'
    INTENSITY_MEDIUM = 'MEDIUM'
    INTENSITY_HIGH = 'HIGH'
    INTENSITY_VERY_HIGH = 'VERY_HIGH'

    INTENSITY_CHOICES = [
        (INTENSITY_LOW, 'Baixa'),
        (INTENSITY_MEDIUM, 'Média'),
        (INTENSITY_HIGH, 'Alta'),
        (INTENSITY_VERY_HIGH, 'Muito Alta'),
    ]

    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
        related_name='training_loads',
        verbose_name='Atleta',
    )
    training_date = models.DateField('Data do treino')
    duration_minutes = models.PositiveIntegerField('Duração (minutos)')
    distance_km = models.DecimalField('Distância (km)', max_digits=6, decimal_places=2)
    heart_rate_avg = models.PositiveIntegerField('FC média', blank=True, null=True)
    heart_rate_max = models.PositiveIntegerField('FC máxima', blank=True, null=True)
    intensity_level = models.CharField(
        'Intensidade',
        max_length=10,
        choices=INTENSITY_CHOICES,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_loads',
        verbose_name='Criado por',
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Carga de treino'
        verbose_name_plural = 'Cargas de treino'
        ordering = ['-training_date', '-created_at']

    def __str__(self):
        return f'{self.athlete.name} - {self.training_date}'

    def fatigue_index(self):
        """Return a simplified fatigue index based on load metrics."""
        return (float(self.distance_km) * self.duration_minutes) / 1000

    def intensity_badge_class(self):
        """Return Tailwind classes for intensity badge styling."""
        mapping = {
            self.INTENSITY_LOW: 'bg-green-500/20 text-green-300 border border-green-400/30',
            self.INTENSITY_MEDIUM: 'bg-blue-500/20 text-blue-300 border border-blue-400/30',
            self.INTENSITY_HIGH: 'bg-amber-500/20 text-amber-300 border border-amber-400/30',
            self.INTENSITY_VERY_HIGH: 'bg-red-500/20 text-red-300 border border-red-400/30',
        }
        return mapping.get(self.intensity_level, 'bg-slate-700 text-slate-200 border border-slate-600/40')


class InjuryRecord(models.Model):
    """Track athlete injury history and recovery timeline."""

    INJURY_MUSCULAR = 'MUSCULAR'
    INJURY_ARTICULAR = 'ARTICULAR'
    INJURY_OSSEOUS = 'OSSEOUS'
    INJURY_LIGAMENT = 'LIGAMENT'
    INJURY_TENDON = 'TENDON'

    INJURY_TYPE_CHOICES = [
        (INJURY_MUSCULAR, 'Muscular'),
        (INJURY_ARTICULAR, 'Articular'),
        (INJURY_OSSEOUS, 'Óssea'),
        (INJURY_LIGAMENT, 'Ligamentar'),
        (INJURY_TENDON, 'Tendínea'),
    ]

    BODY_KNEE = 'KNEE'
    BODY_ANKLE = 'ANKLE'
    BODY_THIGH = 'THIGH'
    BODY_HAMSTRING = 'HAMSTRING'
    BODY_SHOULDER = 'SHOULDER'
    BODY_BACK = 'BACK'

    BODY_PART_CHOICES = [
        (BODY_KNEE, 'Joelho'),
        (BODY_ANKLE, 'Tornozelo'),
        (BODY_THIGH, 'Coxa'),
        (BODY_HAMSTRING, 'Posterior da coxa'),
        (BODY_SHOULDER, 'Ombro'),
        (BODY_BACK, 'Costas'),
    ]

    SEVERITY_MILD = 'LEVE'
    SEVERITY_MODERATE = 'MODERADA'
    SEVERITY_SEVERE = 'GRAVE'

    SEVERITY_LEVEL_CHOICES = [
        (SEVERITY_MILD, 'Leve'),
        (SEVERITY_MODERATE, 'Moderada'),
        (SEVERITY_SEVERE, 'Grave'),
    ]

    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
        related_name='injury_records',
        verbose_name='Atleta',
    )
    injury_date = models.DateField('Data da lesão')
    injury_type = models.CharField(
        'Tipo de lesão',
        max_length=20,
        choices=INJURY_TYPE_CHOICES,
    )
    body_part = models.CharField(
        'Parte do corpo',
        max_length=20,
        choices=BODY_PART_CHOICES,
    )
    severity_level = models.CharField(
        'Gravidade',
        max_length=10,
        choices=SEVERITY_LEVEL_CHOICES,
    )
    description = models.TextField('Descrição', blank=True)
    expected_return = models.DateField('Retorno previsto', blank=True, null=True)
    actual_return = models.DateField('Retorno real', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='injury_records',
        verbose_name='Criado por',
    )

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Registro de lesão'
        verbose_name_plural = 'Registros de lesões'
        ordering = ['-injury_date', '-created_at']

    def __str__(self):
        return f'{self.athlete.name} - {self.injury_date}'

    def days_out(self):
        """Return the number of days the athlete has been sidelined."""
        end_date = self.actual_return or date.today()
        days = (end_date - self.injury_date).days
        return max(days, 0)

    def severity_badge_class(self):
        """Return Tailwind classes for severity badge styling."""
        mapping = {
            self.SEVERITY_SEVERE: 'bg-red-500/20 text-red-300 border border-red-400/40',
            self.SEVERITY_MODERATE: 'bg-amber-500/20 text-amber-300 border border-amber-400/40',
            self.SEVERITY_MILD: 'bg-blue-500/20 text-blue-300 border border-blue-400/40',
        }
        return mapping.get(self.severity_level, 'bg-slate-700 text-slate-200 border border-slate-600/40')

# Create your models here.
