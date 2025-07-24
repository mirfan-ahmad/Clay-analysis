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
        st.set_page_config(
            page_title="Clay Analytics Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                # 'Get Help': 'https://github.com/your-repo/clay-dashboard',
                # 'Report a bug': "https://github.com/your-repo/clay-dashboard/issues",
                'About': "# Clay Analytics Dashboard\nA comprehensive analytics dashboard for Clay data analysis."
            }
        )
    
    def setup_styling(self):
        """Setup custom CSS styling"""
        st.markdown("""
        <style>
            /* Main header styling */
            .main-header {
                font-size: 2.5rem;
                font-weight: bold;
                color: #1f77b4;
                text-align: center;
                margin-bottom: 2rem;
                background: linear-gradient(90deg, #1f77b4, #ff7f0e);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            /* Section header styling */
            .section-header {
                font-size: 1.5rem;
                font-weight: bold;
                color: #2c3e50;
                margin-top: 2rem;
                margin-bottom: 1rem;
                padding: 0.5rem 0;
                border-bottom: 2px solid #1f77b4;
            }
            
            /* Metric card styling */
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 1.5rem;
                border-radius: 1rem;
                color: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 0.5rem 0;
            }
            
            /* Sidebar styling */
            .css-1d391kg {
                background-color: #f8f9fa;
            }
            
            /* Data table styling */
            .dataframe {
                font-size: 0.9rem;
            }
            
            /* Custom button styling */
            .stButton > button {
                background: linear-gradient(90deg, #1f77b4, #ff7f0e);
                color: white;
                border: none;
                border-radius: 0.5rem;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            
            /* Footer styling */
            .footer {
                text-align: center;
                color: #666;
                padding: 2rem 0;
                border-top: 1px solid #eee;
                margin-top: 3rem;
            }
            
            /* Loading animation */
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #1f77b4;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
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
    
    def render_sidebar(self):
        """Render the sidebar navigation"""
        st.sidebar.title("📊 Clay Analytics Dashboard")
        
        # Add dashboard info
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 Dashboard Info")
        st.sidebar.info("""
        This dashboard provides comprehensive analytics for your Clay data including:
        - **Companies**: Industry analysis, geographic distribution, company types
        - **Decision Makers**: Seniority levels, job titles, company representation
        - **Jobs**: Market trends, posting timelines, geographic distribution
        """)
        
        # Navigation
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🧭 Navigation")
        page = st.sidebar.selectbox(
            "Select Dashboard",
            ["📈 Overview", "🏢 Companies", "👥 Decision Makers", "💼 Jobs"]
        )
        
        # Add data refresh button
        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
        
        # Add export options
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📤 Export Options")
        export_format = st.sidebar.selectbox(
            "Export Format",
            ["CSV", "Excel", "JSON"]
        )
        
        return page
    
    def render_footer(self):
        """Render the footer"""
        st.markdown("---")
        st.markdown("""
        <div class="footer">
            <p>📊 Clay Analytics Dashboard</p>
            <p>Last updated: {}</p>
        </div>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    def run(self):
        """Main method to run the dashboard"""
        try:
            # Load and process data
            companies_df, decision_makers_df, jobs_df = self.load_and_process_data()
            
            # Render sidebar and get selected page
            page = self.render_sidebar()
            
            # Render selected page
            if page == "📈 Overview":
                self.dashboard_pages.render_overview_page(companies_df, decision_makers_df, jobs_df)
            elif page == "🏢 Companies":
                self.dashboard_pages.render_companies_page(companies_df)
            elif page == "👥 Decision Makers":
                self.dashboard_pages.render_decision_makers_page(decision_makers_df)
            elif page == "💼 Jobs":
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
