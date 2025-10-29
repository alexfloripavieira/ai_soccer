from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from performance.forms import AthleteForm
from performance.models import Athlete


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
