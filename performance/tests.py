from datetime import date, timedelta
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from ml_models.injury_predictor import (
    InjuryPredictor,
    MINIMUM_SAMPLES,
    evaluate_injury_risk_for_team,
    get_injury_predictor,
)
from performance.forms import AthleteForm, TrainingLoadForm
from performance.models import Athlete, InjuryRecord, TrainingLoad


class AthleteFormTest(TestCase):
    """Validate AthleteForm custom rules."""

    def setUp(self):
        self.default_data = {
            'name': 'Jogador Teste',
            'birth_date': date(2000, 1, 1),
            'position': Athlete.POSITION_FORWARD,
            'nationality': 'Brasil',
            'height': 180,
            'weight': 75,
        }

    def test_birth_date_cannot_be_in_future(self):
        future_date = date.today() + timedelta(days=1)
        form = AthleteForm({**self.default_data, 'birth_date': future_date})
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_height_and_weight_must_be_positive(self):
        form = AthleteForm({**self.default_data, 'height': -10, 'weight': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('height', form.errors)
        self.assertIn('weight', form.errors)


class AthleteCreateViewTest(TestCase):
    """Ensure create view stores athlete and binds creator."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='coach@example.com',
            password='strong-password',
        )
        self.url = reverse('performance:athlete_create')
        self.valid_payload = {
            'name': 'João Silva',
            'birth_date': '2001-04-20',
            'position': Athlete.POSITION_MIDFIELDER,
            'nationality': 'Brasil',
            'height': 178,
            'weight': 72,
        }

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_creates_athlete_and_sets_creator(self):
        self.client.login(email='coach@example.com', password='strong-password')

        response = self.client.post(self.url, self.valid_payload)

        self.assertRedirects(
            response,
            reverse('performance:athlete_list'),
            fetch_redirect_response=False,
        )
        athlete = Athlete.objects.get(name='João Silva')
        self.assertEqual(athlete.created_by, self.user)


class AthleteDetailViewTest(TestCase):
    """Validate detail view rendering and protections."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='staff@example.com',
            password='strong-password',
            first_name='Ana',
            last_name='Silva',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Carlos Mendes',
            birth_date=date(1998, 6, 15),
            position=Athlete.POSITION_DEFENDER,
            nationality='Brasil',
            height=185,
            weight=82,
        )
        self.url = reverse('performance:athlete_detail', args=[self.athlete.pk])
        TrainingLoad.objects.create(
            athlete=self.athlete,
            training_date=date.today() - timedelta(days=1),
            duration_minutes=60,
            distance_km=Decimal('8.5'),
            heart_rate_avg=130,
            heart_rate_max=165,
            intensity_level=TrainingLoad.INTENSITY_MEDIUM,
            created_by=self.user,
        )
        self.injury = InjuryRecord.objects.create(
            athlete=self.athlete,
            injury_date=date.today() - timedelta(days=5),
            injury_type=InjuryRecord.INJURY_MUSCULAR,
            body_part=InjuryRecord.BODY_THIGH,
            severity_level=InjuryRecord.SEVERITY_MODERATE,
            description='Lesão muscular na coxa esquerda',
            expected_return=date.today() + timedelta(days=10),
            created_by=self.user,
        )

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_renders_details_for_authenticated_user(self):
        self.client.login(email='staff@example.com', password='strong-password')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'performance/athlete_detail.html')
        self.assertIn('athlete', response.context)
        self.assertContains(response, 'Carlos Mendes')
        self.assertContains(response, 'Defensor')
        self.assertContains(response, 'staff@example.com')
        self.assertIn('latest_training_loads', response.context)
        self.assertTrue(response.context['has_training_loads'])
        self.assertIn('injury_records', response.context)
        self.assertTrue(response.context['is_currently_injured'])
        self.assertEqual(response.context['injury_tab'], 'training')
        self.assertContains(response, 'Atleta lesionado')

    def test_switches_to_injury_tab(self):
        self.client.login(email='staff@example.com', password='strong-password')

        response = self.client.get(f'{self.url}?tab=injuries')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['injury_tab'], 'injuries')
        self.assertContains(response, 'Histórico de lesões')
        self.assertContains(response, 'Registrar lesão')
        self.assertIn(self.injury, response.context['injury_records'])


