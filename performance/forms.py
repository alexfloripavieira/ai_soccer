from datetime import date
from decimal import Decimal

from django import forms

from .models import Athlete, InjuryRecord, TrainingLoad


class AthleteForm(forms.ModelForm):
    """Form used to create and edit athletes."""

    class Meta:
        model = Athlete
        fields = [
            'name',
            'birth_date',
            'position',
            'nationality',
            'height',
            'weight',
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'position': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'height': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '0.1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'weight': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '0.1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg '
            'text-slate-100 placeholder-slate-400 focus:outline-none '
            'focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', base_class)
            field.widget.attrs.setdefault('placeholder', field.label)

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > date.today():
            raise forms.ValidationError('Data de nascimento não pode estar no futuro.')
        return birth_date

    def clean_height(self):
        height = self.cleaned_data['height']
        if height is not None and height <= 0:
            raise forms.ValidationError('Altura deve ser maior que zero.')
        return height

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight is not None and weight <= 0:
            raise forms.ValidationError('Peso deve ser maior que zero.')
        return weight


class TrainingLoadForm(forms.ModelForm):
    """Form used to create and edit training loads."""

    PERIOD_CHOICES = [
        ('', 'Selecione um período'),
        ('last_7_days', 'Últimos 7 dias'),
        ('last_30_days', 'Últimos 30 dias'),
        ('last_90_days', 'Últimos 90 dias'),
    ]

    class Meta:
        model = TrainingLoad
        fields = [
            'athlete',
            'training_date',
            'duration_minutes',
            'distance_km',
            'heart_rate_avg',
            'heart_rate_max',
            'intensity_level',
        ]
        widgets = {
            'training_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'duration_minutes': forms.NumberInput(
                attrs={
                    'min': '1',
                    'step': '1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'distance_km': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '0.1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'heart_rate_avg': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'heart_rate_max': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '1',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'intensity_level': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
        }
        help_texts = {
            'distance_km': 'Informe a distância percorrida em quilômetros.',
            'duration_minutes': 'Tempo total de treino em minutos.',
            'heart_rate_avg': 'Opcional. Frequência cardíaca média registrada.',
            'heart_rate_max': 'Opcional. Frequência cardíaca máxima registrada.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg '
            'text-slate-100 placeholder-slate-400 focus:outline-none '
            'focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', base_class)
            field.widget.attrs.setdefault('placeholder', field.label)

    def clean_training_date(self):
        training_date = self.cleaned_data['training_date']
        if training_date > date.today():
            raise forms.ValidationError('Data do treino não pode estar no futuro.')
        return training_date

    def clean_distance_km(self):
        distance = self.cleaned_data['distance_km']
        if distance is not None and distance < Decimal('0'):
            raise forms.ValidationError('Distância deve ser maior ou igual a zero.')
        return distance

    def clean(self):
        cleaned_data = super().clean()
        heart_rate_avg = cleaned_data.get('heart_rate_avg')
        heart_rate_max = cleaned_data.get('heart_rate_max')

        if heart_rate_avg is not None and heart_rate_max is not None:
            if heart_rate_avg > heart_rate_max:
                self.add_error(
                    'heart_rate_avg',
                    'FC média não pode ser maior que a FC máxima.',
                )
        return cleaned_data


class InjuryRecordForm(forms.ModelForm):
    """Form used to register and update athlete injuries."""

    class Meta:
        model = InjuryRecord
        fields = [
            'athlete',
            'injury_date',
            'injury_type',
            'body_part',
            'severity_level',
            'description',
            'expected_return',
            'actual_return',
        ]
        widgets = {
            'injury_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'expected_return': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'actual_return': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'injury_type': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'body_part': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'severity_level': forms.Select(
                attrs={
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-green-500',
                    'placeholder': 'Detalhes adicionais sobre a lesão (opcional)',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = (
            'w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg '
            'text-slate-100 placeholder-slate-400 focus:outline-none '
            'focus:ring-2 focus:ring-green-500 focus:border-transparent'
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', base_class)
            field.widget.attrs.setdefault('placeholder', field.label)

    def clean_injury_date(self):
        injury_date = self.cleaned_data['injury_date']
        if injury_date > date.today():
            raise forms.ValidationError('Data da lesão não pode estar no futuro.')
        return injury_date

    def clean(self):
        cleaned_data = super().clean()
        injury_date = cleaned_data.get('injury_date')
        expected_return = cleaned_data.get('expected_return')
        actual_return = cleaned_data.get('actual_return')

        if injury_date and expected_return and expected_return < injury_date:
            self.add_error('expected_return', 'Retorno previsto deve ser após a data da lesão.')

        if injury_date and actual_return and actual_return < injury_date:
            self.add_error('actual_return', 'Retorno real deve ser após a data da lesão.')

        if expected_return and actual_return and actual_return < expected_return:
            self.add_error('actual_return', 'Retorno real não pode ser anterior ao retorno previsto.')

        return cleaned_data
