"""Management command to train the injury prediction model."""

from django.core.management.base import BaseCommand

from ml_models.injury_predictor import get_injury_predictor


class Command(BaseCommand):
    """Train the RandomForest injury prediction model."""

    help = 'Treina o modelo de risco de lesões usando as cargas de treino registradas.'

    def handle(self, *args, **options):
        predictor = get_injury_predictor()
        if predictor.train():
            accuracy_display = (
                f'{predictor.validation_accuracy:.2%}'
                if predictor.validation_accuracy is not None
                else 'n/d'
            )
            self.stdout.write(self.style.SUCCESS('Modelo treinado com sucesso.'))
            self.stdout.write(
                f'● Amostras utilizadas: {predictor.trained_samples}\n'
                f'● Acurácia de validação: {accuracy_display}'
            )
        else:
            self.stdout.write(self.style.WARNING(
                'Não há dados suficientes para treinar o modelo de risco de lesões.'
            ))
