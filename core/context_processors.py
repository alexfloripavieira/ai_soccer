"""Custom context processors for global templates."""


def navigation(request):
    """Provide navigation items for sidebar and navbar components."""

    sidebar_items = [
        {
            'label': 'Início',
            'href': '/',
            'icon': 'home',
            'pattern': '/',
        },
        {
            'label': 'Dashboard',
            'href': '/dashboard/',
            'icon': 'chart',
            'pattern': '/dashboard/',
        },
        {
            'label': 'Performance',
            'href': '/performance/',
            'icon': 'activity',
            'pattern': '/performance/',
        },
        {
            'label': 'Scouting',
            'href': '/scouting/',
            'icon': 'radar',
            'pattern': '/scouting/',
        },
        {
            'label': 'Business',
            'href': '/business/',
            'icon': 'briefcase',
            'pattern': '/business/',
        },
    ]

    return {
        'sidebar_items': sidebar_items,
    }
