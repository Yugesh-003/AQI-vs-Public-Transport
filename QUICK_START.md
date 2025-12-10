# 🚀 Quick Start Guide

## One-Command Setup & Launch

### Option 1: Automatic Setup (Recommended)
```bash
python setup.py
```
This will:
- Install all dependencies
- Generate sample data
- Launch the dashboard automatically

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data
python data_fetcher.py

# Launch dashboard
streamlit run dashboard.py
```

### Option 3: Test First, Then Launch
```bash
# Run tests to verify everything works
python test_setup.py

# If tests pass, launch dashboard
streamlit run dashboard.py
```

## What You'll See

The dashboard will open in your web browser with:

1. **Key Metrics** - Overview of AQI and transport data
2. **Time Series** - Trends over time
3. **Correlations** - Statistical relationships
4. **Interactive Filters** - Date range and AQI threshold controls
5. **Insights** - Automated analysis and findings

## Sample Data

The project generates 90 days of realistic data:
- **AQI Data**: PM2.5, PM10, NO2, Ozone levels with seasonal patterns
- **Transport Data**: Bus and metro usage with weekday/weekend variations
- **Correlations**: Realistic relationships between air quality and transport usage

## Customization

- **Real AQI Data**: Modify `data_fetcher.py` to use OpenAQ API
- **Different Cities**: Change location parameters in AQI fetcher
- **More Transport Modes**: Extend the transport data generator
- **Additional Visualizations**: Add new plots in `dashboard.py`

## Troubleshooting

- **Port in use**: Streamlit will find another port automatically
- **Missing packages**: Run `pip install -r requirements.txt`
- **Data issues**: Delete CSV files and run `python data_fetcher.py` again

## Next Steps

1. Explore the interactive dashboard
2. Try different date ranges and filters
3. Examine the correlation analysis
4. Check out the weekly patterns
5. Customize with your own data sources

Happy analyzing! 📊