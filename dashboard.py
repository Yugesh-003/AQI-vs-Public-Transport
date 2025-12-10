import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from data_fetcher import AQIDataFetcher, TransportDataGenerator, save_sample_data
from data_processor import DataProcessor
import os
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="AQI vs Transport Usage Dashboard",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process data with caching"""
    processor = DataProcessor()
    
    # Check if sample data exists, if not create it
    if not os.path.exists('sample_transport_data.csv') or not os.path.exists('sample_aqi_data.csv'):
        with st.spinner("Generating sample data..."):
            save_sample_data()
    
    # Load data
    transport_df = processor.load_transport_data('sample_transport_data.csv')
    aqi_df = processor.load_aqi_data('sample_aqi_data.csv')
    
    # Merge datasets
    merged_df = processor.merge_datasets(aqi_df, transport_df)
    
    # Calculate correlations
    correlations = processor.calculate_correlations(merged_df)
    
    # Get summary statistics
    summary_stats = processor.get_summary_statistics(merged_df)
    
    return merged_df, correlations, summary_stats, processor

def create_time_series_plot(df):
    """Create time series plot showing AQI and transport usage over time"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Air Quality Index Over Time', 'Transport Usage Over Time'),
        vertical_spacing=0.1,
        specs=[[{"secondary_y": False}], [{"secondary_y": True}]]
    )
    
    # AQI time series
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['AQI'],
            mode='lines',
            name='AQI',
            line=dict(color='red', width=2)
        ),
        row=1, col=1
    )
    
    # Transport usage time series
    if 'bus' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['bus'],
                mode='lines',
                name='Bus Passengers',
                line=dict(color='blue', width=2)
            ),
            row=2, col=1
        )
    
    if 'metro' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df['date'],
                y=df['metro'],
                mode='lines',
                name='Metro Passengers',
                line=dict(color='green', width=2),
                yaxis='y4'
            ),
            row=2, col=1
        )
    
    fig.update_layout(
        height=600,
        title_text="AQI and Transport Usage Trends",
        showlegend=True
    )
    
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="AQI", row=1, col=1)
    fig.update_yaxes(title_text="Bus Passengers", row=2, col=1)
    
    return fig

def create_correlation_heatmap(correlations):
    """Create correlation heatmap"""
    # Prepare data for heatmap
    corr_data = []
    for key, value in correlations.items():
        parts = key.split('_vs_')
        if len(parts) == 2:
            corr_data.append({
                'AQI_Metric': parts[0],
                'Transport_Metric': parts[1],
                'Correlation': value['correlation']
            })
    
    if not corr_data:
        return None
    
    corr_df = pd.DataFrame(corr_data)
    pivot_corr = corr_df.pivot(index='AQI_Metric', columns='Transport_Metric', values='Correlation')
    
    fig = px.imshow(
        pivot_corr,
        color_continuous_scale='RdBu_r',
        aspect='auto',
        title='Correlation Matrix: AQI Metrics vs Transport Usage'
    )
    
    fig.update_layout(height=400)
    return fig

def create_scatter_plot(df, x_col, y_col):
    """Create scatter plot with trend line"""
    fig = px.scatter(
        df, 
        x=x_col, 
        y=y_col,
        color='AQI_Category' if 'AQI_Category' in df.columns else None,
        trendline='ols',
        title=f'{y_col} vs {x_col}',
        hover_data=['date'] if 'date' in df.columns else None
    )
    
    fig.update_layout(height=400)
    return fig

def create_box_plot(df):
    """Create box plot showing transport usage by AQI category"""
    if 'AQI_Category' not in df.columns:
        return None
    
    fig = go.Figure()
    
    categories = df['AQI_Category'].unique()
    colors = px.colors.qualitative.Set3
    
    for i, category in enumerate(categories):
        if pd.notna(category):
            category_data = df[df['AQI_Category'] == category]
            fig.add_trace(go.Box(
                y=category_data['total_passengers'],
                name=category,
                marker_color=colors[i % len(colors)]
            ))
    
    fig.update_layout(
        title='Transport Usage Distribution by AQI Category',
        xaxis_title='AQI Category',
        yaxis_title='Total Passengers',
        height=400
    )
    
    return fig

