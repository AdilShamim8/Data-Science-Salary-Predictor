import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Data Science Salary Explorer",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS styling with additional elements for footer and improved consistency
st.markdown("""
<style>
    /* Global styles */
    body {
        font-family: 'Arial', sans-serif;
        color: #374151;
        background-color: #F9FAFB;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Header styles */
    .main-header {
        font-size: 2.8rem;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 800;
        display: block;
        letter-spacing: -0.5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    
    .sub-header {
        font-size: 1.6rem;
        color: #1e3a8a;
        margin-top: 2.2rem;
        margin-bottom: 1.2rem;
        font-weight: 700;
        display: block;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
    }
    
    /* Container Styles */
    .insight-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        display: block;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .metric-container {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        padding: 20px;
        margin-bottom: 15px;
        display: block;
        border-left: 4px solid #1e3a8a;
        transition: transform 0.2s ease-in-out;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
    }
    
    /* Text Styles */
    p, h1, h2, h3, h4, h5, h6 {
        display: block !important;
    }
    
    /* Chart Containers */
    .chart-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-12oz5g7 {
        background-color: #f1f5f9;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        border: 1px solid #e5e7eb;
        border-bottom: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a !important;
        color: white !important;
    }
    
    /* Footer styles */
    .footer-container {
        background-color: #F1F5F9;
        border-radius: 0.75rem;
        padding: 2rem;
        margin-top: 3rem;
        margin-bottom: 1rem;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        border-top: 4px solid #3B82F6;
    }
    
    .footer-section h4 {
        font-size: 1.1rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 0.5rem;
    }
    
    .footer-section p, .footer-section li {
        font-size: 0.9rem;
        color: #4B5563;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .footer-section ul {
        padding-left: 1.25rem;
        margin-top: 0.5rem;
    }
    
    .footer-copyright {
        grid-column: 1 / -1;
        text-align: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #E5E7EB;
    }
    
    .footer-copyright p {
        font-size: 0.9rem;
        color: #6B7280;
        margin-bottom: 0.25rem;
    }
    
    .version-info {
        font-size: 0.8rem !important;
        color: #9CA3AF !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .footer-container {
            grid-template-columns: 1fr;
        }
        
        .main-header {
            font-size: 2rem;
        }
        
        .sub-header {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('salaries.csv')
    # Convert salary_in_usd to numeric, handling any errors
    df['salary_in_usd'] = pd.to_numeric(df['salary_in_usd'], errors='coerce')
    
    # Remove outliers with salaries above 800,000 USD
    df = df[df['salary_in_usd'] <= 800000]
    
    # Create experience level mapping for better readability
    df['experience_level_full'] = df['experience_level'].map({
        'EN': 'Entry Level',
        'MI': 'Mid Level',
        'SE': 'Senior Level',
        'EX': 'Executive Level'
    })
    
    # Create employment type mapping
    df['employment_type_full'] = df['employment_type'].map({
        'FT': 'Full Time',
        'PT': 'Part Time',
        'CT': 'Contract',
        'FL': 'Freelance'
    })
    
    # Create remote ratio mapping
    df['remote_work'] = df['remote_ratio'].map({
        0: 'On-site',
        50: 'Hybrid',
        100: 'Remote'
    })
    
    # Create company size mapping
    df['company_size_full'] = df['company_size'].map({
        'S': 'Small',
        'M': 'Medium',
        'L': 'Large'
    })
    
    return df

# Load the data
df = load_data()

# Header and Introduction
st.markdown('<h1 class="main-header">Data Science Salary Explorer</h1>', unsafe_allow_html=True)

# Introduction with key insights
st.markdown("""
<div class="insight-box">
    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 20px; display: block; color: #1e3a8a; font-weight: 500;">
        Explore comprehensive salary trends in the data science field across different roles, experience levels, and global locations.
    </p>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 15px;">
        <div style="text-align: center; padding: 10px; min-width: 200px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e3a8a;">💼</div>
            <p style="font-weight: 600; margin: 5px 0; display: block;">Multiple Job Roles</p>
            <p style="font-size: 0.9rem; color: #4b5563; display: block;">Compare salaries across various data science positions</p>
        </div>
        <div style="text-align: center; padding: 10px; min-width: 200px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e3a8a;">📈</div>
            <p style="font-weight: 600; margin: 5px 0; display: block;">Experience Impact</p>
            <p style="font-size: 0.9rem; color: #4b5563; display: block;">See how experience level affects compensation</p>
        </div>
        <div style="text-align: center; padding: 10px; min-width: 200px;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e3a8a;">🌎</div>
            <p style="font-weight: 600; margin: 5px 0; display: block;">Global Insights</p>
            <p style="font-size: 0.9rem; color: #4b5563; display: block;">Discover salary variations across countries</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Sidebar with organized filters
st.sidebar.markdown("""<h2 style='color: #1e3a8a; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px;'>Dashboard Filters</h2>""", unsafe_allow_html=True)

# Add sidebar description
st.sidebar.markdown("""<p style='font-size: 0.9rem; color: #4b5563; margin-bottom: 20px;'>Customize your view by selecting specific criteria below. All filters are applied in real-time.</p>""", unsafe_allow_html=True)

# Create filter sections with expanders for better organization
with st.sidebar.expander("📅 Time Period", expanded=True):
    # Year filter
    years = sorted(df['work_year'].unique())
    selected_years = st.multiselect("Select Years", years, default=years, help="Filter data by work year")

with st.sidebar.expander("👨‍💼 Professional Details", expanded=True):
    # Experience level filter with better labels
    experience_options = df['experience_level_full'].dropna().unique()
    selected_experience = st.multiselect(
        "Experience Level", 
        experience_options, 
        default=experience_options,
        help="Filter by professional experience level"
    )
    
    # Job title filter with search functionality
    job_titles = sorted(df['job_title'].unique())
    job_title_search = st.text_input("Search Job Titles", "", help="Type to search for specific job titles")
    
    # Filter job titles based on search input
    if job_title_search:
        filtered_job_titles = [title for title in job_titles if job_title_search.lower() in title.lower()]
    else:
        filtered_job_titles = job_titles
        
    selected_job_titles = st.multiselect(
        "Job Titles", 
        filtered_job_titles, 
        default=[],
        help="Select specific job titles to analyze"
    )

with st.sidebar.expander("🏢 Company Information", expanded=True):
    # Remote work filter
    remote_options = df['remote_work'].dropna().unique()
    selected_remote = st.multiselect(
        "Work Arrangement", 
        remote_options, 
        default=remote_options,
        help="Filter by remote work status"
    )
    
    # Company size filter
    company_size_options = df['company_size_full'].dropna().unique()
    selected_company_size = st.multiselect(
        "Company Size", 
        company_size_options, 
        default=company_size_options,
        help="Filter by company size category"
    )
    
    # Location filter with search functionality
    locations = sorted(df['company_location'].unique())
    location_search = st.text_input("Search Locations", "", help="Type to search for specific countries")
    
    # Filter locations based on search input
    if location_search:
        filtered_locations = [loc for loc in locations if location_search.lower() in loc.lower()]
    else:
        filtered_locations = locations
        
    selected_locations = st.multiselect(
        "Company Location", 
        filtered_locations, 
        default=[],
        help="Select specific countries to analyze"
    )

with st.sidebar.expander("💰 Compensation", expanded=True):
    # Salary range filter with formatted values
    min_salary = int(df['salary_in_usd'].min())
    max_salary = int(df['salary_in_usd'].max())
    
    st.markdown(f"""<p style='font-size: 0.85rem; color: #4b5563;'>Range: ${min_salary:,} - ${max_salary:,}</p>""", unsafe_allow_html=True)
    
    salary_range = st.slider(
        "Salary Range (USD)", 
        min_salary, 
        max_salary, 
        (min_salary, max_salary),
        help="Filter by annual salary range in USD"
    )
    
    # Display selected range with formatting
    st.markdown(f"""<p style='font-size: 0.9rem; color: #1e3a8a; font-weight: 500;'>Selected: ${salary_range[0]:,} - ${salary_range[1]:,}</p>""", unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()

if selected_years:
    filtered_df = filtered_df[filtered_df['work_year'].isin(selected_years)]
    
if selected_experience:
    filtered_df = filtered_df[filtered_df['experience_level_full'].isin(selected_experience)]
    
if selected_job_titles:
    filtered_df = filtered_df[filtered_df['job_title'].isin(selected_job_titles)]
    
if selected_remote:
    filtered_df = filtered_df[filtered_df['remote_work'].isin(selected_remote)]
    
if selected_company_size:
    filtered_df = filtered_df[filtered_df['company_size_full'].isin(selected_company_size)]
    
if selected_locations:
    filtered_df = filtered_df[filtered_df['company_location'].isin(selected_locations)]
    
filtered_df = filtered_df[(filtered_df['salary_in_usd'] >= salary_range[0]) & 
                          (filtered_df['salary_in_usd'] <= salary_range[1])]

# Display dataset info
st.sidebar.markdown("## Dataset Information")
st.sidebar.info(f"Total Records: {len(df)}\nFiltered Records: {len(filtered_df)}")

# Main dashboard content
tabs = st.tabs(["Overview", "Salary Analysis", "Job Roles", "Geographical Analysis", "Experience Impact"])

# Overview Tab
with tabs[0]:
    st.markdown('<h2 class="sub-header">Salary Overview</h2>', unsafe_allow_html=True)
    
    # Enhanced key metrics with icons and additional insights
st.markdown("""<div class="chart-container">""", unsafe_allow_html=True)

# Calculate additional metrics
avg_salary = filtered_df['salary_in_usd'].mean()
median_salary = filtered_df['salary_in_usd'].median()
max_salary = filtered_df['salary_in_usd'].max()
min_salary = filtered_df['salary_in_usd'].min()
std_salary = filtered_df['salary_in_usd'].std()

# Calculate percentiles for context
p25 = filtered_df['salary_in_usd'].quantile(0.25)
p75 = filtered_df['salary_in_usd'].quantile(0.75)
iqr = p75 - p25

# Create a more visually appealing metrics display
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="metric-container">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 15px; color: #1e3a8a;">💰</div>
            <div>
                <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px; display: block;">Average Salary</p>
                <p style="font-size: 1.5rem; font-weight: 700; color: #1e3a8a; margin: 0; display: block;">${avg_salary:,.0f}</p>
                <p style="font-size: 0.8rem; color: #6b7280; margin-top: 5px; display: block;">Standard Deviation: ${std_salary:,.0f}</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
with col2:
    st.markdown(f'''
    <div class="metric-container">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 15px; color: #1e3a8a;">📊</div>
            <div>
                <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px; display: block;">Median Salary</p>
                <p style="font-size: 1.5rem; font-weight: 700; color: #1e3a8a; margin: 0; display: block;">${median_salary:,.0f}</p>
                <p style="font-size: 0.8rem; color: #6b7280; margin-top: 5px; display: block;">Middle value in distribution</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
with col3:
    st.markdown(f'''
    <div class="metric-container">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 15px; color: #1e3a8a;">🔼</div>
            <div>
                <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px; display: block;">Highest Salary</p>
                <p style="font-size: 1.5rem; font-weight: 700; color: #1e3a8a; margin: 0; display: block;">${max_salary:,.0f}</p>
                <p style="font-size: 0.8rem; color: #6b7280; margin-top: 5px; display: block;">Top earner in dataset</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
with col4:
    st.markdown(f'''
    <div class="metric-container">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2rem; margin-right: 15px; color: #1e3a8a;">🔽</div>
            <div>
                <p style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px; display: block;">Lowest Salary</p>
                <p style="font-size: 1.5rem; font-weight: 700; color: #1e3a8a; margin: 0; display: block;">${min_salary:,.0f}</p>
                <p style="font-size: 0.8rem; color: #6b7280; margin-top: 5px; display: block;">Entry point in dataset</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Add salary distribution context
st.markdown(f'''
<div style="padding: 15px; background-color: #f1f5f9; border-radius: 8px; margin-top: 15px;">
    <p style="font-weight: 600; margin-bottom: 8px; display: block;">Salary Distribution Insights:</p>
    <ul style="margin: 0; padding-left: 20px;">
        <li style="margin-bottom: 5px; display: list-item;">Middle 50% of salaries fall between <b>${p25:,.0f}</b> and <b>${p75:,.0f}</b></li>
        <li style="margin-bottom: 5px; display: list-item;">Interquartile Range (IQR): <b>${iqr:,.0f}</b></li>
        <li style="display: list-item;">Salary Range Spread: <b>${max_salary-min_salary:,.0f}</b></li>
    </ul>
</div>
''', unsafe_allow_html=True)

st.markdown("""</div>""", unsafe_allow_html=True)

# Enhanced Salary distribution with annotations
st.markdown('<h3 class="sub-header">Salary Distribution</h3>', unsafe_allow_html=True)

# Create a more visually appealing histogram with annotations
fig = px.histogram(
    filtered_df, 
    x="salary_in_usd", 
    nbins=50,
    title="Salary Distribution in USD",
    color_discrete_sequence=['#3b82f6'],
    opacity=0.8
)

# Add mean and median lines
fig.add_vline(x=avg_salary, line_dash="dash", line_color="#ef4444", annotation_text=f"Mean: ${avg_salary:,.0f}", 
              annotation_position="top right", annotation_font_color="#ef4444", annotation_font_size=12)
fig.add_vline(x=median_salary, line_dash="dash", line_color="#10b981", annotation_text=f"Median: ${median_salary:,.0f}", 
              annotation_position="top left", annotation_font_color="#10b981", annotation_font_size=12)

# Enhance layout
fig.update_layout(
    xaxis_title="Salary (USD)",
    yaxis_title="Count",
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    font=dict(family="Arial, sans-serif", size=12),
    hoverlabel=dict(font_size=12, font_family="Arial, sans-serif"),
    xaxis=dict(
        tickformat="$,.0f",
        gridcolor="#e5e7eb",
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="#e5e7eb",
        showgrid=True,
    ),
)

st.plotly_chart(fig, use_container_width=True)

# Top job titles by count
st.markdown('<h3 class="sub-header">Most Common Job Titles</h3>', unsafe_allow_html=True)

job_count = filtered_df['job_title'].value_counts().reset_index()
job_count.columns = ['job_title', 'count']
job_count = job_count.sort_values('count', ascending=False).head(10)

fig = px.bar(
    job_count,
    x='count',
    y='job_title',
    orientation='h',
    title="Top 10 Most Common Job Titles",
    color='count',
    color_continuous_scale='Blues',
)
fig.update_layout(
    xaxis_title="Number of Positions",
    yaxis_title="Job Title",
    height=500,
    yaxis={'categoryorder':'total ascending'}
)
st.plotly_chart(fig, use_container_width=True)

# Salary Analysis Tab
with tabs[1]:
    st.markdown('<h2 class="sub-header">Salary Analysis</h2>', unsafe_allow_html=True)
    
    # Salary by experience level
    st.markdown('<h3 class="sub-header">Salary by Experience Level</h3>', unsafe_allow_html=True)
    
    exp_salary = filtered_df.groupby('experience_level_full')['salary_in_usd'].agg(['mean', 'median', 'min', 'max']).reset_index()
    exp_salary.columns = ['Experience Level', 'Mean Salary', 'Median Salary', 'Min Salary', 'Max Salary']
    
    # Sort by experience level in logical order
    exp_order = {'Entry Level': 0, 'Mid Level': 1, 'Senior Level': 2, 'Executive Level': 3}
    exp_salary['order'] = exp_salary['Experience Level'].map(exp_order)
    exp_salary = exp_salary.sort_values('order').drop('order', axis=1)
    
    fig = px.bar(
        exp_salary,
        x='Experience Level',
        y=['Mean Salary', 'Median Salary'],
        barmode='group',
        title="Average and Median Salary by Experience Level",
        color_discrete_sequence=['#0083B8', '#00B0B9']
    )
    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Salary (USD)",
        height=500,
        legend_title="Metric"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary by company size
    st.markdown('<h3 class="sub-header">Salary by Company Size</h3>', unsafe_allow_html=True)
    
    size_salary = filtered_df.groupby('company_size_full')['salary_in_usd'].agg(['mean', 'median']).reset_index()
    size_salary.columns = ['Company Size', 'Mean Salary', 'Median Salary']
    
    # Sort by company size in logical order
    size_order = {'Small': 0, 'Medium': 1, 'Large': 2}
    size_salary['order'] = size_salary['Company Size'].map(size_order)
    size_salary = size_salary.sort_values('order').drop('order', axis=1)
    
    fig = px.bar(
        size_salary,
        x='Company Size',
        y=['Mean Salary', 'Median Salary'],
        barmode='group',
        title="Average and Median Salary by Company Size",
        color_discrete_sequence=['#0083B8', '#00B0B9']
    )
    fig.update_layout(
        xaxis_title="Company Size",
        yaxis_title="Salary (USD)",
        height=500,
        legend_title="Metric"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary by remote work
    st.markdown('<h3 class="sub-header">Salary by Remote Work Status</h3>', unsafe_allow_html=True)
    
    remote_salary = filtered_df.groupby('remote_work')['salary_in_usd'].agg(['mean', 'median']).reset_index()
    remote_salary.columns = ['Remote Status', 'Mean Salary', 'Median Salary']
    
    fig = px.bar(
        remote_salary,
        x='Remote Status',
        y=['Mean Salary', 'Median Salary'],
        barmode='group',
        title="Average and Median Salary by Remote Work Status",
        color_discrete_sequence=['#0083B8', '#00B0B9']
    )
    fig.update_layout(
        xaxis_title="Remote Work Status",
        yaxis_title="Salary (USD)",
        height=500,
        legend_title="Metric"
    )
    st.plotly_chart(fig, use_container_width=True)

# Job Roles Tab
with tabs[2]:
    st.markdown('<h2 class="sub-header">Job Role Analysis</h2>', unsafe_allow_html=True)
    
    # Enhanced Top 10 most common job titles with salary information
    st.markdown('<h3 class="sub-header">Top Paying Job Titles</h3>', unsafe_allow_html=True)
    st.markdown('<p class="chart-description">Analysis of the highest paying job titles with statistical significance (minimum 5 entries).</p>', unsafe_allow_html=True)
    
    # Only include job titles with at least 5 entries for statistical significance
    job_salary = filtered_df.groupby('job_title')['salary_in_usd'].agg(['mean', 'count']).reset_index()
    job_salary = job_salary[job_salary['count'] >= 5].sort_values('mean', ascending=False).head(15)
    job_salary.columns = ['Job Title', 'Average Salary', 'Count']
    
    # Create a more informative and visually appealing bar chart
    fig = px.bar(
        job_salary,
        x='Average Salary',
        y='Job Title',
        orientation='h',
        title="Top 15 Highest Paying Job Titles (with at least 5 entries)",
        color='Average Salary',
        color_continuous_scale='Blues',
        hover_data=['Count'],
        text_auto='.2s'
    )
    
    # Update layout for a more professional look
    fig.update_layout(
        xaxis_title="Average Salary (USD)",
        yaxis_title="Job Title",
        height=600,
        yaxis={'categoryorder':'total ascending'},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif"),
        hoverlabel=dict(font_size=12, font_family="Arial, sans-serif"),
        xaxis=dict(
            tickformat="$,.0f",
            gridcolor="#e5e7eb",
            showgrid=True,
        )
    )
    
    # Update traces for better visualization
    fig.update_traces(
        texttemplate='$%{x:,.0f}',
        textposition='inside',
        marker_line_color='#e5e7eb',
        marker_line_width=1
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary range by job title
    st.markdown('<h3 class="sub-header">Salary Range by Popular Job Titles</h3>', unsafe_allow_html=True)
    
    # Get top 10 most common job titles
    top_jobs = filtered_df['job_title'].value_counts().head(10).index.tolist()
    top_jobs_df = filtered_df[filtered_df['job_title'].isin(top_jobs)]
    
    fig = px.box(
        top_jobs_df,
        x='job_title',
        y='salary_in_usd',
        title="Salary Range for Most Common Job Titles",
        color='job_title',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        xaxis_title="Job Title",
        yaxis_title="Salary (USD)",
        height=600,
        showlegend=False,
        xaxis={'categoryorder':'array', 'categoryarray':top_jobs}
    )
    st.plotly_chart(fig, use_container_width=True)

# Geographical Analysis Tab
with tabs[3]:
    st.markdown('<h2 class="sub-header">Geographical Analysis</h2>', unsafe_allow_html=True)
    
    # Average salary by location
    st.markdown('<h3 class="sub-header">Average Salary by Location</h3>', unsafe_allow_html=True)
    st.markdown('<p class="chart-description">Interactive world map showing average data science salaries by country with detailed statistics.</p>', unsafe_allow_html=True)
    
    # Only include locations with at least 5 entries
    location_salary = filtered_df.groupby('company_location').agg({
        'salary_in_usd': ['mean', 'median', 'std', 'count']
    }).reset_index()
    
    # Flatten the multi-level columns
    location_salary.columns = ['Country Code', 'Average Salary', 'Median Salary', 'Salary Std Dev', 'Count']
    location_salary = location_salary[location_salary['Count'] >= 5].sort_values('Average Salary', ascending=False)
    
    # Create a dictionary for 2-letter to 3-letter country code conversion
    # This is necessary because Plotly's choropleth requires ISO 3166-1 alpha-3 format
    country_code_map = {
        'US': 'USA', 'GB': 'GBR', 'CA': 'CAN', 'DE': 'DEU', 'ES': 'ESP',
        'FR': 'FRA', 'IN': 'IND', 'NL': 'NLD', 'AU': 'AUS', 'JP': 'JPN',
        'BR': 'BRA', 'PT': 'PRT', 'SG': 'SGP', 'IT': 'ITA', 'CH': 'CHE',
        'AT': 'AUT', 'PL': 'POL', 'DK': 'DNK', 'CZ': 'CZE', 'FI': 'FIN',
        'BE': 'BEL', 'SE': 'SWE', 'MX': 'MEX', 'IE': 'IRL', 'RU': 'RUS',
        'UA': 'UKR', 'HK': 'HKG', 'RO': 'ROU', 'IL': 'ISR', 'HU': 'HUN',
        'LT': 'LTU', 'HR': 'HRV', 'EE': 'EST', 'LU': 'LUX', 'SK': 'SVK',
        'SI': 'SVN', 'GR': 'GRC', 'BG': 'BGR', 'NO': 'NOR', 'CO': 'COL',
        'NZ': 'NZL', 'TR': 'TUR', 'MY': 'MYS', 'TH': 'THA', 'VN': 'VNM',
        'PK': 'PAK', 'PH': 'PHL', 'ID': 'IDN', 'AR': 'ARG', 'CL': 'CHL'
    }
    
    # Add country names for better readability
    country_names = {
        'US': 'United States', 'GB': 'United Kingdom', 'CA': 'Canada', 'DE': 'Germany', 'ES': 'Spain',
        'IN': 'India', 'FR': 'France', 'AU': 'Australia', 'NL': 'Netherlands', 'JP': 'Japan',
        'BR': 'Brazil', 'PT': 'Portugal', 'SG': 'Singapore', 'IT': 'Italy', 'CH': 'Switzerland',
        'AT': 'Austria', 'PL': 'Poland', 'DK': 'Denmark', 'CZ': 'Czech Republic', 'FI': 'Finland',
        'BE': 'Belgium', 'SE': 'Sweden', 'MX': 'Mexico', 'IE': 'Ireland', 'RU': 'Russia',
        'UA': 'Ukraine', 'HK': 'Hong Kong', 'RO': 'Romania', 'IL': 'Israel', 'HU': 'Hungary',
        'LT': 'Lithuania', 'HR': 'Croatia', 'EE': 'Estonia', 'LU': 'Luxembourg', 'SK': 'Slovakia',
        'SI': 'Slovenia', 'GR': 'Greece', 'BG': 'Bulgaria', 'NO': 'Norway', 'CO': 'Colombia',
        'NZ': 'New Zealand', 'TR': 'Turkey', 'MY': 'Malaysia', 'TH': 'Thailand', 'VN': 'Vietnam',
        'PK': 'Pakistan', 'PH': 'Philippines', 'ID': 'Indonesia', 'AR': 'Argentina', 'CL': 'Chile'
    }
    
    # Add the ISO codes and country names to the dataframe
    location_salary['ISO_Code'] = location_salary['Country Code'].map(country_code_map)
    location_salary['Country Name'] = location_salary['Country Code'].map(country_names)
    
    # Fill missing values with the country code
    location_salary['Country Name'] = location_salary['Country Name'].fillna(location_salary['Country Code'])
    
    # Format the hover text to show detailed statistics
    location_salary['Hover Text'] = location_salary.apply(
        lambda row: f"<b>{row['Country Name']} ({row['Country Code']})</b><br>" +
                    f"Average Salary: ${row['Average Salary']:,.0f}<br>" +
                    f"Median Salary: ${row['Median Salary']:,.0f}<br>" +
                    f"Standard Deviation: ${row['Salary Std Dev']:,.0f}<br>" +
                    f"Number of Jobs: {row['Count']}",
        axis=1
    )
    
    fig = px.choropleth(
        location_salary,
        locations='ISO_Code',  # Use the 3-letter ISO codes
        color='Average Salary',
        hover_name='Country Name',  # Keep the original 2-letter code for hover
        custom_data=['Hover Text'],
        title="Average Salary by Country (USD)",
        color_continuous_scale='Blues',
        projection='natural earth'
    )
    
    # Update hover template to show the custom hover text
    fig.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>"
    )
    
    # Add a color bar title
    fig.update_coloraxes(colorbar_title_text='Average Salary (USD)', colorbar_title_font=dict(size=14))
    
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular',
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(223, 223, 223)',
            countrycolor='rgb(223, 223, 223)'
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif"),
        hoverlabel=dict(font_size=12, font_family="Arial, sans-serif", bgcolor="white", bordercolor="#e5e7eb")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top countries by average salary
    st.markdown('<h3 class="sub-header">Top Countries by Average Salary</h3>', unsafe_allow_html=True)
    
    top_countries = location_salary.head(10)
    
    fig = px.bar(
        top_countries,
        x='Country Code',
        y='Average Salary',
        title="Top 10 Countries by Average Salary",
        color='Average Salary',
        color_continuous_scale='Blues',
        hover_data=['Count']
    )
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Average Salary (USD)",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary comparison: Employee residence vs. Company location
    st.markdown('<h3 class="sub-header">Salary Comparison: Employee Residence vs. Company Location</h3>', unsafe_allow_html=True)
    
    # Get top 10 countries by count
    top_countries_by_count = filtered_df['company_location'].value_counts().head(10).index.tolist()
    
    # Filter data for these countries
    country_comparison = filtered_df[filtered_df['company_location'].isin(top_countries_by_count)]
    
    # Calculate average salary by employee residence and company location
    emp_residence = country_comparison.groupby('employee_residence')['salary_in_usd'].mean().reset_index()
    emp_residence.columns = ['Country', 'Average Salary']
    emp_residence['Type'] = 'Employee Residence'
    
    comp_location = country_comparison.groupby('company_location')['salary_in_usd'].mean().reset_index()
    comp_location.columns = ['Country', 'Average Salary']
    comp_location['Type'] = 'Company Location'
    
    combined = pd.concat([emp_residence, comp_location])
    
    fig = px.bar(
        combined,
        x='Country',
        y='Average Salary',
        color='Type',
        barmode='group',
        title="Average Salary: Employee Residence vs. Company Location",
        color_discrete_sequence=['#0083B8', '#00B0B9']
    )
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Average Salary (USD)",
        height=500,
        legend_title="Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# Experience Impact Tab
with tabs[4]:
    st.markdown('<h2 class="sub-header">Experience Level Impact</h2>', unsafe_allow_html=True)
    
    # Salary progression by experience level for top job titles
    st.markdown('<h3 class="sub-header">Salary Progression by Experience Level</h3>', unsafe_allow_html=True)
    
    # Get top 5 job titles
    top_5_jobs = filtered_df['job_title'].value_counts().head(5).index.tolist()
    
    # Filter data for these job titles
    exp_progression = filtered_df[filtered_df['job_title'].isin(top_5_jobs)]
    
    # Group by job title and experience level
    job_exp_salary = exp_progression.groupby(['job_title', 'experience_level_full'])['salary_in_usd'].mean().reset_index()
    
    # Create experience level order for proper sorting
    exp_level_order = {'Entry Level': 0, 'Mid Level': 1, 'Senior Level': 2, 'Executive Level': 3}
    job_exp_salary['exp_order'] = job_exp_salary['experience_level_full'].map(exp_level_order)
    job_exp_salary = job_exp_salary.sort_values(['job_title', 'exp_order'])
    
    fig = px.line(
        job_exp_salary,
        x='experience_level_full',
        y='salary_in_usd',
        color='job_title',
        markers=True,
        title="Salary Progression by Experience Level for Top 5 Job Titles",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Average Salary (USD)",
        height=600,
        xaxis={'categoryorder':'array', 'categoryarray':['Entry Level', 'Mid Level', 'Senior Level', 'Executive Level']}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Experience level distribution
    st.markdown('<h3 class="sub-header">Experience Level Distribution</h3>', unsafe_allow_html=True)
    
    exp_dist = filtered_df['experience_level_full'].value_counts().reset_index()
    exp_dist.columns = ['Experience Level', 'Count']
    
    # Sort by experience level in logical order
    exp_dist['order'] = exp_dist['Experience Level'].map(exp_level_order)
    exp_dist = exp_dist.sort_values('order').drop('order', axis=1)
    
    fig = px.pie(
        exp_dist,
        values='Count',
        names='Experience Level',
        title="Distribution of Experience Levels",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_layout(
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Experience level impact on remote work
    st.markdown('<h3 class="sub-header">Experience Level Impact on Remote Work</h3>', unsafe_allow_html=True)
    
    remote_exp = filtered_df.groupby(['experience_level_full', 'remote_work']).size().reset_index()
    remote_exp.columns = ['Experience Level', 'Remote Status', 'Count']
    
    # Sort by experience level in logical order
    remote_exp['order'] = remote_exp['Experience Level'].map(exp_level_order)
    remote_exp = remote_exp.sort_values('order')
    
    fig = px.bar(
        remote_exp,
        x='Experience Level',
        y='Count',
        color='Remote Status',
        title="Remote Work Distribution by Experience Level",
        color_discrete_sequence=['#0083B8', '#00B0B9', '#00D7B9']
    )
    fig.update_layout(
        xaxis_title="Experience Level",
        yaxis_title="Count",
        height=500,
        legend_title="Remote Status",
        xaxis={'categoryorder':'array', 'categoryarray':['Entry Level', 'Mid Level', 'Senior Level', 'Executive Level']}
    )
    st.plotly_chart(fig, use_container_width=True)

# Enhanced professional footer with additional information
st.markdown('''
<div class="footer-container">
    <div class="footer-section">
        <h4>About This Dashboard</h4>
        <p>This interactive dashboard provides comprehensive insights into data science salaries across different job roles, experience levels, and geographical locations. The analysis is based on real-world salary data to help professionals, recruiters, and organizations make informed decisions.</p>
    </div>
    
    <div class="footer-section">
        <h4>Key Insights</h4>
        <ul>
            <li>Explore salary distributions across different job titles and experience levels</li>
            <li>Compare compensation packages based on company size and remote work options</li>
            <li>Analyze geographical salary variations with interactive visualizations</li>
            <li>Track salary trends over time for career planning</li>
        </ul>
    </div>
    
    <div class="footer-section">
        <h4>Methodology</h4>
        <p>The analysis uses statistical methods to process and visualize salary data. Outliers are handled using IQR method, and all visualizations are created with Plotly and Streamlit. The dashboard is updated regularly to ensure data accuracy.</p>
    </div>
    
    <div class="footer-copyright">
        <p>© 2025 Data Science Salary Explorer | Created with <span style="color: #ff4b4b;">♥</span> using Streamlit and Plotly</p>
        <p class="version-info">Version 2.0 | Last Updated: July 2025</p>
    </div>
</div>
''', unsafe_allow_html=True)