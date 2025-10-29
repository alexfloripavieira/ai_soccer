"""Forms for scouting application."""

from datetime import date
from decimal import Decimal

from django import forms

from scouting.models import ScoutedPlayer


class ScoutedPlayerForm(forms.ModelForm):
    """Form used to create and edit scouted players."""

    ORDER_BY_CHOICES = [
        ('', 'Ordenar por'),
        ('-created_at', 'Mais recentes'),
        ('created_at', 'Mais antigos'),
        ('-market_value', 'Maior valor de mercado'),
        ('market_value', 'Menor valor de mercado'),
        ('name', 'Nome (A-Z)'),
        ('-name', 'Nome (Z-A)'),
    ]

    class Meta:
        model = ScoutedPlayer
        fields = [
            'name',
            'birth_date',
            'nationality',
            'position',
            'current_club',
            'market_value',
            'status',
            'notes',
            'photo',
        ]
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'position': forms.Select(),
            'status': forms.Select(),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'market_value': forms.NumberInput(
                attrs={
                    'min': '0',
                    'step': '0.01',
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
            if field_name == 'photo':
                continue
            field.widget.attrs.setdefault('class', base_class)
            field.widget.attrs.setdefault('placeholder', field.label)
        self.fields['photo'].widget.attrs.update(
            {
                'class': (
                    'w-full text-sm text-slate-200 file:mr-4 file:rounded-lg '
                    'file:border-0 file:bg-gradient-to-r file:from-green-500 '
                    'file:to-blue-500 file:px-4 file:py-2 file:text-sm file:font-semibold '
                    'hover:file:from-green-400 hover:file:to-blue-400'
                ),
                'accept': 'image/*',
            }
        )

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > date.today():
            raise forms.ValidationError('Data de nascimento não pode estar no futuro.')
        return birth_date

    def clean_market_value(self):
        market_value = self.cleaned_data.get('market_value')
        if market_value is None:
            return market_value
        if isinstance(market_value, Decimal) and market_value < 0:
            raise forms.ValidationError('Valor de mercado deve ser positivo.')
        return market_value
