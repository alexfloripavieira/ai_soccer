from django.test import RequestFactory, TestCase
from django.urls import reverse

from core.context_processors import navigation


class NavigationContextTest(TestCase):
    """Ensure sidebar navigation context provides active states correctly."""

    def setUp(self):
        self.factory = RequestFactory()

    def _get_sidebar_items(self, path: str):
        request = self.factory.get(path)
        request.user = None  # context processor does not require user object
        context = navigation(request)
        return context['sidebar_items']

    def test_home_item_is_exact_match(self):
        sidebar_items = self._get_sidebar_items(reverse('home'))
        home = next(item for item in sidebar_items if item['label'] == 'Início')
        dashboard = next(item for item in sidebar_items if item['label'] == 'Dashboard')

        self.assertTrue(home['active'])
        self.assertFalse(dashboard['active'])

    def test_performance_children_activation(self):
        sidebar_items = self._get_sidebar_items(reverse('performance:athlete_create'))
        performance = next(item for item in sidebar_items if item['label'] == 'Performance')
        children = {child['label']: child for child in performance['children']}

        self.assertTrue(performance['active'])
        self.assertTrue(children['Novo atleta']['active'])
        self.assertFalse(children['Atletas']['active'])
