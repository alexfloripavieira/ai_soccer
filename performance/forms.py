from datetime import date

from django import forms

from .models import Athlete


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
