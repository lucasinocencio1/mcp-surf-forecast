import pytest
from pydantic import ValidationError

from backend.context import format_forecast_to_llm_context
from backend.models import (
    CurrentConditions,
    DailyForecast,
    MarineDaily,
    MarineHourly,
    MarineResponse,
    SurfForecast,
    WeatherDaily,
    WeatherHourly,
    WeatherResponse,
)
from services.forecast import ForecastService


def _marine_response():
    return MarineResponse(
        hourly=MarineHourly(
            time=[
                "2026-02-10T00:00",
                "2026-02-10T01:00",
                "2026-02-10T02:00",
                "2026-02-10T03:00",
                "2026-02-10T04:00",
            ],
            wave_height=[1.0, None, 2.0, None, 1.5],
            wave_direction=[10, None, 20, 30, 40],
            wave_period=[8, 9, 10, 11, 12],
            wind_wave_height=[0.3, 0.3, 0.4, 0.4, 0.5],
            wind_wave_direction=[50, 60, 70, 80, 90],
            wind_wave_period=[5, 5, 6, 6, 7],
            swell_wave_height=[0.7, 0.8, 0.9, 1.0, 1.1],
            swell_wave_direction=[200, 210, 220, 230, 240],
            swell_wave_period=[12, 12, 13, 13, 14],
        ),
        daily=MarineDaily(
            time=["2026-02-10", "2026-02-11"],
            wave_height_max=[2.0, 3.0],
            wave_direction_dominant=[280, 290],
            wave_period_max=[10, 11],
            wind_wave_height_max=[0.8, 1.0],
            wind_wave_direction_dominant=[260, 270],
            wind_wave_period_max=[6, 7],
            swell_wave_height_max=[1.5, 2.0],
            swell_wave_direction_dominant=[300, 310],
            swell_wave_period_max=[12, 13],
        ),
    )


def _weather_response():
    return WeatherResponse(
        hourly=WeatherHourly(
            time=["2026-02-10T00:00", "2026-02-10T01:00"],
            temperature_2m=[20.0, None],
            windspeed_10m=[5.0, None],
            winddirection_10m=[180.0, None],
            windgusts_10m=[8.0, None],
        ),
        daily=WeatherDaily(
            time=["2026-02-10", "2026-02-11"],
            temperature_2m_max=[22.0, 23.0],
            temperature_2m_min=[18.0, 17.0],
            windspeed_10m_max=[10.0, 11.0],
            winddirection_10m_dominant=[190.0, 200.0],
            windgusts_10m_max=[15.0, 16.0],
        ),
    )


def test_parse_forecast_handles_missing_weather_values():
    marine = _marine_response()
    weather = _weather_response()

    forecast = ForecastService.parse_forecast_data(
        marine, weather, "Test Beach", 10.0, 20.0
    )

    assert forecast.current_conditions.wind_speed_knots == 5.0
    assert len(forecast.hourly_forecast) == 1
    assert forecast.hourly_forecast[0].wind_speed_knots is None


def test_forecast_days_must_be_chronological():
    with pytest.raises(ValidationError):
        SurfForecast(
            location="Test",
            latitude=0.0,
            longitude=0.0,
            current_conditions=CurrentConditions(
                timestamp="2026-02-10T00:00",
                wave_height_m=1.0,
                swell_wave_height_m=0.8,
                wind_wave_height_m=0.2,
                wave_direction_deg=10.0,
                swell_wave_direction_deg=20.0,
                wave_period_s=9.0,
                swell_wave_period_s=10.0,
                wind_speed_knots=5.0,
                wind_direction_deg=180.0,
                wind_gusts_knots=8.0,
                temperature_c=20.0,
            ),
            hourly_forecast=[],
            forecast_5day=[
                DailyForecast(
                    date="2026-02-11",
                    wave_height_max_m=2.0,
                    swell_wave_height_max_m=1.5,
                    wind_wave_height_max_m=0.6,
                    wave_direction_dominant_deg=280.0,
                    swell_wave_direction_dominant_deg=290.0,
                    wave_period_max_s=10.0,
                    swell_wave_period_max_s=12.0,
                    wind_speed_max_knots=10.0,
                    wind_direction_dominant_deg=200.0,
                    wind_gusts_max_knots=15.0,
                    temperature_max_c=22.0,
                    temperature_min_c=18.0,
                ),
                DailyForecast(
                    date="2026-02-10",
                    wave_height_max_m=2.5,
                    swell_wave_height_max_m=1.8,
                    wind_wave_height_max_m=0.7,
                    wave_direction_dominant_deg=270.0,
                    swell_wave_direction_dominant_deg=280.0,
                    wave_period_max_s=9.0,
                    swell_wave_period_max_s=11.0,
                    wind_speed_max_knots=11.0,
                    wind_direction_dominant_deg=210.0,
                    wind_gusts_max_knots=16.0,
                    temperature_max_c=21.0,
                    temperature_min_c=17.0,
                ),
            ],
            surf_quality_notes="ok",
        )


def test_llm_context_shows_na_for_missing_values():
    forecast = SurfForecast(
        location="Test",
        latitude=0.0,
        longitude=0.0,
        current_conditions=CurrentConditions(
            timestamp="2026-02-10T00:00",
            wave_height_m=None,
            swell_wave_height_m=None,
            wind_wave_height_m=None,
            wave_direction_deg=None,
            swell_wave_direction_deg=None,
            wave_period_s=None,
            swell_wave_period_s=None,
            wind_speed_knots=None,
            wind_direction_deg=None,
            wind_gusts_knots=None,
            temperature_c=None,
        ),
        hourly_forecast=[],
        forecast_5day=[
            DailyForecast(
                date="2026-02-10",
                wave_height_max_m=None,
                swell_wave_height_max_m=None,
                wind_wave_height_max_m=None,
                wave_direction_dominant_deg=None,
                swell_wave_direction_dominant_deg=None,
                wave_period_max_s=None,
                swell_wave_period_max_s=None,
                wind_speed_max_knots=None,
                wind_direction_dominant_deg=None,
                wind_gusts_max_knots=None,
                temperature_max_c=None,
                temperature_min_c=None,
            )
        ],
        surf_quality_notes="data missing",
    )

    text = format_forecast_to_llm_context(forecast)
    assert "N/A" in text
