"""Populate the system with 48 months of realistic data across all modules."""

from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from typing import Dict, List, Sequence, Tuple

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import CustomUser
from business.models import Club, FinancialRecord, Revenue
from performance.models import Athlete, InjuryRecord, TrainingLoad
from scouting.models import ScoutedPlayer, ScoutingReport


MONTHS_REQUIRED = 48
DEFAULT_USER_EMAIL = 'demo@aisoccer.test'
DEFAULT_USER_PASSWORD = 'AiSoccer!2024'


@dataclass(frozen=True)
class MonthWindow:
    """Represent a monthly time window used for data generation."""

    year: int
    month: int
    start: date
    end: date
    index: int


class Command(BaseCommand):
    """Populate the database with realistic historical data."""

    help = (
        'Gera dados históricos realistas para os módulos de Performance, Scouting e Business '
        'cobrindo pelo menos 48 meses consecutivos para habilitar todos os modelos.'
    )

    def handle(self, *args, **options):
        months = list(self._build_month_windows())

        with transaction.atomic():
            user = self._ensure_demo_user()
            clubs = self._ensure_clubs(user)
            athletes = self._ensure_athletes(user)
            scouted_players = self._ensure_scouted_players(user)

            self._generate_performance_data(months, user, athletes)
            self._generate_business_data(months, user, clubs)
            self._generate_scouting_data(months, user, scouted_players)

        self.stdout.write(self.style.SUCCESS(
            'Dados históricos criados/atualizados com sucesso para os módulos Performance, Business e Scouting.'
        ))

    # ------------------------------------------------------------------
    # Helpers for month iteration and coverage checks
    # ------------------------------------------------------------------

    def _build_month_windows(self) -> Iterable[MonthWindow]:
        """Return sequential MonthWindow objects covering the required period."""
        today = date.today()
        start_year, start_month = self._add_months(today.year, today.month, -(MONTHS_REQUIRED - 1))
        current_year, current_month = start_year, start_month

        for index in range(MONTHS_REQUIRED):
            start = date(current_year, current_month, 1)
            last_day = calendar.monthrange(current_year, current_month)[1]
            end = date(current_year, current_month, last_day)
            yield MonthWindow(
                year=current_year,
                month=current_month,
                start=start,
                end=end,
                index=index,
            )
            current_year, current_month = self._add_months(current_year, current_month, 1)

    def _add_months(self, year: int, month: int, delta: int) -> Tuple[int, int]:
        """Return year/month shifted by delta months (delta can be negative)."""
        total = (year * 12 + (month - 1)) + delta
        new_year = total // 12
        new_month = total % 12 + 1
        return new_year, new_month

    # ------------------------------------------------------------------
    # Entity creation helpers
    # ------------------------------------------------------------------

    def _ensure_demo_user(self) -> CustomUser:
        """Return an active superuser used as author for the generated data."""
        user = CustomUser.objects.filter(email=DEFAULT_USER_EMAIL).first()
        if user:
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save(update_fields=['is_staff', 'is_superuser'])
            return user

        user = CustomUser.objects.create_superuser(
            email=DEFAULT_USER_EMAIL,
            password=DEFAULT_USER_PASSWORD,
            first_name='Equipe',
            last_name='Analytics',
        )
        return user

    def _ensure_clubs(self, user: CustomUser) -> List[Club]:
        """Create or retrieve clubs with realistic metadata."""
        clubs_data = [
            ('CR Flamengo', 'Brasil', 'Rio de Janeiro', 'PRIMEIRA'),
            ('SE Palmeiras', 'Brasil', 'São Paulo', 'PRIMEIRA'),
            ('SC Internacional', 'Brasil', 'Porto Alegre', 'PRIMEIRA'),
        ]

        clubs: List[Club] = []
        for name, country, city, division in clubs_data:
            club, created = Club.objects.get_or_create(
                name=name,
                defaults={
                    'country': country,
                    'city': city,
                    'division': division,
                    'created_by': user,
                },
            )
            if created:
                club.country = country
                club.city = city
                club.division = division
                club.created_by = user
                club.save()
            clubs.append(club)
        return clubs

    def _ensure_athletes(self, user: CustomUser) -> List[Athlete]:
        """Create athletes inspired by atletas do cenário brasileiro."""
        athlete_profiles = [
            ('Pedro Guilherme', date(1997, 6, 20), Athlete.POSITION_FORWARD, 'Brasil', 185, 82, '90000000.00'),
            ('Gabriel Barbosa', date(1996, 8, 30), Athlete.POSITION_FORWARD, 'Brasil', 178, 78, '95000000.00'),
            ('Giorgian De Arrascaeta', date(1994, 6, 1), Athlete.POSITION_MIDFIELDER, 'Uruguai', 172, 70, '110000000.00'),
            ('Everton Ribeiro', date(1989, 4, 10), Athlete.POSITION_MIDFIELDER, 'Brasil', 174, 72, '45000000.00'),
            ('David Luiz', date(1987, 4, 22), Athlete.POSITION_DEFENDER, 'Brasil', 189, 87, '30000000.00'),
            ('Filipe Luís', date(1985, 8, 9), Athlete.POSITION_DEFENDER, 'Brasil', 182, 78, '15000000.00'),
            ('Bruno Henrique', date(1990, 12, 30), Athlete.POSITION_FORWARD, 'Brasil', 184, 78, '60000000.00'),
            ('Matheuzinho', date(2000, 9, 8), Athlete.POSITION_DEFENDER, 'Brasil', 175, 70, '32000000.00'),
            ('João Gomes', date(2001, 2, 12), Athlete.POSITION_MIDFIELDER, 'Brasil', 176, 74, '50000000.00'),
            ('Santos Oliveira', date(1990, 3, 17), Athlete.POSITION_GOALKEEPER, 'Brasil', 191, 88, '20000000.00'),
            ('Danilo dos Santos', date(2001, 4, 15), Athlete.POSITION_MIDFIELDER, 'Brasil', 184, 80, '105000000.00'),
            ('Rony Silva', date(1995, 5, 11), Athlete.POSITION_FORWARD, 'Brasil', 169, 66, '70000000.00'),
            ('Raphael Veiga', date(1995, 6, 19), Athlete.POSITION_MIDFIELDER, 'Brasil', 176, 74, '120000000.00'),
            ('Gustavo Gómez', date(1993, 5, 6), Athlete.POSITION_DEFENDER, 'Paraguai', 185, 86, '80000000.00'),
            ('Murilo Cerqueira', date(1997, 4, 27), Athlete.POSITION_DEFENDER, 'Brasil', 188, 83, '52000000.00'),
            ('Weverton Pereira', date(1987, 12, 13), Athlete.POSITION_GOALKEEPER, 'Brasil', 189, 87, '40000000.00'),
            ('Maurício Souza', date(2001, 6, 3), Athlete.POSITION_MIDFIELDER, 'Brasil', 177, 73, '38000000.00'),
            ('Wanderson Maciel', date(1994, 10, 7), Athlete.POSITION_FORWARD, 'Brasil', 181, 75, '45000000.00'),
        ]

        athletes: List[Athlete] = []
        for profile in athlete_profiles:
            (name, birth_date, position, nationality, height, weight, market_value) = profile
            athlete, created = Athlete.objects.get_or_create(
                name=name,
                defaults={
                    'birth_date': birth_date,
                    'position': position,
                    'nationality': nationality,
                    'height': float(height),
                    'weight': float(weight),
                    'market_value': Decimal(market_value),
                    'created_by': user,
                },
            )
            if created:
                athlete.created_by = user
                athlete.save()
            athletes.append(athlete)
        return athletes

    def _ensure_scouted_players(self, user: CustomUser) -> List[ScoutedPlayer]:
        """Create scouted players referenced in scouting reports."""
        scouting_profiles = [
            ('Vitor Roque', date(2005, 2, 28), 'Brasil', ScoutedPlayer.POSITION_STRIKER, 'Athletico Paranaense'),
            ('Endrick Felipe', date(2006, 7, 21), 'Brasil', ScoutedPlayer.POSITION_STRIKER, 'Palmeiras'),
            ('Matheus França', date(2004, 4, 1), 'Brasil', ScoutedPlayer.POSITION_ATT_MIDFIELDER, 'Flamengo'),
            ('Ângelo Gabriel', date(2004, 12, 21), 'Brasil', ScoutedPlayer.POSITION_RIGHT_WINGER, 'Chelsea'),
            ('Andrey Santos', date(2004, 5, 3), 'Brasil', ScoutedPlayer.POSITION_CENTRAL_MIDFIELDER, 'Chelsea'),
            ('Marcos Leonardo', date(2003, 5, 2), 'Brasil', ScoutedPlayer.POSITION_STRIKER, 'Santos'),
            ('Lázaro Vinícius', date(2002, 3, 12), 'Brasil', ScoutedPlayer.POSITION_LEFT_WINGER, 'Flamengo'),
            ('Kaiky Fernandes', date(2004, 1, 12), 'Brasil', ScoutedPlayer.POSITION_CENTER_BACK, 'Santos'),
        ]

        players: List[ScoutedPlayer] = []
        for name, birth_date, nationality, position, club in scouting_profiles:
            player, created = ScoutedPlayer.objects.get_or_create(
                name=name,
                defaults={
                    'birth_date': birth_date,
                    'nationality': nationality,
                    'position': position,
                    'current_club': club,
                    'status': ScoutedPlayer.STATUS_MONITORING,
                    'created_by': user,
                },
            )
            if created:
                player.created_by = user
                player.save()
            players.append(player)
        return players

    # ------------------------------------------------------------------
    # Data generation per module
    # ------------------------------------------------------------------

    def _generate_performance_data(
        self,
        months: Sequence[MonthWindow],
        user: CustomUser,
        athletes: Sequence[Athlete],
    ) -> None:
        """Generate training loads and injury records across the period."""
        today = date.today()
        existing_loads = set(
            TrainingLoad.objects.filter(training_date__gte=months[0].start).values_list('athlete_id', 'training_date')
        )
        existing_injuries = set(
            InjuryRecord.objects.filter(injury_date__gte=months[0].start).values_list('athlete_id', 'injury_date')
        )

        load_instances: List[TrainingLoad] = []
        injury_instances: List[InjuryRecord] = []

        intensity_mapping = {
            Athlete.POSITION_GOALKEEPER: ['LOW', 'MEDIUM', 'MEDIUM'],
            Athlete.POSITION_DEFENDER: ['MEDIUM', 'HIGH', 'HIGH', 'VERY_HIGH'],
            Athlete.POSITION_MIDFIELDER: ['MEDIUM', 'HIGH', 'HIGH', 'VERY_HIGH'],
            Athlete.POSITION_FORWARD: ['MEDIUM', 'HIGH', 'VERY_HIGH'],
        }

        for athlete in athletes:
            for window in months:
                period_end = min(window.end, today)
                if period_end < window.start:
                    continue

                week_start = window.start
                while week_start <= period_end:
                    for offset in (0, 2, 4):
                        session_day = week_start + timedelta(days=offset)
                        if session_day > period_end or session_day.month != window.month:
                            continue
                        key = (athlete.id, session_day)
                        if key in existing_loads:
                            continue

                        duration = 72 + (athlete.id % 9) * 3 + (offset * 3)
                        distance_base = 7.4 + ((athlete.id + offset) % 5) * 0.6
                        if athlete.position == Athlete.POSITION_FORWARD:
                            distance_base += 0.7
                        if athlete.position == Athlete.POSITION_DEFENDER and offset == 4:
                            distance_base += 0.3

                        intensity_options = intensity_mapping.get(athlete.position, ['MEDIUM'])
                        intensity = intensity_options[(window.index + offset) % len(intensity_options)]
                        average_hr = 145 + ((athlete.id + window.index + offset) % 25)
                        max_hr = average_hr + 35

                        load_instances.append(
                            TrainingLoad(
                                athlete=athlete,
                                training_date=session_day,
                                duration_minutes=duration,
                                distance_km=Decimal(str(round(distance_base, 2))),
                                heart_rate_avg=average_hr,
                                heart_rate_max=max_hr,
                                intensity_level=intensity,
                                created_by=user,
                            )
                        )
                    week_start += timedelta(days=7)

                # Injury probability scales with workload and position
                if (window.index % 6 == athlete.id % 6) or (window.index % 11 == 0 and athlete.position != Athlete.POSITION_GOALKEEPER):
                    injury_day = window.start + timedelta(days=min(20, (athlete.id * 2 + window.index * 3) % 27))
                    if injury_day > period_end or (athlete.id, injury_day) in existing_injuries:
                        continue

                    severity_choices = [
                        InjuryRecord.SEVERITY_MILD,
                        InjuryRecord.SEVERITY_MODERATE,
                        InjuryRecord.SEVERITY_SEVERE,
                    ]
                    severity = severity_choices[(athlete.id + window.index) % len(severity_choices)]
                    injury_types = [choice[0] for choice in InjuryRecord.INJURY_TYPE_CHOICES]
                    body_parts = [choice[0] for choice in InjuryRecord.BODY_PART_CHOICES]
                    injury_type = injury_types[(athlete.id + window.index) % len(injury_types)]
                    body_part = body_parts[(athlete.id * 2 + window.index) % len(body_parts)]

                    base_days_out = 12 if severity == InjuryRecord.SEVERITY_MILD else 28 if severity == InjuryRecord.SEVERITY_MODERATE else 52
                    expected_return = injury_day + timedelta(days=base_days_out)
                    actual_return = expected_return + timedelta(days=(athlete.id + window.index) % 10 - 4)
                    if actual_return > today:
                        actual_return = None

                    injury_instances.append(
                        InjuryRecord(
                            athlete=athlete,
                            injury_date=injury_day,
                            injury_type=injury_type,
                            body_part=body_part,
                            severity_level=severity,
                            description='Ocorrência registrada automaticamente a partir do histórico de cargas.',
                            expected_return=expected_return,
                            actual_return=actual_return,
                            created_by=user,
                        )
                    )

        if load_instances:
            TrainingLoad.objects.bulk_create(load_instances, batch_size=1000)
        if injury_instances:
            InjuryRecord.objects.bulk_create(injury_instances, batch_size=500)

    def _generate_business_data(
        self,
        months: Sequence[MonthWindow],
        user: CustomUser,
        clubs: Sequence[Club],
    ) -> None:
        """Create monthly revenue breakdowns and financial records for each club."""
        today = date.today()
        existing_revenues = set(
            Revenue.objects.filter(year__gte=months[0].year).values_list('club_id', 'year', 'month')
        )
        existing_financial = set(
            FinancialRecord.objects.filter(record_date__gte=months[0].start).values_list(
                'club_id', 'record_date', 'category', 'transaction_type'
            )
        )

        revenue_profiles: Dict[str, Dict[str, float]] = {
            'CR Flamengo': {'ticketing': 7_800_000, 'sponsorship': 14_200_000, 'broadcasting': 18_500_000, 'merchandising': 4_600_000},
            'SE Palmeiras': {'ticketing': 6_900_000, 'sponsorship': 15_800_000, 'broadcasting': 16_400_000, 'merchandising': 3_900_000},
            'SC Internacional': {'ticketing': 5_200_000, 'sponsorship': 11_700_000, 'broadcasting': 14_100_000, 'merchandising': 3_200_000},
        }
        seasonality = {
            1: 0.94,
            2: 0.96,
            3: 0.98,
            4: 1.00,
            5: 1.04,
            6: 1.08,
            7: 1.12,
            8: 1.10,
            9: 1.05,
            10: 1.02,
            11: 1.00,
            12: 1.18,
        }

        revenue_instances: List[Revenue] = []
        financial_instances: List[FinancialRecord] = []

        for club in clubs:
            profile = revenue_profiles.get(club.name, revenue_profiles['SC Internacional'])
            for window in months:
                if (club.id, window.year, window.month) in existing_revenues:
                    continue
                trend_factor = 1 + (0.015 * window.index)
                seasonal_factor = seasonality.get(window.month, 1.0)
                multiplier = trend_factor * seasonal_factor

                ticketing = Decimal(str(round(profile['ticketing'] * multiplier, 2)))
                sponsorship = Decimal(str(round(profile['sponsorship'] * multiplier, 2)))
                broadcasting = Decimal(str(round(profile['broadcasting'] * multiplier, 2)))
                merchandising = Decimal(str(round(profile['merchandising'] * multiplier, 2)))

                revenue_instances.append(
                    Revenue(
                        club=club,
                        created_by=user,
                        year=window.year,
                        month=window.month,
                        ticketing=ticketing,
                        sponsorship=sponsorship,
                        broadcasting=broadcasting,
                        merchandising=merchandising,
                    )
                )

                record_date = min(window.end, today)
                if record_date < window.start:
                    continue

                month_total = ticketing + sponsorship + broadcasting + merchandising
                revenue_categories = [
                    ('MARKETING', ticketing, 'Receitas de bilheteria e matchday'),
                    ('MARKETING', merchandising, 'Receitas de produtos licenciados'),
                    ('OUTROS', sponsorship, 'Receitas de patrocínios e acordos comerciais'),
                    ('OUTROS', broadcasting, 'Cotas de TV e direitos de transmissão'),
                ]
                for category, amount, description in revenue_categories:
                    key = (club.id, record_date, category, 'RECEITA')
                    if key not in existing_financial:
                        financial_instances.append(
                            FinancialRecord(
                                club=club,
                                created_by=user,
                                record_date=record_date,
                                category=category,
                                amount=amount,
                                transaction_type='RECEITA',
                                description=description,
                            )
                        )
                        existing_financial.add(key)

                expenses = [
                    ('SALARIOS', month_total * Decimal('0.58'), 'Folha salarial do elenco principal'),
                    ('INFRAESTRUTURA', month_total * Decimal('0.14'), 'Investimentos em infraestrutura e ct'),
                ]
                for category, amount, description in expenses:
                    key = (club.id, record_date, category, 'DESPESA')
                    if key not in existing_financial:
                        financial_instances.append(
                            FinancialRecord(
                                club=club,
                                created_by=user,
                                record_date=record_date,
                                category=category,
                                amount=amount.quantize(Decimal('0.01')),
                                transaction_type='DESPESA',
                                description=description,
                            )
                        )
                        existing_financial.add(key)

        if revenue_instances:
            Revenue.objects.bulk_create(revenue_instances, batch_size=500)
        if financial_instances:
            FinancialRecord.objects.bulk_create(financial_instances, batch_size=500)

    def _generate_scouting_data(
        self,
        months: Sequence[MonthWindow],
        user: CustomUser,
        players: Sequence[ScoutedPlayer],
    ) -> None:
        """Generate scouting reports distributed along the 48 month range."""
        today = date.today()
        existing_reports = set(
            ScoutingReport.objects.filter(report_date__gte=months[0].start).values_list(
                'player_id', 'report_date', 'match_or_event'
            )
        )

        report_instances: List[ScoutingReport] = []
        player_style_index = {player.id: index for index, player in enumerate(players)}

        for window in months:
            period_end = min(window.end, today)
            if period_end < window.start:
                continue

            # Two detailed reports per month covering distinct players
            target_players = list(players)
            rotation_offset = (window.index * 3) % len(players)
            target_players = target_players[rotation_offset:] + target_players[:rotation_offset]
            for player in target_players[:2]:
                report_day = window.start + timedelta(days=((player.id + window.index * 2) % 20))
                if report_day > period_end:
                    report_day = period_end
                if report_day < window.start:
                    report_day = window.start

                match_label = f'Observação técnica {window.year}-{window.month:02d}'
                key = (player.id, report_day, match_label)
                if key in existing_reports:
                    continue

                base = 6 + (player_style_index[player.id] % 4)
                technical = min(10, base + (window.index % 3))
                physical = min(10, base + ((window.index + 1) % 3))
                tactical = min(10, base + ((window.index + 2) % 3))
                mental = min(10, base + ((player_style_index[player.id] + window.index) % 3))
                potential = max(7, min(10, (technical + tactical + mental) // 3 + 1))

                strengths = [
                    'Boa leitura tática em fase ofensiva',
                    'Capacidade de aceleração nos metros finais',
                    'Qualidade na tomada de decisão sob pressão',
                ]
                weaknesses = [
                    'Necessita evoluir na consistência defensiva',
                    'Pode aprimorar alternância de ritmo sem bola',
                ]

                report_instances.append(
                    ScoutingReport(
                        player=player,
                        created_by=user,
                        report_date=report_day,
                        match_or_event=match_label,
                        technical_score=technical,
                        physical_score=physical,
                        tactical_score=tactical,
                        mental_score=mental,
                        potential_score=potential,
                        strengths='\n'.join(strengths),
                        weaknesses='\n'.join(weaknesses),
                        recommendation='Manter monitoramento ativo e reavaliar a cada trimestre.',
                    )
                )
                existing_reports.add(key)

        if report_instances:
            ScoutingReport.objects.bulk_create(report_instances, batch_size=500)
