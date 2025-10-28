"""Integration tests for authentication flows."""

from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    """Validate signup, login and logout flows."""

    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')
        self.home_url = reverse('home')

    def test_signup_creates_user_and_redirects_home(self):
        data = {
            'first_name': 'Teste',
            'last_name': 'Usuário',
            'email': 'novo-usuario@example.com',
            'password1': 'SenhaSegura123',
            'password2': 'SenhaSegura123',
        }

        response = self.client.post(self.signup_url, data, follow=True)

        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
        self.assertTrue(get_user_model().objects.filter(email=data['email']).exists())

        messages = list(response.context['messages'])
        self.assertTrue(any('Conta criada com sucesso' in str(message) for message in messages))

    def test_login_with_email_success(self):
        user = get_user_model().objects.create_user(
            email='login@example.com',
            password='SenhaSegura123',
            first_name='Login',
            last_name='User',
        )

        response = self.client.post(
            self.login_url,
            {'username': user.email, 'password': 'SenhaSegura123'},
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:dashboard'), status_code=302, target_status_code=200)
        self.assertIn(SESSION_KEY, self.client.session)

        messages = list(response.context['messages'])
        self.assertTrue(any('Bem-vindo de volta' in str(message) for message in messages))

    def test_protected_admin_redirects_to_login(self):
        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)

    def test_logout_redirects_to_home_with_message(self):
        user = get_user_model().objects.create_user(
            email='logout@example.com',
            password='SenhaSegura123',
            first_name='Logout',
            last_name='User',
        )
        self.client.login(email=user.email, password='SenhaSegura123')

        response = self.client.get(self.logout_url, follow=True)

        self.assertRedirects(response, self.home_url, status_code=302, target_status_code=200)
        self.assertNotIn(SESSION_KEY, self.client.session)

        messages = list(response.context['messages'])
        self.assertTrue(any('Você saiu do AI Soccer' in str(message) for message in messages))

    def test_templates_include_responsive_classes(self):
        signup_response = self.client.get(self.signup_url)
        login_response = self.client.get(self.login_url)

        self.assertContains(signup_response, 'lg:grid-cols-2')
        self.assertContains(login_response, 'lg:grid-cols-2')

    def test_navbar_for_anonymous_user(self):
        response = self.client.get(self.home_url)

        self.assertContains(response, 'Entrar')
        self.assertContains(response, 'Criar conta')

    def test_navbar_for_authenticated_user(self):
        user = get_user_model().objects.create_user(
            email='nav@example.com',
            password='SenhaSegura123',
            first_name='Nav',
            last_name='User',
        )
        self.client.login(email=user.email, password='SenhaSegura123')

        response = self.client.get(self.home_url)

        self.assertContains(response, 'Meu perfil')
        self.assertContains(response, 'Sair')

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_profile_view_shows_user_details(self):
        user = get_user_model().objects.create_user(
            email='profile@example.com',
            password='SenhaSegura123',
            first_name='Perfil',
            last_name='Teste',
        )
        self.client.login(email=user.email, password='SenhaSegura123')

        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perfil Teste')
        self.assertContains(response, 'Editar perfil')
        self.assertContains(response, 'profile@example.com')

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse('accounts:profile-edit'))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('accounts:login'), response.url)

    def test_profile_edit_updates_data(self):
        user = get_user_model().objects.create_user(
            email='update@example.com',
            password='SenhaSegura123',
            first_name='Nome',
            last_name='Antigo',
        )
        self.client.login(email=user.email, password='SenhaSegura123')

        response = self.client.post(
            reverse('accounts:profile-edit'),
            {
                'first_name': 'Nome Atualizado',
                'last_name': 'Novo',
                'email': 'update@example.com',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:profile'), status_code=302, target_status_code=200)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Nome Atualizado')
        self.assertEqual(user.last_name, 'Novo')

        messages = list(response.context['messages'])
        self.assertTrue(any('Perfil atualizado com sucesso' in str(message) for message in messages))
