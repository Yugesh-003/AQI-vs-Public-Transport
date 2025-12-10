import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """Process and merge AQI and transport data"""
    
    def __init__(self):
        self.merged_data = None
        
    def load_transport_data(self, filepath_or_df):
        """Load transport usage data"""
        if isinstance(filepath_or_df, str):
            df = pd.read_csv(filepath_or_df)
        else:
            df = filepath_or_df.copy()
        
        df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    
    def load_aqi_data(self, filepath_or_df):
        """Load AQI data"""
        if isinstance(filepath_or_df, str):
            df = pd.read_csv(filepath_or_df)
        else:
            df = filepath_or_df.copy()
        
        df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    
    def process_aqi_data(self, aqi_df):
        """Process and clean AQI data"""
        # Handle missing values
        numeric_cols = ['AQI', 'PM2.5', 'PM10', 'NO2', 'Ozone']
        
        for col in numeric_cols:
            if col in aqi_df.columns:
                # Fill missing values with interpolation
                aqi_df[col] = aqi_df[col].interpolate(method='linear')
                # Fill remaining NaN with median
                aqi_df[col] = aqi_df[col].fillna(aqi_df[col].median())
        
        # Create AQI categories
        aqi_df['AQI_Category'] = pd.cut(
            aqi_df['AQI'], 
            bins=[0, 50, 100, 150, 200, 300, 500],
            labels=['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous'],
            include_lowest=True
        )
        
        # Add day of week and month
        aqi_df['date_dt'] = pd.to_datetime(aqi_df['date'])
        aqi_df['day_of_week'] = aqi_df['date_dt'].dt.day_name()
        aqi_df['month'] = aqi_df['date_dt'].dt.month_name()
        aqi_df['is_weekend'] = aqi_df['date_dt'].dt.weekday >= 5
        
        return aqi_df
    
    def process_transport_data(self, transport_df):
        """Process and clean transport data"""
        # Add temporal features
        transport_df['date_dt'] = pd.to_datetime(transport_df['date'])
        transport_df['day_of_week'] = transport_df['date_dt'].dt.day_name()
        transport_df['month'] = transport_df['date_dt'].dt.month_name()
        transport_df['is_weekend'] = transport_df['date_dt'].dt.weekday >= 5
        
        # Pivot to have bus and metro as separate columns
        transport_pivot = transport_df.pivot_table(
            index=['date', 'date_dt', 'day_of_week', 'month', 'is_weekend'],
            columns='mode',
            values='number_of_passengers',
            aggfunc='sum'
        ).reset_index()
        
        # Flatten column names
        transport_pivot.columns.name = None
        
        # Calculate total passengers
        transport_pivot['total_passengers'] = (
            transport_pivot.get('bus', 0) + transport_pivot.get('metro', 0)
        )
        
        return transport_pivot
    
    def merge_datasets(self, aqi_df, transport_df):
        """Merge AQI and transport datasets on date"""
        # Process both datasets
        aqi_processed = self.process_aqi_data(aqi_df)
        transport_processed = self.process_transport_data(transport_df)
        
        # Merge on date
        merged = pd.merge(
            aqi_processed,
            transport_processed,
            on='date',
            how='inner',
            suffixes=('_aqi', '_transport')
        )
        
        # Clean up duplicate columns
        merged['day_of_week'] = merged['day_of_week_aqi']
        merged['month'] = merged['month_aqi']
        merged['is_weekend'] = merged['is_weekend_aqi']
        
        # Drop duplicate columns
        cols_to_drop = [col for col in merged.columns if col.endswith('_aqi') or col.endswith('_transport')]
        merged = merged.drop(columns=cols_to_drop)
        
        # Sort by date
        merged = merged.sort_values('date').reset_index(drop=True)
        
        self.merged_data = merged
        return merged
    
    def calculate_correlations(self, merged_df=None):
        """Calculate correlations between AQI and transport usage"""
        if merged_df is None:
            merged_df = self.merged_data
        
        if merged_df is None:
            raise ValueError("No merged data available. Run merge_datasets first.")
        
        # Select numeric columns for correlation
        aqi_cols = ['AQI', 'PM2.5', 'PM10', 'NO2', 'Ozone']
        transport_cols = ['bus', 'metro', 'total_passengers']
        
        # Filter existing columns
        aqi_cols = [col for col in aqi_cols if col in merged_df.columns]
        transport_cols = [col for col in transport_cols if col in merged_df.columns]
        
        correlations = {}
        
        for aqi_col in aqi_cols:
            for transport_col in transport_cols:
                if aqi_col in merged_df.columns and transport_col in merged_df.columns:
                    corr_coef, p_value = stats.pearsonr(
                        merged_df[aqi_col].dropna(),
                        merged_df[transport_col].dropna()
                    )
                    correlations[f"{aqi_col}_vs_{transport_col}"] = {
                        'correlation': corr_coef,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }
        
        return correlations
    
    def get_summary_statistics(self, merged_df=None):
        """Get summary statistics for the merged dataset"""
        if merged_df is None:
            merged_df = self.merged_data
        
        if merged_df is None:
            raise ValueError("No merged data available. Run merge_datasets first.")
        
        summary = {
            'total_days': len(merged_df),
            'date_range': {
                'start': merged_df['date'].min(),
                'end': merged_df['date'].max()
            },
            'aqi_stats': {},
            'transport_stats': {}
        }
        
        # AQI statistics
        aqi_cols = ['AQI', 'PM2.5', 'PM10', 'NO2', 'Ozone']
        for col in aqi_cols:
            if col in merged_df.columns:
                summary['aqi_stats'][col] = {
                    'mean': merged_df[col].mean(),
                    'median': merged_df[col].median(),
                    'std': merged_df[col].std(),
                    'min': merged_df[col].min(),
                    'max': merged_df[col].max()
                }
        
        # Transport statistics
        transport_cols = ['bus', 'metro', 'total_passengers']
        for col in transport_cols:
            if col in merged_df.columns:
                summary['transport_stats'][col] = {
                    'mean': merged_df[col].mean(),
                    'median': merged_df[col].median(),
                    'std': merged_df[col].std(),
                    'min': merged_df[col].min(),
                    'max': merged_df[col].max()
                }
        
        # AQI category distribution
        if 'AQI_Category' in merged_df.columns:
            summary['aqi_category_distribution'] = merged_df['AQI_Category'].value_counts().to_dict()
        
        return summary
    
    def add_lag_features(self, merged_df=None, lag_days=[1, 3, 7]):
        """Add lagged features for time series analysis"""
        if merged_df is None:
            merged_df = self.merged_data.copy()
        
        if merged_df is None:
            raise ValueError("No merged data available. Run merge_datasets first.")
        
        # Sort by date to ensure proper lagging
        merged_df = merged_df.sort_values('date').reset_index(drop=True)
        
        # Add lagged AQI features
        for lag in lag_days:
            merged_df[f'AQI_lag_{lag}'] = merged_df['AQI'].shift(lag)
            merged_df[f'total_passengers_lag_{lag}'] = merged_df['total_passengers'].shift(lag)
        
        # Add rolling averages
        for window in [3, 7, 14]:
            merged_df[f'AQI_rolling_{window}d'] = merged_df['AQI'].rolling(window=window, min_periods=1).mean()
            merged_df[f'total_passengers_rolling_{window}d'] = merged_df['total_passengers'].rolling(window=window, min_periods=1).mean()
        
        return merged_df