def create_weekly_pattern_plot(df):
    """Create weekly pattern analysis"""
    weekly_stats = df.groupby('day_of_week').agg({
        'AQI': 'mean',
        'total_passengers': 'mean'
    }).reset_index()
    
    # Reorder days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_stats['day_of_week'] = pd.Categorical(weekly_stats['day_of_week'], categories=day_order, ordered=True)
    weekly_stats = weekly_stats.sort_values('day_of_week')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Average AQI by Day of Week', 'Average Transport Usage by Day of Week')
    )
    
    fig.add_trace(
        go.Bar(x=weekly_stats['day_of_week'], y=weekly_stats['AQI'], name='AQI', marker_color='red'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=weekly_stats['day_of_week'], y=weekly_stats['total_passengers'], name='Transport Usage', marker_color='blue'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🚌 AQI vs Public Transport Usage Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    try:
        df, correlations, summary_stats, processor = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Date range filter
    if not df.empty:
        min_date = df['date'].min()
        max_date = df['date'].max()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        else:
            df_filtered = df
    else:
        df_filtered = df
    
    # AQI threshold filter
    if 'AQI' in df_filtered.columns:
        aqi_threshold = st.sidebar.slider(
            "AQI Threshold",
            min_value=int(df_filtered['AQI'].min()),
            max_value=int(df_filtered['AQI'].max()),
            value=int(df_filtered['AQI'].max())
        )
        df_filtered = df_filtered[df_filtered['AQI'] <= aqi_threshold]
    
    # Main dashboard
    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
        return
    
    # Key metrics
    st.header("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_aqi = df_filtered['AQI'].mean()
        st.metric("Average AQI", f"{avg_aqi:.1f}")
    
    with col2:
        total_passengers = df_filtered['total_passengers'].sum()
        st.metric("Total Passengers", f"{total_passengers:,.0f}")
    
    with col3:
        high_aqi_days = len(df_filtered[df_filtered['AQI'] > 100])
        st.metric("High AQI Days (>100)", high_aqi_days)
    
    with col4:
        data_days = len(df_filtered)
        st.metric("Days of Data", data_days)
    
    # Time series plots
    st.header("📈 Time Series Analysis")
    time_series_fig = create_time_series_plot(df_filtered)
    st.plotly_chart(time_series_fig, use_container_width=True)
    
    # Correlation analysis
    st.header("🔗 Correlation Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Correlation heatmap
        corr_fig = create_correlation_heatmap(correlations)
        if corr_fig:
            st.plotly_chart(corr_fig, use_container_width=True)
        else:
            st.info("Correlation data not available")
    
    with col2:
        # Key correlations
        st.subheader("Key Correlations")
        for key, value in correlations.items():
            if 'total_passengers' in key:
                corr_val = value['correlation']
                significance = "✅" if value['significant'] else "❌"
                st.write(f"{key.replace('_', ' ').title()}: {corr_val:.3f} {significance}")
    
    # Scatter plots
    st.header("🎯 Relationship Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'AQI' in df_filtered.columns and 'total_passengers' in df_filtered.columns:
            scatter_fig = create_scatter_plot(df_filtered, 'AQI', 'total_passengers')
            st.plotly_chart(scatter_fig, use_container_width=True)
    
    with col2:
        box_fig = create_box_plot(df_filtered)
        if box_fig:
            st.plotly_chart(box_fig, use_container_width=True)
    
    # Weekly patterns
    st.header("📅 Weekly Patterns")
    weekly_fig = create_weekly_pattern_plot(df_filtered)
    st.plotly_chart(weekly_fig, use_container_width=True)
    
    # Insights
    st.header("💡 Key Insights")
    
    # Calculate insights
    insights = []
    
    # AQI insights
    if 'AQI' in df_filtered.columns:
        avg_aqi = df_filtered['AQI'].mean()
        if avg_aqi > 100:
            insights.append(f"⚠️ Average AQI ({avg_aqi:.1f}) indicates unhealthy air quality")
        elif avg_aqi > 50:
            insights.append(f"⚡ Average AQI ({avg_aqi:.1f}) indicates moderate air quality")
        else:
            insights.append(f"✅ Average AQI ({avg_aqi:.1f}) indicates good air quality")
    
    # Correlation insights
    aqi_transport_corr = correlations.get('AQI_vs_total_passengers', {}).get('correlation', 0)
    if abs(aqi_transport_corr) > 0.3:
        direction = "positive" if aqi_transport_corr > 0 else "negative"
        insights.append(f"📊 Strong {direction} correlation ({aqi_transport_corr:.3f}) between AQI and transport usage")
    elif abs(aqi_transport_corr) > 0.1:
        direction = "positive" if aqi_transport_corr > 0 else "negative"
        insights.append(f"📊 Moderate {direction} correlation ({aqi_transport_corr:.3f}) between AQI and transport usage")
    else:
        insights.append(f"📊 Weak correlation ({aqi_transport_corr:.3f}) between AQI and transport usage")
    
    # Weekend vs weekday
    if 'is_weekend' in df_filtered.columns:
        weekend_avg = df_filtered[df_filtered['is_weekend']]['total_passengers'].mean()
        weekday_avg = df_filtered[~df_filtered['is_weekend']]['total_passengers'].mean()
        if weekday_avg > weekend_avg * 1.2:
            insights.append(f"🚌 Weekday transport usage ({weekday_avg:.0f}) significantly higher than weekends ({weekend_avg:.0f})")
    
    for insight in insights:
        st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    # Data summary
    with st.expander("📋 Data Summary"):
        st.json(summary_stats)
    
    # Raw data
    with st.expander("🔍 Raw Data"):
        st.dataframe(df_filtered)

if __name__ == "__main__":
    main()