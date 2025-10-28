"""Forms for the accounts app."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    """Signup form using the custom user model."""

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nome'
        self.fields['first_name'].widget.attrs.update(
            {
                'placeholder': 'Nome',
                'autocomplete': 'given-name',
            }
        )
        self.fields['last_name'].label = 'Sobrenome'
        self.fields['last_name'].widget.attrs.update(
            {
                'placeholder': 'Sobrenome',
                'autocomplete': 'family-name',
            }
        )
        self.fields['email'].label = 'E-mail'
        self.fields['email'].widget = forms.EmailInput(
            attrs={
                'placeholder': 'E-mail corporativo',
                'autocomplete': 'email',
            }
        )
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].help_text = 'Use ao menos 8 caracteres com letras e números.'
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Senha segura',
                'autocomplete': 'new-password',
            }
        )
        self.fields['password2'].label = 'Confirmar senha'
        self.fields['password2'].help_text = 'Repita a senha para confirmar.'
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Confirme a senha',
                'autocomplete': 'new-password',
            }
        )

        base_classes = (
            'block w-full rounded-xl border border-slate-700 bg-slate-900/80 '
            'px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-green-400 '
            'focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 '
            'focus:ring-offset-slate-950 transition-all duration-150'
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', base_classes)


class CustomAuthenticationForm(AuthenticationForm):
    """Authentication form that accepts email login."""

    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail corporativo',
                'autocomplete': 'email',
            }
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['password'].label = 'Senha'
        self.fields['password'].widget.attrs.update(
            {
                'placeholder': 'Digite sua senha',
                'autocomplete': 'current-password',
            }
        )

        base_classes = (
            'block w-full rounded-xl border border-slate-700 bg-slate-900/80 '
            'px-4 py-3 text-slate-100 placeholder-slate-500 focus:border-blue-400 '
            'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 '
            'focus:ring-offset-slate-950 transition-all duration-150'
        )
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', base_classes)
