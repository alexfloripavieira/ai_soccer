"""Tools to train and use a potential evaluation model for scouted players."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from django.db.models import Avg, QuerySet
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from scouting.models import ScoutedPlayer, ScoutingReport

FEATURE_COLUMNS = ['technical_score', 'physical_score', 'tactical_score', 'mental_score']
TARGET_COLUMN = 'potential_score'
MINIMUM_SAMPLES = 8


@dataclass
class PredictionResult:
    """Represent the outcome of a potential prediction run."""

    predicted_score: float
    confidence: float
    report_count: int
    source: str

    def percentage(self) -> int:
        """Return the predicted score as a percentage value from 0 to 100."""
        return int(round((self.predicted_score / 10) * 100))

    def confidence_percentage(self) -> int:
        """Return the confidence value as a percentage between 0 and 100."""
        return int(round(self.confidence * 100))


class PotentialEvaluator:
    """Handle training and inference for the scouting potential regression model."""

    def __init__(self) -> None:
        self._model: Optional[LinearRegression] = None
        self._validation_score: Optional[float] = None
        self._trained_samples: int = 0

    def _fetch_training_reports(self) -> QuerySet[ScoutingReport]:
        """Return all scouting reports suitable for model training."""
        return ScoutingReport.objects.values(*FEATURE_COLUMNS, TARGET_COLUMN)

    def _build_training_frame(self) -> pd.DataFrame:
        """Convert reports queryset to a pandas DataFrame ready for modelling."""
        reports = list(self._fetch_training_reports())
        if not reports:
            return pd.DataFrame(columns=FEATURE_COLUMNS + [TARGET_COLUMN])
        frame = pd.DataFrame(reports)
        frame = frame.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
        for column in FEATURE_COLUMNS + [TARGET_COLUMN]:
            frame[column] = frame[column].astype(float)
        return frame

    def train(self) -> bool:
        """Train the regression model using the available scouting reports."""
        frame = self._build_training_frame()
        if frame.empty or len(frame) < MINIMUM_SAMPLES:
            self._model = None
            self._validation_score = None
            self._trained_samples = len(frame)
            return False

        features = frame[FEATURE_COLUMNS].to_numpy(dtype=float)
        labels = frame[TARGET_COLUMN].to_numpy(dtype=float)
        if len(frame) >= 20:
            X_train, X_test, y_train, y_test = train_test_split(
                features,
                labels,
                test_size=0.25,
                random_state=42,
            )
        else:
            X_train, X_test, y_train, y_test = features, features, labels, labels

        model = LinearRegression()
        model.fit(X_train, y_train)

        if len(frame) >= 20:
            predictions = model.predict(X_test)
            validation_score = r2_score(y_test, predictions)
        else:
            validation_score = model.score(X_test, y_test) if len(frame) >= MINIMUM_SAMPLES else None

        self._model = model
        self._validation_score = validation_score
        self._trained_samples = len(frame)
        return True

    def _ensure_trained(self) -> bool:
        """Ensure a trained model is available, trying to train if necessary."""
        if self._model is not None:
            return True
        return self.train()

    def _build_player_vector(self, player: ScoutedPlayer) -> Optional[np.ndarray]:
        """Aggregate a player's reports into a feature vector."""
        aggregates = player.reports.aggregate(
            technical_avg=Avg('technical_score'),
            physical_avg=Avg('physical_score'),
            tactical_avg=Avg('tactical_score'),
            mental_avg=Avg('mental_score'),
        )
        if all(value is None for value in aggregates.values()):
            return None

        vector = []
        for key in ['technical_avg', 'physical_avg', 'tactical_avg', 'mental_avg']:
            value = aggregates.get(key)
            if value is None:
                return None
            vector.append(float(value))
        return np.array(vector, dtype=float).reshape(1, -1)

    def _compute_confidence(self, report_count: int) -> float:
        """Estimate confidence based on validation performance and available data."""
        base_confidence = self._validation_score if self._validation_score is not None else 0.6
        base_confidence = max(0.0, min(1.0, base_confidence))
        volume_factor = min(1.0, report_count / 6)
        confidence = (base_confidence * 0.7) + (volume_factor * 0.3)
        return round(confidence, 3)

    def evaluate_player(self, player: ScoutedPlayer) -> Optional[PredictionResult]:
        """Return predicted potential for a player or None if unavailable."""
        if not self._ensure_trained():
            return None
        if self._model is None:
            return None

        feature_vector = self._build_player_vector(player)
        if feature_vector is None:
            return None

        predicted = float(self._model.predict(feature_vector)[0])
        predicted = max(0.0, min(10.0, predicted))
        report_count = player.reports.count()
        confidence = self._compute_confidence(report_count)
        source = f'{self._trained_samples} samples'
        return PredictionResult(predicted_score=predicted, confidence=confidence, report_count=report_count, source=source)


_evaluator = PotentialEvaluator()


def get_potential_evaluator() -> PotentialEvaluator:
    """Return a shared instance of the PotentialEvaluator."""
    return _evaluator


def evaluate_player_potential(player: ScoutedPlayer) -> Optional[PredictionResult]:
    """Convenience wrapper used by views to evaluate a player's potential."""
    evaluator = get_potential_evaluator()
    return evaluator.evaluate_player(player)
