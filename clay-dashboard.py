import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processor import DataProcessor
from utils.visualizations import ChartCreator
from components.dashboard_pages import DashboardPages

class ClayDashboard:
    """Main dashboard application class"""
    
    def __init__(self):
        """Initialize the dashboard with all components"""
        self.setup_page_config()
        self.setup_styling()
        self.data_processor = DataProcessor()
        self.chart_creator = ChartCreator()
        self.dashboard_pages = DashboardPages(self.data_processor, self.chart_creator)
        
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        # Force light mode
        st.set_page_config(
            page_title="Upstart13 - Dashboard",
            page_icon="🏗️",
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={
                'About': "# Upstart13 Dashboard."
            }
        )
        
        # Additional CSS to force light mode
        st.markdown("""
        <style>
            /* Force light mode globally */
            .stApp {
                background-color: #ffffff !important;
            }
            
            /* Override Streamlit's dark mode detection */
            [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
            }
            
            /* Force light mode for all Streamlit components */
            .stMarkdown, .stText, .stDataFrame, .stMetric, .stSelectbox, .stButton {
                background-color: transparent !important;
                color: #2c3e50 !important;
            }
            
            /* Override any system dark mode preferences */
            @media (prefers-color-scheme: dark) {
                .stApp, [data-testid="stAppViewContainer"] {
                    background-color: #ffffff !important;
                }
            }
        </style>
        """, unsafe_allow_html=True)
    
    def setup_styling(self):
        """Setup professional CSS styling for stakeholders"""
        st.markdown("""
        <style>
            /* Force light mode - override system dark mode */
            [data-testid="stAppViewContainer"] {
                background-color: #ffffff !important;
            }
            
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
            }
            
            .stApp {
                background-color: #ffffff !important;
            }
            
            /* Override any dark mode styles */
            .dark .stApp {
                background-color: #ffffff !important;
            }
            
            /* Force light text on light background */
            .stMarkdown, .stText, .stDataFrame {
                color: #2c3e50 !important;
            }
            
            /* Professional color scheme for light theme */
            :root {
                --primary-color: #1f4e79;
                --secondary-color: #2c5aa0;
                --accent-color: #4a90e2;
                --success-color: #28a745;
                --warning-color: #ffc107;
                --danger-color: #dc3545;
                --text-dark: #2c3e50;
                --text-light: #6c757d;
                --bg-light: #f8f9fa;
                --border-color: #dee2e6;
                --card-bg: #ffffff;
            }
            
            /* Main header styling */
            .main-header {
                font-size: 2.5rem;
                font-weight: 600;
                color: var(--primary-color);
                text-align: center;
                margin-bottom: 1.5rem;
                letter-spacing: -0.5px;
            }
            
            /* Section header styling */
            .section-header {
                font-size: 1.6rem;
                font-weight: 600;
                color: var(--text-dark);
                margin-top: 2rem;
                margin-bottom: 1.5rem;
                padding: 0.5rem 0;
                border-bottom: 2px solid var(--primary-color);
            }
            
            /* Metric card styling */
            .metric-card {
                background: var(--card-bg);
                padding: 1.5rem;
                border-radius: 8px;
                border: 1px solid var(--border-color);
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                margin: 0.5rem 0;
                transition: transform 0.2s ease;
            }
            
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            /* Professional button styling */
            .stButton > button {
                background: var(--primary-color);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                font-size: 0.9rem;
                transition: all 0.2s ease;
            }
            
            .stButton > button:hover {
                background: var(--secondary-color);
                transform: translateY(-1px);
            }
            
            /* Data table styling */
            .dataframe {
                font-size: 0.9rem;
                border-radius: 6px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            
            /* Footer styling */
            .footer {
                text-align: center;
                color: var(--text-light);
                padding: 2rem 0;
                border-top: 1px solid var(--border-color);
                margin-top: 3rem;
                background: var(--bg-light);
            }
            
            /* Description styling */
            .description {
                background: var(--bg-light);
                padding: 1.5rem;
                border-radius: 8px;
                border-left: 4px solid var(--primary-color);
                margin: 1rem 0;
                color: var(--text-dark);
                font-size: 1rem;
                line-height: 1.6;
            }
            
            /* Hide sidebar */
            .css-1d391kg {
                display: none;
            }
            
            /* Professional selectbox styling */
            .stSelectbox > div > div {
                border-radius: 6px;
                border: 1px solid var(--border-color);
            }
            
            /* Professional text input styling */
            .stTextInput > div > div > input {
                border-radius: 6px;
                border: 1px solid var(--border-color);
            }
            
            /* Enhanced Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0px;
                background-color: var(--bg-light);
                border-bottom: 2px solid var(--border-color);
                padding: 0;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: var(--bg-light);
                border-radius: 8px 8px 0 0;
                border: 1px solid var(--border-color);
                border-bottom: none;
                color: var(--text-dark);
                font-weight: 500;
                font-size: 1rem;
                padding: 1rem 2rem;
                margin-right: 4px;
                min-width: 200px;
                text-align: center;
                transition: all 0.2s ease;
            }
            
            .stTabs [aria-selected="true"] {
                background-color: var(--primary-color);
                color: white;
                border-color: var(--primary-color);
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .stTabs [aria-selected="false"]:hover {
                background-color: var(--accent-color);
                color: white;
                border-color: var(--accent-color);
            }
            
            /* Graph description styling */
            .graph-description {
                color: var(--text-light);
                font-style: italic;
                margin-bottom: 1rem;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            
            /* Refresh button styling */
            .stButton > button[data-testid="baseButton-secondary"] {
                background: var(--accent-color) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
            
            .stButton > button[data-testid="baseButton-secondary"]:hover {
                background: var(--secondary-color) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            }
            
            /* Alternative styling for refresh button */
            .stButton > button:has-text("🔄 Refresh Data") {
                background: var(--accent-color) !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }
            
            .stButton > button:has-text("🔄 Refresh Data"):hover {
                background: var(--secondary-color) !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
            }
            
        </style>
        """, unsafe_allow_html=True)
    
    def render_description(self, page: str):
        """Render professional description for each page"""
        descriptions = {
            "📈 Overview": "Executive summary providing key business intelligence across all data dimensions. Monitor critical KPIs and strategic insights for informed decision-making.",
            "🏢 Companies": "Comprehensive company analysis including market positioning, competitive landscape, and strategic opportunities. Track industry trends and geographic distribution.",
            "👥 Decision Makers": "Strategic leadership analysis and relationship mapping. Identify key decision makers, seniority distribution, and company representation for targeted outreach.",
            "💼 Jobs": "Market intelligence and recruitment analytics. Monitor job posting trends, skill demand, and employment opportunities across industries and locations."
        }
        
        st.markdown(f"""
        <div class="description">
            <strong>📋 Strategic Overview:</strong> {descriptions.get(page, "Analytics dashboard providing comprehensive business intelligence.")}
        </div>
        """, unsafe_allow_html=True)
    
    def load_and_process_data(self):
        """Load and process all data"""
        with st.spinner("Loading data..."):
            # Load raw data
            companies_df, decision_makers_df, jobs_df = self.data_processor.load_data()
            
            if companies_df is None or decision_makers_df is None or jobs_df is None:
                st.error("Failed to load data. Please check your data files.")
                st.stop()
            
            # Preprocess data
            companies_clean = self.data_processor.preprocess_companies(companies_df)
            decision_makers_clean = self.data_processor.preprocess_decision_makers(decision_makers_df)
            jobs_clean = self.data_processor.preprocess_jobs(jobs_df)
            
            return companies_clean, decision_makers_clean, jobs_clean
    
    def render_navbar_with_refresh(self):
        """Render navbar with tabs and refresh icon on the right edge"""
        # Create a container for the navbar
        navbar_container = st.container()
        
        with navbar_container:
            # Create columns for navbar layout
            col1, col2, col3 = st.columns([8, 1, 1])
            
            with col1:
                # This space will be occupied by the tabs
                pass
            
            with col2:
                # Add some spacing
                st.write("")
            
            with col3:
                # Refresh icon button positioned at the far right
                if st.button("🔄", key="navbar_refresh", help="Refresh data"):
                    # Clear the cache to force data reload
                    st.cache_data.clear()
                    st.rerun()
    
    def render_refresh_button(self):
        """Render refresh button for data reload (legacy method)"""
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Refresh Data", key="refresh_data", help="Click to reload the latest data from files"):
                # Clear the cache to force data reload
                st.cache_data.clear()
                st.rerun()
    
    def render_footer(self):
        """Render the footer"""
        st.markdown("""
        <div class="footer">
            <p><strong>🏗️ Upstart13 Dashboard</strong></p>
            <p>Strategic Business Intelligence for Architecture, Engineering & Construction</p>
            <p>Last updated: {}</p>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    def run(self):
        """Main method to run the dashboard"""
        try:
            # Load and process data
            companies_df, decision_makers_df, jobs_df = self.load_and_process_data()
            
            # Main header with tooltip
            st.markdown('''
            <h1 class="main-header">
                Upstart13 Dashboard
                <span title="AEC = Architecture, Engineering & Construction. This platform provides strategic business intelligence, competitive analysis, and market insights for companies in the built environment industry." style="cursor: help; color: var(--accent-color); font-size: 0.8em; margin-left: 10px;">ⓘ</span>
            </h1>
            ''', unsafe_allow_html=True)
            
            # Create navbar with tabs and refresh icon
            self.render_navbar_with_refresh()
            
            # Use enhanced tabs for navigation
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Executive Overview", 
                "🏢 Company Intelligence", 
                "👥 Decision Maker Analysis", 
                "💼 Market Intelligence"
            ])
            
            with tab1:
                self.render_description("📈 Overview")
                self.dashboard_pages.render_overview_page(companies_df, decision_makers_df, jobs_df)
            
            with tab2:
                self.render_description("🏢 Companies")
                self.dashboard_pages.render_companies_page(companies_df)
            
            with tab3:
                self.render_description("👥 Decision Makers")
                self.dashboard_pages.render_decision_makers_page(decision_makers_df, companies_df)
            
            with tab4:
                self.render_description("💼 Jobs")
                self.dashboard_pages.render_jobs_page(jobs_df)
            
            # Render footer
            self.render_footer()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.exception(e)


def main():
    """Main entry point"""
    dashboard = ClayDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
