# AQI vs Public Transport Usage Dashboard

A comprehensive data dashboard that examines the relationship between Air Quality Index (AQI) and daily public transport usage. This project fetches real AQI data from public APIs, generates realistic transport usage data, and provides interactive visualizations to analyze correlations and trends.

## Features

- **Real AQI Data**: Fetches air quality data from OpenAQ API
- **Simulated Transport Data**: Generates realistic 90+ days of transport usage data
- **Interactive Dashboard**: Built with Streamlit for easy exploration
- **Comprehensive Analysis**: Correlation analysis, time series plots, and statistical insights
- **Multiple Visualizations**: Time series, scatter plots, box plots, heatmaps, and more

## Project Structure

```
├── dashboard.py           # Main Streamlit dashboard application
├── data_fetcher.py       # AQI data fetching and transport data generation
├── data_processor.py     # Data cleaning, processing, and analysis
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── sample_aqi_data.csv  # Generated sample AQI data (created on first run)
└── sample_transport_data.csv  # Generated sample transport data (created on first run)
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

If you have the files, ensure they're in a single directory.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will automatically:
1. Generate sample data on first run (90 days of transport and AQI data)
2. Process and merge the datasets
3. Launch the interactive dashboard in your web browser

## Usage Instructions

### Dashboard Features

1. **Key Metrics**: Overview of average AQI, total passengers, and data coverage
2. **Time Series Analysis**: Visualize AQI and transport usage trends over time
3. **Correlation Analysis**: Heatmap and statistical correlations between variables
4. **Relationship Analysis**: Scatter plots and box plots showing relationships
5. **Weekly Patterns**: Analysis of usage patterns by day of week
6. **Interactive Filters**: Date range and AQI threshold filters in sidebar

### Dashboard Controls

- **Date Range Filter**: Select specific time periods for analysis
- **AQI Threshold**: Filter data by maximum AQI values
- **Expandable Sections**: View raw data and detailed statistics

## Data Sources

### AQI Data
- **Source**: OpenAQ API (https://api.openaq.org/)
- **Parameters**: PM2.5, PM10, NO2, Ozone
- **Coverage**: 90+ days of historical data
- **Fallback**: Sample data generated if API is unavailable

### Transport Data (Simulated)
- **Bus Usage**: Realistic passenger counts with weekday/weekend patterns
- **Metro Usage**: Higher capacity with seasonal variations
- **Patterns**: Includes seasonal trends and day-of-week effects

## Key Metrics Analyzed

### Air Quality Metrics
- **AQI**: Overall Air Quality Index (0-500 scale)
- **PM2.5**: Fine particulate matter (μg/m³)
- **PM10**: Coarse particulate matter (μg/m³)
- **NO2**: Nitrogen dioxide (ppb)
- **Ozone**: Ground-level ozone (ppb)

### Transport Metrics
- **Bus Passengers**: Daily bus ridership
- **Metro Passengers**: Daily metro/subway ridership
- **Total Passengers**: Combined public transport usage

### Analysis Features
- **Correlation Analysis**: Pearson correlation coefficients
- **Temporal Patterns**: Weekly and seasonal trends
- **AQI Categories**: Good, Moderate, Unhealthy classifications
- **Statistical Significance**: P-values for correlation tests

## Customization

### Adding Real AQI Data

To use real AQI data instead of simulated data:

1. Modify `data_fetcher.py` to use the `AQIDataFetcher` class
2. Get available locations: `fetcher.get_locations(country="US")`
3. Fetch measurements: `fetcher.fetch_measurements(location_id, start_date, end_date)`

### Extending Transport Data

To add more realistic transport data:

1. Modify `TransportDataGenerator` in `data_fetcher.py`
2. Add weather correlation factors
3. Include special events or holidays
4. Add more transport modes (bike share, ride share, etc.)

### Dashboard Customization

The dashboard can be extended with:

- Additional visualization types
- Machine learning predictions
- Real-time data updates
- Export functionality
- Advanced filtering options

## Technical Details

### Data Processing Pipeline

1. **Data Generation/Fetching**: Create or fetch AQI and transport data
2. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
3. **Data Merging**: Combine datasets on date with proper alignment
4. **Feature Engineering**: Add temporal features, categories, and lag variables
5. **Analysis**: Calculate correlations, statistics, and insights
6. **Visualization**: Create interactive plots and dashboards

### Performance Considerations

- **Caching**: Streamlit caching for data loading and processing
- **Efficient Processing**: Pandas operations optimized for performance
- **Memory Management**: Appropriate data types and chunking for large datasets

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Run `pip install -r requirements.txt`
2. **Port Already in Use**: Streamlit will automatically find an available port
3. **Data Loading Errors**: Sample data will be generated automatically on first run
4. **API Rate Limits**: The OpenAQ API has rate limits; sample data is used as fallback

### Performance Tips

- Use date range filters for large datasets
- Close unused browser tabs running the dashboard
- Restart the dashboard if memory usage becomes high

## Future Enhancements

- **Real-time Data**: Live AQI and transport data feeds
- **Machine Learning**: Predictive models for transport usage based on AQI
- **Geographic Analysis**: Multi-city comparisons
- **Weather Integration**: Include weather data as additional factor
- **Mobile Optimization**: Responsive design for mobile devices
- **Data Export**: CSV/Excel export functionality
- **Advanced Analytics**: Seasonal decomposition, anomaly detection

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For questions or issues, please check the troubleshooting section or open an issue in the project repository.