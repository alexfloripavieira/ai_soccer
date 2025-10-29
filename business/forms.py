from datetime import date

from django import forms

from business.models import Club, FinancialRecord, Revenue


class ClubForm(forms.ModelForm):
    """
    Form for creating and updating Club instances.
    Includes custom validation and TailwindCSS dark theme styling.
    """

    class Meta:
        model = Club
        fields = ['name', 'country', 'city', 'division', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite o nome do clube'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite o país'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Digite a cidade'
            }),
            'division': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-green-500 file:to-blue-500 file:text-white hover:file:opacity-80 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
        }

    def clean_name(self):
        """Validate club name - ensure it's not empty and strip whitespace."""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('O nome do clube não pode estar vazio.')

        # Check for duplicate names (case-insensitive), excluding current instance if updating
        existing_club = Club.objects.filter(name__iexact=name)
        if self.instance and self.instance.pk:
            existing_club = existing_club.exclude(pk=self.instance.pk)

        if existing_club.exists():
            raise forms.ValidationError('Já existe um clube com este nome.')

        return name

    def clean_country(self):
        """Validate country name - ensure it's not empty and strip whitespace."""
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise forms.ValidationError('O país não pode estar vazio.')
        return country

    def clean_city(self):
        """Validate city name - ensure it's not empty and strip whitespace."""
        city = self.cleaned_data.get('city', '').strip()
        if not city:
            raise forms.ValidationError('A cidade não pode estar vazia.')
        return city

    def clean_logo(self):
        """Validate logo file - check size and format."""
        logo = self.cleaned_data.get('logo')

        if logo:
            # Check file size (max 5MB)
            if logo.size > 5 * 1024 * 1024:
                raise forms.ValidationError('O arquivo da logo não pode ser maior que 5MB.')

            # Check file format
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if logo.content_type not in allowed_types:
                raise forms.ValidationError('Formato de arquivo inválido. Use JPEG, PNG, GIF ou WebP.')

        return logo


class FinancialRecordForm(forms.ModelForm):
    """
    Form for creating and updating FinancialRecord instances.
    Includes custom validations for date and amount, with TailwindCSS dark theme styling.
    """

    class Meta:
        model = FinancialRecord
        fields = ['club', 'record_date', 'category', 'amount', 'transaction_type', 'description']
        widgets = {
            'club': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'record_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': 'Descreva o registro financeiro...',
                'rows': 4
            }),
        }

    def clean_record_date(self):
        """Validate that record_date is not in the future."""
        record_date = self.cleaned_data.get('record_date')

        if record_date and record_date > date.today():
            raise forms.ValidationError('A data do registro não pode ser futura.')

        return record_date

    def clean_amount(self):
        """Validate that amount is greater than 0."""
        amount = self.cleaned_data.get('amount')

        if amount is not None and amount <= 0:
            raise forms.ValidationError('O valor deve ser maior que zero.')

        return amount

    def clean_description(self):
        """Validate description - ensure it's not empty and strip whitespace."""
        description = self.cleaned_data.get('description', '').strip()

        if not description:
            raise forms.ValidationError('A descrição não pode estar vazia.')

        return description


class RevenueForm(forms.ModelForm):
    """
    Form for creating and updating Revenue instances.
    Includes custom validation for year, month, duplicate prevention,
    and non-negative revenue values with TailwindCSS dark theme styling.
    """

    # Month choices with Portuguese names (10.4.2)
    MONTH_CHOICES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro'),
    ]

    month = forms.ChoiceField(
        label='Mês',
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
        })
    )

    class Meta:
        model = Revenue
        fields = ['club', 'year', 'month', 'ticketing', 'sponsorship', 'broadcasting', 'merchandising']
        widgets = {
            'club': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '2025',
                'min': '2000',
                'max': '2100'
            }),
            'ticketing': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'sponsorship': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'broadcasting': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'merchandising': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
        }

    def clean_year(self):
        """Validate that year is between 2000 and 2100 (10.4.3)."""
        year = self.cleaned_data.get('year')

        if year is not None:
            if year < 2000 or year > 2100:
                raise forms.ValidationError('O ano deve estar entre 2000 e 2100.')

        return year

    def clean_month(self):
        """Validate that month is between 1 and 12 (10.4.3)."""
        month = self.cleaned_data.get('month')

        if month:
            month = int(month)
            if month < 1 or month > 12:
                raise forms.ValidationError('O mês deve estar entre 1 e 12.')

        return month

    def clean_ticketing(self):
        """Validate that ticketing is non-negative (10.4.3)."""
        ticketing = self.cleaned_data.get('ticketing')

        if ticketing is not None and ticketing < 0:
            raise forms.ValidationError('A bilheteria não pode ser negativa.')

        return ticketing

    def clean_sponsorship(self):
        """Validate that sponsorship is non-negative (10.4.3)."""
        sponsorship = self.cleaned_data.get('sponsorship')

        if sponsorship is not None and sponsorship < 0:
            raise forms.ValidationError('O patrocínio não pode ser negativo.')

        return sponsorship

    def clean_broadcasting(self):
        """Validate that broadcasting is non-negative (10.4.3)."""
        broadcasting = self.cleaned_data.get('broadcasting')

        if broadcasting is not None and broadcasting < 0:
            raise forms.ValidationError('Os direitos de transmissão não podem ser negativos.')

        return broadcasting

    def clean_merchandising(self):
        """Validate that merchandising is non-negative (10.4.3)."""
        merchandising = self.cleaned_data.get('merchandising')

        if merchandising is not None and merchandising < 0:
            raise forms.ValidationError('O merchandising não pode ser negativo.')

        return merchandising

    def clean(self):
        """
        Validate unique_together constraint (club + year + month).
        Prevent duplicate entries with clear error message (10.4.3).
        """
        cleaned_data = super().clean()
        club = cleaned_data.get('club')
        year = cleaned_data.get('year')
        month = cleaned_data.get('month')

        if club and year and month:
            # Convert month to int if it's a string
            if isinstance(month, str):
                month = int(month)

            # Check for existing revenue with same club, year, month
            existing_revenue = Revenue.objects.filter(
                club=club,
                year=year,
                month=month
            )

            # Exclude current instance when updating
            if self.instance and self.instance.pk:
                existing_revenue = existing_revenue.exclude(pk=self.instance.pk)

            if existing_revenue.exists():
                month_name = dict(self.MONTH_CHOICES).get(month, str(month))
                raise forms.ValidationError(
                    f'Já existe um registro de receita para {club.name} em {month_name}/{year}. '
                    'Cada clube pode ter apenas um registro por mês.'
                )

        return cleaned_data
