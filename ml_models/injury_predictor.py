"""Machine learning utilities to predict injury risk for athletes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd
from django.db.models import QuerySet
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from performance.models import Athlete, InjuryRecord, TrainingLoad

FEATURE_COLUMNS = ['duration_minutes', 'distance_km', 'session_frequency', 'acute_chronic_ratio']
LABEL_COLUMN = 'injury_next_30_days'
MINIMUM_SAMPLES = 25
RECENT_WINDOW_DAYS = 28
CHRONIC_WINDOW_DAYS = 60
FUTURE_INJURY_WINDOW_DAYS = 30


@dataclass
class InjuryRiskResult:
    """Represent model inference output for a single athlete."""

    athlete: Athlete
    risk_probability: float
    risk_label: str
    session_frequency: int
    average_duration: float
    average_distance: float
    acute_chronic_ratio: float
    trained_samples: int
    validation_accuracy: Optional[float]
    confidence: float

    def percentage(self) -> int:
        """Return formatted injury probability as integer percentage."""
        return int(round(self.risk_probability * 100))

    def confidence_percentage(self) -> int:
        """Return prediction confidence as integer percentage."""
        return int(round(self.confidence * 100))


class InjuryPredictor:
    """Encapsulate training and inference of the injury risk classifier."""

    def __init__(self) -> None:
        self._model: Optional[RandomForestClassifier] = None
        self._validation_accuracy: Optional[float] = None
        self._trained_samples: int = 0

    @property
    def validation_accuracy(self) -> Optional[float]:
        """Return last computed validation accuracy."""
        return self._validation_accuracy

    @property
    def trained_samples(self) -> int:
        """Return number of training samples used in the last fit."""
        return self._trained_samples

    def _fetch_training_loads(self) -> QuerySet[TrainingLoad]:
        """Return all training load records with related athlete data."""
        return TrainingLoad.objects.select_related('athlete').order_by('training_date')

    def _fetch_injury_records(self) -> QuerySet[InjuryRecord]:
        """Return all injury records sorted by date."""
        return InjuryRecord.objects.select_related('athlete').order_by('injury_date')

    def _prepare_training_rows(self) -> List[Dict[str, float]]:
        """Convert training and injury history to a list of feature dicts."""
        loads = list(self._fetch_training_loads())
        if not loads:
            return []

        injuries_by_athlete: Dict[int, List[date]] = {}
        for injury in self._fetch_injury_records():
            injuries_by_athlete.setdefault(injury.athlete_id, []).append(injury.injury_date)

        training_history: Dict[int, List[TrainingLoad]] = {}
        for load in loads:
            training_history.setdefault(load.athlete_id, []).append(load)

        rows: List[Dict[str, float]] = []
        for athlete_id, athlete_loads in training_history.items():
            athlete_loads.sort(key=lambda item: item.training_date)
            injury_dates = injuries_by_athlete.get(athlete_id, [])

            for index, load in enumerate(athlete_loads):
                recent_window_start = load.training_date - timedelta(days=RECENT_WINDOW_DAYS)
                chronic_window_start = load.training_date - timedelta(days=CHRONIC_WINDOW_DAYS)

                recent_loads = [
                    item for item in athlete_loads
                    if recent_window_start <= item.training_date <= load.training_date
                ]
                chronic_loads = [
                    item for item in athlete_loads
                    if chronic_window_start <= item.training_date <= load.training_date
                ]
                if not chronic_loads:
                    continue

                recent_distance = sum(float(item.distance_km) for item in recent_loads)
                chronic_distance = sum(float(item.distance_km) for item in chronic_loads)
                acute_chronic_ratio = (recent_distance / len(recent_loads)) / (
                    (chronic_distance / len(chronic_loads)) if chronic_distance else 1
                )

                session_frequency = len(recent_loads)
                label = any(
                    injury_date for injury_date in injury_dates
                    if load.training_date < injury_date <= load.training_date + timedelta(days=FUTURE_INJURY_WINDOW_DAYS)
                )

                rows.append(
                    {
                        'duration_minutes': float(load.duration_minutes),
                        'distance_km': float(load.distance_km),
                        'session_frequency': float(session_frequency),
                        'acute_chronic_ratio': float(acute_chronic_ratio),
                        LABEL_COLUMN: 1.0 if label else 0.0,
                    }
                )
        return rows

    def _build_training_frame(self) -> pd.DataFrame:
        """Return a pandas DataFrame containing training samples and labels."""
        rows = self._prepare_training_rows()
        if not rows:
            return pd.DataFrame(columns=FEATURE_COLUMNS + [LABEL_COLUMN])
        frame = pd.DataFrame(rows)
        frame = frame.replace([np.inf, -np.inf], np.nan).dropna()
        return frame

    def train(self) -> bool:
        """Train the RandomForest model if enough data is available."""
        frame = self._build_training_frame()
        if frame.empty or len(frame) < MINIMUM_SAMPLES:
            self._model = None
            self._trained_samples = len(frame)
            self._validation_accuracy = None
            return False

        features = frame[FEATURE_COLUMNS].to_numpy(dtype=float)
        labels = frame[LABEL_COLUMN].to_numpy(dtype=int)

        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=0.2, random_state=42, stratify=labels
        )
        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight='balanced',
        )
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions) if len(X_test) else None

        self._model = model
        self._trained_samples = len(frame)
        self._validation_accuracy = accuracy
        return True

    def _ensure_model(self) -> bool:
        """Ensure the model is trained and available."""
        if self._model is not None:
            return True
        return self.train()

    def _aggregate_recent_training(self, athlete: Athlete) -> Optional[Dict[str, float]]:
        """Aggregate training metrics for inference of a single athlete."""
        today = date.today()
        recent_threshold = today - timedelta(days=RECENT_WINDOW_DAYS)
        chronic_threshold = today - timedelta(days=CHRONIC_WINDOW_DAYS)

        recent_loads = list(
            athlete.training_loads.filter(training_date__gte=recent_threshold).order_by('-training_date')
        )
        chronic_loads = list(
            athlete.training_loads.filter(training_date__gte=chronic_threshold).order_by('-training_date')
        )
        if not chronic_loads:
            return None

        session_frequency = len(recent_loads)
        average_duration = (
            sum(load.duration_minutes for load in recent_loads) / session_frequency
            if session_frequency else 0.0
        )
        average_distance = (
            sum(float(load.distance_km) for load in recent_loads) / session_frequency
            if session_frequency else 0.0
        )

        acute_distance = sum(float(load.distance_km) for load in recent_loads) or 0.0
        chronic_distance = sum(float(load.distance_km) for load in chronic_loads) or 1.0
        acute_chronic_ratio = (
            (acute_distance / max(session_frequency, 1))
            / (chronic_distance / len(chronic_loads))
            if chronic_distance and len(chronic_loads)
            else 0.0
        )

        return {
            'duration_minutes': float(average_duration or 0.0),
            'distance_km': float(average_distance or 0.0),
            'session_frequency': float(session_frequency),
            'acute_chronic_ratio': float(acute_chronic_ratio),
        }

    def _compute_prediction_confidence(self, session_frequency: float) -> float:
        """Estimate confidence based on validation accuracy, data volume, and recency."""
        base_confidence = self._validation_accuracy if self._validation_accuracy is not None else 0.65
        base_confidence = max(0.0, min(1.0, base_confidence))
        volume_factor = min(1.0, self._trained_samples / float(MINIMUM_SAMPLES * 2)) if self._trained_samples else 0.3
        session_factor = min(1.0, session_frequency / 12.0)
        confidence = (base_confidence * 0.6) + (volume_factor * 0.25) + (session_factor * 0.15)
        return round(max(0.0, min(1.0, confidence)), 3)

    def evaluate_athlete(self, athlete: Athlete) -> Optional[InjuryRiskResult]:
        """Return injury risk prediction for a single athlete."""
        if not self._ensure_model():
            return None
        if self._model is None:
            return None

        feature_dict = self._aggregate_recent_training(athlete)
        if feature_dict is None:
            return None

        feature_array = np.array([[feature_dict[column] for column in FEATURE_COLUMNS]], dtype=float)
        probability = float(self._model.predict_proba(feature_array)[0][1])
        risk_label = self._map_probability_to_label(probability)
        confidence = self._compute_prediction_confidence(feature_dict['session_frequency'])
        return InjuryRiskResult(
            athlete=athlete,
            risk_probability=probability,
            risk_label=risk_label,
            session_frequency=int(feature_dict['session_frequency']),
            average_duration=feature_dict['duration_minutes'],
            average_distance=feature_dict['distance_km'],
            acute_chronic_ratio=feature_dict['acute_chronic_ratio'],
            trained_samples=self._trained_samples,
            validation_accuracy=self._validation_accuracy,
            confidence=confidence,
        )

    def _map_probability_to_label(self, value: float) -> str:
        """Translate raw probability into user friendly label."""
        if value >= 0.7:
            return 'Alto risco'
        if value >= 0.4:
            return 'Risco moderado'
        return 'Baixo risco'

    def evaluate_team(self, athletes: Optional[Iterable[Athlete]] = None) -> List[InjuryRiskResult]:
        """Return risk predictions for the provided athletes ordered by probability."""
        target_athletes = athletes or Athlete.objects.order_by('name')
        results = []
        for athlete in target_athletes:
            result = self.evaluate_athlete(athlete)
            if result:
                results.append(result)
        results.sort(key=lambda item: item.risk_probability, reverse=True)
        return results


_predictor = InjuryPredictor()


def get_injury_predictor() -> InjuryPredictor:
    """Return shared InjuryPredictor instance."""
    return _predictor


def evaluate_injury_risk(athlete: Athlete) -> Optional[InjuryRiskResult]:
    """Convenience wrapper used by views and templates."""
    return get_injury_predictor().evaluate_athlete(athlete)


def evaluate_injury_risk_for_team(athletes: Optional[Iterable[Athlete]] = None) -> List[InjuryRiskResult]:
    """Convenience wrapper returning predictions for multiple athletes."""
    return get_injury_predictor().evaluate_team(athletes=athletes)
