"""
surf forecast service - business logic for combining and interpreting data
"""

from backend.models import (
    CurrentConditions,
    DailyForecast,
    SurfForecast,
    MarineResponse,
    WeatherResponse
)


class ForecastService:
    """service for processing and interpreting surf forecast data"""
    
    @staticmethod
    def assess_surf_quality(current: dict, forecast: list[dict]) -> str:
        """
        provide surf quality assessment based on wave and wind data
        
        args:
            current: current conditions dictionary
            forecast: list of daily forecast dictionaries
        
        returns:
            human-readable surf quality assessment string
        """
        wave_height = current.get('wave_height_m') or 0
        swell_height = current.get('swell_wave_height_m') or 0
        period = current.get('wave_period_s') or 0
        wind_speed = current.get('wind_speed_knots') or 0
        
        notes = []
        
        # wave height assessment
        if wave_height < 0.5:
            notes.append("very small waves - flat conditions")
        elif wave_height < 1.0:
            notes.append("small waves - suitable for beginners")
        elif wave_height < 2.0:
            notes.append("good wave height for most surfers")
        elif wave_height < 3.0:
            notes.append("solid waves - intermediate to advanced")
        else:
            notes.append("big waves - advanced surfers only")
        
        # wind conditions assessment
        if wind_speed < 5:
            notes.append("light winds - glassy conditions")
        elif wind_speed < 10:
            notes.append("light breeze - good conditions")
        elif wind_speed < 15:
            notes.append("moderate wind - textured surface")
        elif wind_speed < 20:
            notes.append("strong wind - challenging conditions")
        else:
            notes.append("very strong wind - difficult surfing")
        
        # swell quality
        if period > 12:
            notes.append("long period swell - clean waves expected")
        elif period > 8:
            notes.append("moderate period - decent wave quality")
        else:
            notes.append("short period - choppy conditions likely")
        
        # swell vs wind wave ratio
        if swell_height > 0 and wave_height > 0:
            swell_ratio = swell_height / wave_height
            if swell_ratio > 0.7:
                notes.append("swell dominant - cleaner conditions")
            else:
                notes.append("wind waves present - may be choppy")
        
        return " | ".join(notes)
    
    @staticmethod
    def parse_forecast_data(
        marine_data: MarineResponse,
        weather_data: WeatherResponse,
        location_name: str, 
        latitude: float, 
        longitude: float
    ) -> SurfForecast:
        """
        parse the validated api responses into structured surf forecast
        
        args:
            marine_data: validated marine api response
            weather_data: validated weather api response
            location_name: full location name
            latitude: latitude coordinate
            longitude: longitude coordinate
        
        returns:
            validated structured SurfForecast object
            
        raises:
            ValidationError: if constructed models fail validation
        """
        # get current conditions (first hourly data point)
        current_idx = 0
        def _v(lst, i):
            if i < len(lst):
                v = lst[i]
                return v if v is not None else None
            return None

        current = CurrentConditions(
            timestamp=marine_data.hourly.time[current_idx],
            wave_height_m=_v(marine_data.hourly.wave_height, current_idx),
            swell_wave_height_m=_v(marine_data.hourly.swell_wave_height, current_idx),
            wind_wave_height_m=_v(marine_data.hourly.wind_wave_height, current_idx),
            wave_direction_deg=_v(marine_data.hourly.wave_direction, current_idx),
            swell_wave_direction_deg=_v(marine_data.hourly.swell_wave_direction, current_idx),
            wave_period_s=_v(marine_data.hourly.wave_period, current_idx),
            swell_wave_period_s=_v(marine_data.hourly.swell_wave_period, current_idx),
            wind_speed_knots=_v(weather_data.hourly.windspeed_10m, current_idx),
            wind_direction_deg=_v(weather_data.hourly.winddirection_10m, current_idx),
            wind_gusts_knots=_v(weather_data.hourly.windgusts_10m, current_idx),
            temperature_c=_v(weather_data.hourly.temperature_2m, current_idx),
        )
        
        # get next 6 hours (every 3 hours: +3, +6, +9, +12 hours)
        hourly_forecasts = []
        for hour_idx in [3, 6, 9, 12]:
            if hour_idx < len(marine_data.hourly.time):
                hour_forecast = CurrentConditions(
                    timestamp=marine_data.hourly.time[hour_idx],
                    wave_height_m=_v(marine_data.hourly.wave_height, hour_idx),
                    swell_wave_height_m=_v(marine_data.hourly.swell_wave_height, hour_idx),
                    wind_wave_height_m=_v(marine_data.hourly.wind_wave_height, hour_idx),
                    wave_direction_deg=_v(marine_data.hourly.wave_direction, hour_idx),
                    swell_wave_direction_deg=_v(marine_data.hourly.swell_wave_direction, hour_idx),
                    wave_period_s=_v(marine_data.hourly.wave_period, hour_idx),
                    swell_wave_period_s=_v(marine_data.hourly.swell_wave_period, hour_idx),
                    wind_speed_knots=_v(weather_data.hourly.windspeed_10m, hour_idx),
                    wind_direction_deg=_v(weather_data.hourly.winddirection_10m, hour_idx),
                    wind_gusts_knots=_v(weather_data.hourly.windgusts_10m, hour_idx),
                    temperature_c=_v(weather_data.hourly.temperature_2m, hour_idx),
                )
                hourly_forecasts.append(hour_forecast)
        
        # get 5 day forecast
        forecast_days = []
        for i in range(min(5, len(marine_data.daily.time))):
            day_forecast = DailyForecast(
                date=marine_data.daily.time[i],
                wave_height_max_m=_v(marine_data.daily.wave_height_max, i),
                swell_wave_height_max_m=_v(marine_data.daily.swell_wave_height_max, i),
                wind_wave_height_max_m=_v(marine_data.daily.wind_wave_height_max, i),
                wave_direction_dominant_deg=_v(marine_data.daily.wave_direction_dominant, i),
                swell_wave_direction_dominant_deg=_v(marine_data.daily.swell_wave_direction_dominant, i),
                wave_period_max_s=_v(marine_data.daily.wave_period_max, i),
                swell_wave_period_max_s=_v(marine_data.daily.swell_wave_period_max, i),
                wind_speed_max_knots=_v(weather_data.daily.windspeed_10m_max, i),
                wind_direction_dominant_deg=_v(weather_data.daily.winddirection_10m_dominant, i),
                wind_gusts_max_knots=_v(weather_data.daily.windgusts_10m_max, i),
                temperature_max_c=_v(weather_data.daily.temperature_2m_max, i),
                temperature_min_c=_v(weather_data.daily.temperature_2m_min, i),
            )
            forecast_days.append(day_forecast)
        
        # assess surf quality
        current_dict = current.model_dump()
        forecast_dict = [f.model_dump() for f in forecast_days]
        quality_notes = ForecastService.assess_surf_quality(current_dict, forecast_dict)
        
        return SurfForecast(
            location=location_name,
            latitude=latitude,
            longitude=longitude,
            current_conditions=current,
            hourly_forecast=hourly_forecasts,
            forecast_5day=forecast_days,
            surf_quality_notes=quality_notes
        )