class AthleteUpdateViewTest(TestCase):
    """Ensure athletes can be edited with proper validations."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='coach@example.com',
            password='strong-password',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Pedro Souza',
            birth_date=date(1995, 2, 10),
            position=Athlete.POSITION_FORWARD,
            nationality='Brasil',
            height=175,
            weight=70,
        )
        self.url = reverse('performance:athlete_update', args=[self.athlete.pk])

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_updates_fields_with_valid_data(self):
        self.client.login(email='coach@example.com', password='strong-password')

        payload = {
            'name': 'Pedro Souza',
            'birth_date': '1995-02-10',
            'position': Athlete.POSITION_MIDFIELDER,
            'nationality': 'Brasil',
            'height': 176,
            'weight': 71,
        }

        response = self.client.post(self.url, payload)

        self.assertRedirects(
            response,
            reverse('performance:athlete_detail', args=[self.athlete.pk]),
            fetch_redirect_response=False,
        )
        self.athlete.refresh_from_db()
        self.assertEqual(self.athlete.position, Athlete.POSITION_MIDFIELDER)
        self.assertEqual(self.athlete.height, 176)
        self.assertEqual(self.athlete.weight, 71)

    def test_invalid_data_returns_errors(self):
        self.client.login(email='coach@example.com', password='strong-password')

        payload = {
            'name': 'Pedro Souza',
            'birth_date': '2100-01-01',
            'position': Athlete.POSITION_FORWARD,
            'nationality': 'Brasil',
            'height': -10,
            'weight': 0,
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'performance/athlete_form.html')
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertIn('Data de nascimento não pode estar no futuro.', form.errors['birth_date'])
        self.assertIn('Altura deve ser maior que zero.', form.errors['height'])
        self.assertIn('Peso deve ser maior que zero.', form.errors['weight'])


class AthleteDeleteViewTest(TestCase):
    """Validate delete confirmation flow."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='manager@example.com',
            password='strong-password',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Rafael Lima',
            birth_date=date(1992, 11, 5),
            position=Athlete.POSITION_GOALKEEPER,
            nationality='Brasil',
            height=190,
            weight=83,
        )
        self.url = reverse('performance:athlete_delete', args=[self.athlete.pk])

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_displays_confirmation_template(self):
        self.client.login(email='manager@example.com', password='strong-password')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'performance/athlete_confirm_delete.html')
        self.assertContains(response, 'Rafael Lima')
        self.assertContains(response, 'Confirmar exclusão')

    def test_deletes_athlete_on_post(self):
        self.client.login(email='manager@example.com', password='strong-password')

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse('performance:athlete_list'),
            fetch_redirect_response=False,
        )
        self.assertFalse(Athlete.objects.filter(pk=self.athlete.pk).exists())


class TrainingLoadModelTest(TestCase):
    """Ensure TrainingLoad model helpers behave as expected."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='coach@example.com',
            password='strong-password',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Lucas Rocha',
            birth_date=date(1999, 3, 12),
            position=Athlete.POSITION_MIDFIELDER,
            nationality='Brasil',
            height=178,
            weight=72,
        )
        self.training_load = TrainingLoad.objects.create(
            athlete=self.athlete,
            training_date=date(2025, 10, 1),
            duration_minutes=75,
            distance_km=Decimal('9.5'),
            heart_rate_avg=125,
            heart_rate_max=170,
            intensity_level=TrainingLoad.INTENSITY_HIGH,
            created_by=self.user,
        )

    def test_str_representation(self):
        self.assertEqual(str(self.training_load), 'Lucas Rocha - 2025-10-01')

    def test_fatigue_index(self):
        self.assertAlmostEqual(self.training_load.fatigue_index(), 0.7125)

    def test_intensity_badge_class(self):
        self.assertIn('bg-amber-500/20', self.training_load.intensity_badge_class())


class TrainingLoadFormTest(TestCase):
    """Validate TrainingLoadForm business rules."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='physio@example.com',
            password='strong-password',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Thiago Nunes',
            birth_date=date(2000, 7, 22),
            position=Athlete.POSITION_FORWARD,
            nationality='Brasil',
            height=180,
            weight=78,
        )
        self.valid_payload = {
            'athlete': self.athlete.pk,
            'training_date': date.today(),
            'duration_minutes': 60,
            'distance_km': Decimal('6.5'),
            'heart_rate_avg': 140,
            'heart_rate_max': 170,
            'intensity_level': TrainingLoad.INTENSITY_MEDIUM,
        }

    def test_valid_payload(self):
        form = TrainingLoadForm(self.valid_payload)
        self.assertTrue(form.is_valid())

    def test_future_training_date_not_allowed(self):
        data = self.valid_payload | {'training_date': date.today() + timedelta(days=1)}
        form = TrainingLoadForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('training_date', form.errors)

    def test_distance_cannot_be_negative(self):
        data = self.valid_payload | {'distance_km': Decimal('-1')}
        form = TrainingLoadForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('distance_km', form.errors)

    def test_heart_rate_avg_cannot_exceed_max(self):
        data = self.valid_payload | {'heart_rate_avg': 180, 'heart_rate_max': 170}
        form = TrainingLoadForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('heart_rate_avg', form.errors)


