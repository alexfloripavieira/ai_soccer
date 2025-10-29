"""Revenue forecasting utilities powered by linear regression."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional, Union

import numpy as np
import pandas as pd
from django.db.models import QuerySet, Sum
from sklearn.linear_model import LinearRegression

from business.models import Club, Revenue

MINIMUM_SAMPLES = 4
FORECAST_PERIODS = 6
CATEGORY_COLUMNS = ['ticketing', 'sponsorship', 'broadcasting', 'merchandising']


def _month_as_date(year: int, month: int) -> date:
    """Return a date representing the first day of the provided year/month."""
    return date(year=year, month=month, day=1)


def _format_month_label(year: int, month: int) -> str:
    """Return Portuguese month label in the format 'Mês Ano'."""
    month_name = Revenue.MONTH_NAMES.get(month, f'Mês {month}')
    return f'{month_name} {year}'


@dataclass
class ForecastPoint:
    """Represent a single historical or predicted revenue data point."""

    period: date
    label: str
    total: float
    ticketing: float
    sponsorship: float
    broadcasting: float
    merchandising: float
    is_prediction: bool


@dataclass
class ForecastResult:
    """Container with historical data, predictions, and training metadata."""

    historical: List[ForecastPoint]
    predictions: List[ForecastPoint]
    trained_samples: int
    model_score: Optional[float]
    category_distribution: Dict[str, float]
    has_sufficient_data: bool

    @property
    def points(self) -> List[ForecastPoint]:
        """Return historical points followed by predictions."""
        return self.historical + self.predictions


class RevenueForecaster:
    """Handle revenue forecasting for the business module."""

    def __init__(self) -> None:
        self._model: Optional[LinearRegression] = None
        self._trained_samples: int = 0
        self._model_score: Optional[float] = None
        self._category_distribution: Dict[str, float] = {column: 0.0 for column in CATEGORY_COLUMNS}
        self._last_frame: Optional[pd.DataFrame] = None
        self._last_club_id: Optional[int] = None

    def _fetch_revenues(self, club: Optional[Union[Club, int]]) -> QuerySet:
        """Return queryset with aggregated revenue data per month."""
        queryset = Revenue.objects.all()
        if club:
            club_id = club.pk if isinstance(club, Club) else club
            queryset = queryset.filter(club_id=club_id)
        return queryset.values('year', 'month').annotate(
            ticketing_total=Sum('ticketing'),
            sponsorship_total=Sum('sponsorship'),
            broadcasting_total=Sum('broadcasting'),
            merchandising_total=Sum('merchandising'),
        ).order_by('year', 'month')

    def _build_training_frame(self, club: Optional[Union[Club, int]]) -> pd.DataFrame:
        """Convert queryset to a pandas DataFrame ready for modelling."""
        records = list(self._fetch_revenues(club=club))
        if not records:
            return pd.DataFrame(columns=['year', 'month'] + CATEGORY_COLUMNS + ['total_revenue', 'month_index'])

        data: Dict[str, List[float]] = {
            'year': [],
            'month': [],
            'ticketing': [],
            'sponsorship': [],
            'broadcasting': [],
            'merchandising': [],
        }
        for record in records:
            data['year'].append(int(record['year']))
            data['month'].append(int(record['month']))
            data['ticketing'].append(float(record['ticketing_total'] or 0.0))
            data['sponsorship'].append(float(record['sponsorship_total'] or 0.0))
            data['broadcasting'].append(float(record['broadcasting_total'] or 0.0))
            data['merchandising'].append(float(record['merchandising_total'] or 0.0))

        frame = pd.DataFrame(data)
        frame['total_revenue'] = frame[CATEGORY_COLUMNS].sum(axis=1)
        frame['month_index'] = np.arange(len(frame), dtype=float)
        return frame

    def _compute_category_distribution(self, frame: pd.DataFrame) -> Dict[str, float]:
        """Calculate proportional contribution of each revenue category."""
        totals = frame[CATEGORY_COLUMNS].sum()
        grand_total = float(totals.sum())
        if grand_total <= 0:
            return {column: 1.0 / len(CATEGORY_COLUMNS) for column in CATEGORY_COLUMNS}
        distribution = {column: float(totals[column]) / grand_total for column in CATEGORY_COLUMNS}
        return distribution

    def _train_model(self, frame: pd.DataFrame) -> LinearRegression:
        """Fit a linear regression model using month index as the feature."""
        model = LinearRegression()
        features = frame[['month_index']].to_numpy(dtype=float)
        target = frame['total_revenue'].to_numpy(dtype=float)
        model.fit(features, target)
        if len(frame) >= 2:
            self._model_score = float(model.score(features, target))
        else:
            self._model_score = None
        self._trained_samples = len(frame)
        self._model = model
        return model

    def train(self, club: Optional[Union[Club, int]] = None) -> bool:
        """Train the forecasting model for the provided club or global context."""
        frame = self._build_training_frame(club=club)
        self._last_frame = frame
        self._last_club_id = club.pk if isinstance(club, Club) else club
        self._trained_samples = len(frame)

        if frame.empty or len(frame) < MINIMUM_SAMPLES:
            self._model = None
            self._model_score = None
            self._category_distribution = {column: 0.0 for column in CATEGORY_COLUMNS}
            return False

        self._category_distribution = self._compute_category_distribution(frame)
        self._train_model(frame)
        return True

    def _ensure_trained(self, club: Optional[Union[Club, int]]) -> bool:
        """Ensure the model is trained for the requested club context."""
        club_id = club.pk if isinstance(club, Club) else club
        if self._model is not None and self._last_frame is not None and club_id == self._last_club_id:
            return True
        return self.train(club=club)

    def _build_historical_points(self, frame: pd.DataFrame) -> List[ForecastPoint]:
        """Convert training frame rows into historical forecast points."""
        points: List[ForecastPoint] = []
        for _, row in frame.iterrows():
            year = int(row['year'])
            month = int(row['month'])
            points.append(
                ForecastPoint(
                    period=_month_as_date(year, month),
                    label=_format_month_label(year, month),
                    total=float(row['total_revenue']),
                    ticketing=float(row['ticketing']),
                    sponsorship=float(row['sponsorship']),
                    broadcasting=float(row['broadcasting']),
                    merchandising=float(row['merchandising']),
                    is_prediction=False,
                )
            )
        return points

    def _build_prediction_points(
        self,
        model: LinearRegression,
        frame: pd.DataFrame,
        periods: int,
    ) -> List[ForecastPoint]:
        """Generate forecast points for the specified number of future periods."""
        if frame.empty:
            return []

        last_year = int(frame.iloc[-1]['year'])
        last_month = int(frame.iloc[-1]['month'])
        last_index = float(frame.iloc[-1]['month_index'])
        future_indices = np.arange(last_index + 1, last_index + periods + 1, dtype=float).reshape(-1, 1)
        predictions = model.predict(future_indices)

        points: List[ForecastPoint] = []
        distribution = self._category_distribution
        if not distribution or sum(distribution.values()) <= 0:
            distribution = {column: 1.0 / len(CATEGORY_COLUMNS) for column in CATEGORY_COLUMNS}

        current_year, current_month = last_year, last_month
        for predicted_total in predictions:
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1

            total_value = max(0.0, float(predicted_total))
            category_values = {
                column: total_value * distribution.get(column, 0.0)
                for column in CATEGORY_COLUMNS
            }

            points.append(
                ForecastPoint(
                    period=_month_as_date(current_year, current_month),
                    label=_format_month_label(current_year, current_month),
                    total=total_value,
                    ticketing=float(category_values['ticketing']),
                    sponsorship=float(category_values['sponsorship']),
                    broadcasting=float(category_values['broadcasting']),
                    merchandising=float(category_values['merchandising']),
                    is_prediction=True,
                )
            )
        return points

    def forecast(
        self,
        club: Optional[Union[Club, int]] = None,
        periods: int = FORECAST_PERIODS,
    ) -> ForecastResult:
        """Return forecast result containing historical data and predictions."""
        has_model = self._ensure_trained(club=club)
        frame = self._last_frame if self._last_frame is not None else pd.DataFrame()
        historical = self._build_historical_points(frame)
        predictions: List[ForecastPoint] = []

        if has_model and self._model is not None:
            predictions = self._build_prediction_points(model=self._model, frame=frame, periods=periods)

        return ForecastResult(
            historical=historical,
            predictions=predictions,
            trained_samples=self._trained_samples,
            model_score=self._model_score,
            category_distribution=self._category_distribution,
            has_sufficient_data=has_model,
        )


_forecaster = RevenueForecaster()


def get_revenue_forecaster() -> RevenueForecaster:
    """Return shared RevenueForecaster instance."""
    return _forecaster


def forecast_revenue(
    club: Optional[Union[Club, int]] = None,
    periods: int = FORECAST_PERIODS,
) -> ForecastResult:
    """Convenience wrapper to forecast revenues for templates and views."""
    forecaster = get_revenue_forecaster()
    return forecaster.forecast(club=club, periods=periods)
