"""Custom context processors for global templates."""

from __future__ import annotations

from typing import Any, Dict, List

from django.urls import reverse


def navigation(request):
    """Provide navigation items for sidebar and navbar components."""

    current_path = request.path

    performance_list_url = reverse('performance:athlete_list')
    performance_create_url = reverse('performance:athlete_create')
    scouted_player_list_url = reverse('scouting:player_list')
    scouted_player_create_url = reverse('scouting:player_create')

    sidebar_items: List[Dict[str, Any]] = [
        {
            'label': 'Início',
            'href': reverse('home'),
            'icon': 'home',
            'pattern': '/',
            'exact': True,
        },
        {
            'label': 'Dashboard',
            'href': reverse('accounts:dashboard'),
            'icon': 'chart',
            'pattern': reverse('accounts:dashboard'),
        },
        {
            'label': 'Performance',
            'href': performance_list_url,
            'icon': 'activity',
            'pattern': '/performance/',
            'children': [
                {
                    'label': 'Atletas',
                    'href': performance_list_url,
                    'pattern': '/performance/athletes/',
                    'exclude_patterns': ['/performance/athletes/novo/'],
                },
                {
                    'label': 'Cargas de treino',
                    'href': reverse('performance:training_load_list'),
                    'pattern': '/performance/training-loads/',
                    'exclude_patterns': ['/performance/training-loads/add/'],
                },
                {
                    'label': 'Novo atleta',
                    'href': performance_create_url,
                    'pattern': '/performance/athletes/novo/',
                },
            ],
        },
        {
            'label': 'Scouting',
            'href': scouted_player_list_url,
            'icon': 'radar',
            'pattern': '/scouting/',
            'children': [
                {
                    'label': 'Jogadores observados',
                    'href': scouted_player_list_url,
                    'pattern': '/scouting/jogadores/',
                    'exclude_patterns': ['/scouting/jogadores/novo/'],
                },
                {
                    'label': 'Cadastrar jogador',
                    'href': scouted_player_create_url,
                    'pattern': '/scouting/jogadores/novo/',
                },
            ],
        },
        {
            'label': 'Business',
            'href': '/business/',
            'icon': 'briefcase',
            'pattern': '/business/',
        },
    ]

    for item in sidebar_items:
        item.setdefault('exact', False)
        item_children = item.get('children', [])

        item['active'] = (
            current_path == item['href']
            if item['exact']
            else current_path.startswith(item['pattern'])
        )

        for child in item_children:
            child.setdefault('exact', False)
            child.setdefault('pattern', child['href'])
            # Provide optional patterns to exclude from activation
            exclude_patterns = child.get('exclude_patterns', [])
            child['active'] = (
                current_path == child['href']
                if child['exact']
                else current_path.startswith(child['pattern'])
            )
            if child['active'] and any(current_path.startswith(pattern) for pattern in exclude_patterns):
                child['active'] = False

        if any(child['active'] for child in item_children):
            item['active'] = True

    return {
        'sidebar_items': sidebar_items,
    }
