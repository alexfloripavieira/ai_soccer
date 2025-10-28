"""Account views."""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Landing page view for AI Soccer."""

    template_name = 'home.html'
