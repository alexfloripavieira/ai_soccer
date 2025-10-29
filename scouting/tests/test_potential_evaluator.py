from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from ml_models.potential_evaluator import (
    PotentialEvaluator,
    evaluate_player_potential,
    get_potential_evaluator,
)
from scouting.models import ScoutedPlayer, ScoutingReport


class PotentialEvaluatorTestCase(TestCase):
    """Validate behaviour of the potential evaluator model."""

    def setUp(self) -> None:
        user_model = get_user_model()
        self.user = user_model.objects.create_user(email='scout@example.com', password='password123')
        self.player = ScoutedPlayer.objects.create(
            created_by=self.user,
            name='João Silva',
            birth_date=date(2000, 1, 1),
            nationality='Brasil',
            position=ScoutedPlayer.POSITION_STRIKER,
            current_club='FC Teste',
        )
        base_date = date(2024, 1, 1)
        for index in range(8):
            ScoutingReport.objects.create(
                player=self.player,
                created_by=self.user,
                report_date=base_date + timedelta(days=index),
                match_or_event=f'Jogo {index + 1}',
                technical_score=6 + index % 3,
                physical_score=5 + (index % 4),
                tactical_score=6 + (index % 2),
                mental_score=7,
                potential_score=7 + (index % 3),
                strengths='Boa finalização',
                weaknesses='Precisa melhorar o jogo aéreo',
                recommendation='Continuar acompanhamento',
            )

    def test_train_and_evaluate_player(self) -> None:
        evaluator = PotentialEvaluator()
        self.assertTrue(evaluator.train())
        result = evaluator.evaluate_player(self.player)
        self.assertIsNotNone(result)
        assert result is not None  # for type checkers
        self.assertGreaterEqual(result.predicted_score, 0)
        self.assertLessEqual(result.predicted_score, 10)
        self.assertGreaterEqual(result.confidence, 0)
        self.assertEqual(result.report_count, 8)

    def test_global_evaluator_wrapper(self) -> None:
        evaluator = get_potential_evaluator()
        evaluator.train()
        result = evaluate_player_potential(self.player)
        self.assertIsNotNone(result)

    def test_returns_none_without_reports(self) -> None:
        another_player = ScoutedPlayer.objects.create(
            created_by=self.user,
            name='Pedro Souza',
            birth_date=date(2001, 5, 15),
            nationality='Brasil',
            position=ScoutedPlayer.POSITION_CENTER_BACK,
            current_club='Academia Jovem',
        )
        evaluator = PotentialEvaluator()
        self.assertTrue(evaluator.train())
        self.assertIsNone(evaluator.evaluate_player(another_player))