class TrainingLoadViewsTest(TestCase):
    """Exercise list, create, update and delete views for training loads."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='coach@example.com',
            password='strong-password',
        )
        self.other_user = get_user_model().objects.create_user(
            email='assistant@example.com',
            password='strong-password',
        )
        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='João Pereira',
            birth_date=date(1997, 4, 10),
            position=Athlete.POSITION_GOALKEEPER,
            nationality='Brasil',
            height=188,
            weight=84,
        )
        self.training_load = TrainingLoad.objects.create(
            athlete=self.athlete,
            training_date=date.today() - timedelta(days=3),
            duration_minutes=55,
            distance_km=Decimal('5.5'),
            heart_rate_avg=120,
            heart_rate_max=160,
            intensity_level=TrainingLoad.INTENSITY_MEDIUM,
            created_by=self.user,
        )
        TrainingLoad.objects.create(
            athlete=self.athlete,
            training_date=date.today() - timedelta(days=10),
            duration_minutes=70,
            distance_km=Decimal('7.2'),
            intensity_level=TrainingLoad.INTENSITY_LOW,
            created_by=self.user,
        )
        self.client.login(email='coach@example.com', password='strong-password')

    def test_list_filters_by_period(self):
        url = reverse('performance:training_load_list')
        response = self.client.get(url, {'period': 'last_7_days'})
        self.assertEqual(response.status_code, 200)
        loads = response.context['training_loads']
        self.assertTrue(all(load.training_date >= date.today() - timedelta(days=7) for load in loads))

    def test_create_training_load_sets_creator(self):
        url = reverse('performance:training_load_create')
        payload = {
            'athlete': self.athlete.pk,
            'training_date': date.today(),
            'duration_minutes': 65,
            'distance_km': '6.2',
            'heart_rate_avg': 135,
            'heart_rate_max': 172,
            'intensity_level': TrainingLoad.INTENSITY_HIGH,
        }
        response = self.client.post(url, payload)
        self.assertRedirects(response, reverse('performance:training_load_list'))
        training_load = TrainingLoad.objects.get(distance_km=Decimal('6.2'))
        self.assertEqual(training_load.created_by, self.user)

    def test_update_training_load(self):
        url = reverse('performance:training_load_update', args=[self.training_load.pk])
        response = self.client.post(
            url,
            {
                'athlete': self.athlete.pk,
                'training_date': self.training_load.training_date,
                'duration_minutes': 60,
                'distance_km': '6.0',
                'heart_rate_avg': 130,
                'heart_rate_max': 165,
                'intensity_level': TrainingLoad.INTENSITY_HIGH,
            },
        )
        self.assertRedirects(response, reverse('performance:training_load_list'))
        self.training_load.refresh_from_db()
        self.assertEqual(self.training_load.duration_minutes, 60)
        self.assertEqual(self.training_load.intensity_level, TrainingLoad.INTENSITY_HIGH)

    def test_delete_training_load(self):
        url = reverse('performance:training_load_delete', args=[self.training_load.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('performance:training_load_list'))
        self.assertFalse(TrainingLoad.objects.filter(pk=self.training_load.pk).exists())


class PerformanceDashboardViewTest(TestCase):
    """Validate aggregated metrics and alerts in the performance dashboard."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='analytics@example.com',
            password='strong-password',
        )
        self.client.login(email='analytics@example.com', password='strong-password')

        self.athlete_active = Athlete.objects.create(
            created_by=self.user,
            name='Diego Sousa',
            birth_date=date(1996, 5, 20),
            position=Athlete.POSITION_FORWARD,
            nationality='Brasil',
            height=180,
            weight=76,
        )
        self.athlete_injured = Athlete.objects.create(
            created_by=self.user,
            name='Ricardo Lima',
            birth_date=date(1999, 9, 12),
            position=Athlete.POSITION_MIDFIELDER,
            nationality='Brasil',
            height=177,
            weight=72,
        )
        TrainingLoad.objects.create(
            athlete=self.athlete_active,
            training_date=date.today(),
            duration_minutes=90,
            distance_km=Decimal('10.0'),
            intensity_level=TrainingLoad.INTENSITY_VERY_HIGH,
            created_by=self.user,
        )
        TrainingLoad.objects.create(
            athlete=self.athlete_active,
            training_date=date.today() - timedelta(days=2),
            duration_minutes=85,
            distance_km=Decimal('9.2'),
            intensity_level=TrainingLoad.INTENSITY_HIGH,
            created_by=self.user,
        )
        InjuryRecord.objects.create(
            athlete=self.athlete_injured,
            injury_date=date.today() - timedelta(days=3),
            injury_type=InjuryRecord.INJURY_MUSCULAR,
            body_part=InjuryRecord.BODY_THIGH,
            severity_level=InjuryRecord.SEVERITY_MODERATE,
            description='Lesão muscular na coxa esquerda',
            created_by=self.user,
        )
        self.url = reverse('performance:dashboard')

    def test_requires_authentication(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response['Location'])

    def test_dashboard_metrics_and_alerts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'performance/performance_dashboard.html')

        self.assertEqual(response.context['total_athletes'], 2)
        self.assertEqual(response.context['injured_athletes'], 1)
        self.assertEqual(response.context['active_athletes'], 1)
        self.assertIsNotNone(response.context['average_age'])

        latest_loads = response.context['latest_training_loads']
        self.assertTrue(any(load.athlete == self.athlete_active for load in latest_loads))

        recent_injuries = response.context['recent_injuries']
        self.assertTrue(any(injury.athlete == self.athlete_injured for injury in recent_injuries))

        alerts = response.context['alerts']
        self.assertTrue(any(alert['athlete'] == self.athlete_active for alert in alerts))

        activities = response.context['latest_activities']
        self.assertGreaterEqual(len(activities), 1)


