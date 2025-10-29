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

# Create your models here.
