"""
context formatting utilities for surf forecast models
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from backend.models import SurfForecast


def _fmt(v: Optional[float], decimals: int = 1) -> str:
    """Format optional float for display; use 'N/A' when missing."""
    if v is None:
        return "N/A"
    return f"{v:.{decimals}f}"


def _fmt_int(v: Optional[float]) -> str:
    """Format optional float as integer for display."""
    if v is None:
        return "N/A"
    return f"{int(round(v))}"


def format_forecast_to_llm_context(forecast: "SurfForecast") -> str:
    """
    format forecast as concise, human-readable text optimized for llm context

    args:
        forecast: SurfForecast model instance

    returns:
        formatted string suitable for llm consumption
    """
    from services.helpers import degrees_to_compass

    cc = forecast.current_conditions
    wd = _fmt_int(cc.wind_direction_deg) if cc.wind_direction_deg is not None else "N/A"
    sd = (
        _fmt_int(cc.swell_wave_direction_deg)
        if cc.swell_wave_direction_deg is not None
        else "N/A"
    )
    lines = [
        f"# Surf Forecast: {forecast.location}",
        "",
        "## Current Conditions",
        f"Waves: {_fmt(cc.wave_height_m)}m ({_fmt(cc.wave_period_s, 0)}s period)",
        f"  - Swell: {_fmt(cc.swell_wave_height_m)}m from {degrees_to_compass(cc.swell_wave_direction_deg or 0).upper()}",
        f"  - Wind waves: {_fmt(cc.wind_wave_height_m)}m",
        f"Wind: {_fmt_int(cc.wind_speed_knots)} knots from {degrees_to_compass(cc.wind_direction_deg or 0).upper()} (gusts {_fmt_int(cc.wind_gusts_knots)} knots)",
        f"Temperature: {_fmt_int(cc.temperature_c)}°C",
        "",
    ]

    # add hourly forecast if available
    if forecast.hourly_forecast:
        lines.append("## Next Hours")
        for hour in forecast.hourly_forecast:
            # parse timestamp to get readable time
            try:
                if "T" in hour.timestamp:
                    dt = datetime.fromisoformat(hour.timestamp.replace("Z", "+00:00"))
                    time_str = dt.strftime("%H:%M")
                else:
                    time_str = hour.timestamp[-5:]
            except:
                time_str = (
                    hour.timestamp.split("T")[1]
                    if "T" in hour.timestamp
                    else hour.timestamp[-5:]
                )

            swell_dir = degrees_to_compass(hour.swell_wave_direction_deg or 0).upper()
            wind_dir = degrees_to_compass(hour.wind_direction_deg or 0).upper()
            lines.append(
                f"{time_str}: {_fmt(hour.wave_height_m)}m waves (swell {_fmt(hour.swell_wave_height_m)}m from {swell_dir}), "
                f"{_fmt_int(hour.wind_speed_knots)}kn wind from {wind_dir}"
            )
        lines.append("")

    lines.append("## 5-Day Forecast")

    for day in forecast.forecast_5day:
        wave_dir = degrees_to_compass(day.wave_direction_dominant_deg or 0).upper()
        swell_dir = degrees_to_compass(
            day.swell_wave_direction_dominant_deg or 0
        ).upper()
        wind_dir = degrees_to_compass(day.wind_direction_dominant_deg or 0).upper()
        lines.extend(
            [
                f"{day.date}:",
                f"  Waves: {_fmt(day.wave_height_max_m)}m max (swell {_fmt(day.swell_wave_height_max_m)}m from {swell_dir})",
                f"  Wind: {_fmt_int(day.wind_speed_max_knots)} knots from {wind_dir}",
                f"  Temp: {_fmt_int(day.temperature_min_c)}-{_fmt_int(day.temperature_max_c)}°C",
            ]
        )

    return "\n".join(lines)