class InjuryPredictorTestCase(TestCase):
    """Validate training pipeline and integration helpers for injury predictor."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='coach@example.com',
            password='strong-password',
        )
        self.client.force_login(self.user)

        self.athlete = Athlete.objects.create(
            created_by=self.user,
            name='Carlos Pereira',
            birth_date=date(1998, 6, 1),
            position=Athlete.POSITION_MIDFIELDER,
            nationality='Brasil',
            height=180,
            weight=75,
        )
        self.secondary_athlete = Athlete.objects.create(
            created_by=self.user,
            name='Eduardo Silva',
            birth_date=date(1995, 4, 12),
            position=Athlete.POSITION_FORWARD,
            nationality='Brasil',
            height=182,
            weight=78,
        )

        today = date.today()
        for day_offset in range(40):
            training_date = today - timedelta(days=40 - day_offset)
            TrainingLoad.objects.create(
                athlete=self.athlete,
                training_date=training_date,
                duration_minutes=60 + (day_offset % 15),
                distance_km=Decimal('5.0') + Decimal(day_offset % 4),
                heart_rate_avg=130,
                heart_rate_max=175,
                intensity_level=TrainingLoad.INTENSITY_MEDIUM,
                created_by=self.user,
            )

        for day_offset in range(10):
            training_date = today - timedelta(days=10 - day_offset)
            TrainingLoad.objects.create(
                athlete=self.secondary_athlete,
                training_date=training_date,
                duration_minutes=50 + day_offset,
                distance_km=Decimal('4.5') + Decimal(day_offset % 3),
                heart_rate_avg=128,
                heart_rate_max=168,
                intensity_level=TrainingLoad.INTENSITY_LOW,
                created_by=self.user,
            )

        InjuryRecord.objects.create(
            athlete=self.athlete,
            injury_date=today - timedelta(days=5),
            injury_type=InjuryRecord.INJURY_MUSCULAR,
            body_part=InjuryRecord.BODY_HAMSTRING,
            severity_level=InjuryRecord.SEVERITY_MODERATE,
            description='Lesao muscular detectada apos sequencia intensa.',
            expected_return=today + timedelta(days=10),
            created_by=self.user,
        )

        shared_predictor = get_injury_predictor()
        shared_predictor._model = None  # noqa: SLF001 - reset for testing
        shared_predictor._trained_samples = 0  # noqa: SLF001
        shared_predictor._validation_accuracy = None  # noqa: SLF001

    def test_predictor_trains_and_evaluates(self) -> None:
        predictor = InjuryPredictor()
        self.assertTrue(predictor.train())
        self.assertGreaterEqual(predictor.trained_samples, MINIMUM_SAMPLES)
        athlete_result = predictor.evaluate_athlete(self.athlete)
        self.assertIsNotNone(athlete_result)
        assert athlete_result is not None
        self.assertGreaterEqual(athlete_result.risk_probability, 0.0)
        self.assertLessEqual(athlete_result.risk_probability, 1.0)
        self.assertGreaterEqual(athlete_result.confidence, 0.0)
        self.assertLessEqual(athlete_result.confidence, 1.0)

    def test_global_predictor_wrapper_returns_results(self) -> None:
        predictor = get_injury_predictor()
        self.assertTrue(predictor.train())
        team_results = evaluate_injury_risk_for_team()
        self.assertTrue(team_results)
        self.assertGreaterEqual(len(team_results), 1)

    def test_injury_risk_view_renders_predictions(self) -> None:
        predictor = get_injury_predictor()
        predictor.train()
        response = self.client.get(reverse('performance:injury_risk'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.context)

    def test_management_command_outputs_success(self) -> None:
        output = StringIO()
        call_command('train_injury_model', stdout=output)
        self.assertIn('Modelo treinado com sucesso', output.getvalue())
