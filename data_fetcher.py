import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

class AQIDataFetcher:
    """Fetch real AQI data from OpenAQ API"""
    
    def __init__(self):
        self.base_url = "https://api.openaq.org/v2"
        
    def get_locations(self, country="US", limit=10):
        """Get available monitoring locations"""
        url = f"{self.base_url}/locations"
        params = {
            "country": country,
            "limit": limit,
            "order_by": "lastUpdated",
            "sort": "desc"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching locations: {e}")
            return None
    
    def fetch_measurements(self, location_id, date_from, date_to, parameters=None):
        """Fetch AQI measurements for a specific location and date range"""
        if parameters is None:
            parameters = ["pm25", "pm10", "no2", "o3"]
        
        url = f"{self.base_url}/measurements"
        params = {
            "location_id": location_id,
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "limit": 10000,
            "order_by": "datetime",
            "sort": "asc"
        }
        
        all_data = []
        
        for param in parameters:
            params["parameter"] = param
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "results" in data:
                    for measurement in data["results"]:
                        all_data.append({
                            "date": pd.to_datetime(measurement["date"]["utc"]).date(),
                            "parameter": measurement["parameter"],
                            "value": measurement["value"],
                            "unit": measurement["unit"],
                            "location": measurement["location"]
                        })
                
                # Rate limiting
                time.sleep(0.1)
                
            except requests.RequestException as e:
                print(f"Error fetching {param} data: {e}")
                continue
        
        return pd.DataFrame(all_data)
    
    def calculate_aqi_from_pm25(self, pm25_value):
        """Calculate AQI from PM2.5 concentration (US EPA standard)"""
        if pd.isna(pm25_value):
            return np.nan
        
        # US EPA AQI breakpoints for PM2.5 (24-hour average)
        breakpoints = [
            (0, 12.0, 0, 50),      # Good
            (12.1, 35.4, 51, 100), # Moderate
            (35.5, 55.4, 101, 150), # Unhealthy for Sensitive Groups
            (55.5, 150.4, 151, 200), # Unhealthy
            (150.5, 250.4, 201, 300), # Very Unhealthy
            (250.5, 500.4, 301, 500)  # Hazardous
        ]
        
        for c_low, c_high, i_low, i_high in breakpoints:
            if c_low <= pm25_value <= c_high:
                return int(((i_high - i_low) / (c_high - c_low)) * (pm25_value - c_low) + i_low)
        
        return 500  # Maximum AQI for values above 500.4

class TransportDataGenerator:
    """Generate realistic transport usage data"""
    
    def __init__(self, start_date, days=90):
        self.start_date = pd.to_datetime(start_date)
        self.days = days
        
    def generate_transport_data(self):
        """Generate simulated transport usage data with realistic patterns"""
        dates = pd.date_range(start=self.start_date, periods=self.days, freq='D')
        
        data = []
        
        for date in dates:
            # Base usage patterns
            weekday = date.weekday()  # 0=Monday, 6=Sunday
            is_weekend = weekday >= 5
            
            # Seasonal variation (higher usage in winter/poor weather)
            day_of_year = date.timetuple().tm_yday
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
            
            # Weekend vs weekday patterns
            if is_weekend:
                base_bus = np.random.normal(8000, 1500)
                base_metro = np.random.normal(12000, 2000)
            else:
                base_bus = np.random.normal(15000, 2500)
                base_metro = np.random.normal(25000, 3500)
            
            # Apply seasonal variation
            bus_passengers = max(0, int(base_bus * seasonal_factor))
            metro_passengers = max(0, int(base_metro * seasonal_factor))
            
            # Add some correlation with air quality (people use more transport on bad air days)
            # This will be enhanced when we merge with actual AQI data
            
            data.extend([
                {
                    'date': date.date(),
                    'mode': 'bus',
                    'number_of_passengers': bus_passengers
                },
                {
                    'date': date.date(),
                    'mode': 'metro',
                    'number_of_passengers': metro_passengers
                }
            ])
        
        return pd.DataFrame(data)

def save_sample_data():
    """Generate and save sample data for testing"""
    # Generate transport data
    transport_gen = TransportDataGenerator('2024-01-01', days=90)
    transport_df = transport_gen.generate_transport_data()
    transport_df.to_csv('sample_transport_data.csv', index=False)
    
    # Create sample AQI data (for testing when API is unavailable)
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    aqi_data = []
    
    for date in dates:
        # Generate realistic AQI values with some correlation to season
        day_of_year = date.timetuple().tm_yday
        base_aqi = 50 + 30 * np.sin(2 * np.pi * (day_of_year - 80) / 365)  # Seasonal variation
        aqi = max(0, int(np.random.normal(base_aqi, 20)))
        
        # Generate component pollutants
        pm25 = max(0, np.random.normal(15 + aqi * 0.3, 5))
        pm10 = max(0, np.random.normal(25 + aqi * 0.4, 8))
        no2 = max(0, np.random.normal(20 + aqi * 0.2, 6))
        o3 = max(0, np.random.normal(30 + aqi * 0.25, 7))
        
        aqi_data.append({
            'date': date.date(),
            'AQI': aqi,
            'PM2.5': pm25,
            'PM10': pm10,
            'NO2': no2,
            'Ozone': o3
        })
    
    aqi_df = pd.DataFrame(aqi_data)
    aqi_df.to_csv('sample_aqi_data.csv', index=False)
    
    print("Sample data generated successfully!")
    print(f"Transport data: {len(transport_df)} records")
    print(f"AQI data: {len(aqi_df)} records")

if __name__ == "__main__":
    save_sample_data()