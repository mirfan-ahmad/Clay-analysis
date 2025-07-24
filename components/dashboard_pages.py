import streamlit as st
import pandas as pd
from utils.visualizations import ChartCreator
from utils.data_processor import DataProcessor
from utils.interactive_manager import InteractiveManager
from typing import Dict, Any
import plotly.graph_objects as go

class DashboardPages:
    """Handles all dashboard page components with interactive filtering"""
    
    def __init__(self, data_processor: DataProcessor, chart_creator: ChartCreator):
        self.data_processor = data_processor
        self.chart_creator = chart_creator
        self.interactive_manager = InteractiveManager()
        self.interactive_manager.initialize_session_state()
    
    def render_overview_page(self, companies_df: pd.DataFrame, 
                           decision_makers_df: pd.DataFrame, 
                           jobs_df: pd.DataFrame):
        """Render the overview dashboard page with interactive filtering"""
        st.markdown('<h1 class="main-header">📈 Clay Analytics Overview</h1>', unsafe_allow_html=True)
        
        # Manual filter controls on main screen
        st.markdown('<h2 class="section-header">🔧 Filter Controls</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.interactive_manager.create_manual_filter_controls(companies_df, 'Primary Industry', 'Industry')
        
        with col2:
            self.interactive_manager.create_manual_filter_controls(companies_df, 'Size', 'Company Size')
        
        with col3:
            self.interactive_manager.create_manual_filter_controls(decision_makers_df, 'Seniority', 'Seniority')
        
        # Apply filters to companies data
        filtered_companies = self.interactive_manager.apply_filters_to_dataframe(
            companies_df, 
            {"Industry": "Primary Industry", "Company Size": "Size"}
        )
        
        # Apply filters to decision makers data
        filtered_decision_makers = self.interactive_manager.apply_filters_to_dataframe(
            decision_makers_df,
            {"Seniority": "Seniority"}
        )
        
        # Cross-filter decision makers based on company filters
        active_filters = self.interactive_manager.get_active_filters()
        if "Industry" in active_filters or "Company Size" in active_filters:
            # Get filtered company names
            filtered_company_names = set(filtered_companies['Name'].str.lower())
            
            # Filter decision makers whose companies match the filtered companies
            filtered_decision_makers = filtered_decision_makers[
                filtered_decision_makers['Company'].str.lower().isin(filtered_company_names)
            ]
        
        # Key metrics (updated based on filters)
        self._render_overview_metrics(filtered_companies, filtered_decision_makers, jobs_df)
        
        # Interactive charts section
        st.markdown('<h2 class="section-header">📊 Industry Distribution</h2>', unsafe_allow_html=True)
        
        # Create interactive charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Industries distribution
            industry_counts = filtered_companies['Primary Industry'].value_counts()
            fig_industry = self.chart_creator.create_horizontal_bar(
                industry_counts, "Companies by Industry", "Number of Companies", "Industry"
            )
            fig_industry = self.interactive_manager.create_interactive_chart(fig_industry, "industry_chart")
            
            st.plotly_chart(fig_industry, use_container_width=True, key="industry_chart")
        
        with col2:
            # Company size distribution
            size_counts = filtered_companies['Size'].value_counts()
            fig_size = self.chart_creator.create_pie_chart(size_counts, "Company Size Distribution")
            fig_size = self.interactive_manager.create_interactive_chart(fig_size, "company_size_chart")
            
            st.plotly_chart(fig_size, use_container_width=True, key="size_chart")
        
        # Geographic distribution
        st.markdown('<h2 class="section-header">🌍 Geographic Distribution</h2>', unsafe_allow_html=True)
        country_counts = filtered_companies['Country'].value_counts()
        fig_country = self.chart_creator.create_vertical_bar(
            country_counts, "Companies by Country"
        )
        fig_country = self.interactive_manager.create_interactive_chart(fig_country, "country_chart")
        
        st.plotly_chart(fig_country, use_container_width=True, key="country_chart")
        
        # Decision makers by seniority
        st.markdown('<h2 class="section-header">👥 Decision Makers by Seniority</h2>', unsafe_allow_html=True)
        seniority_counts = filtered_decision_makers['Seniority'].value_counts()
        fig_seniority = self.chart_creator.create_pie_chart(
            seniority_counts, "Decision Makers by Seniority Level"
        )
        fig_seniority = self.interactive_manager.create_interactive_chart(fig_seniority, "seniority_chart")
        
        st.plotly_chart(fig_seniority, use_container_width=True, key="seniority_chart")
        
        # Filter management on main screen
        # self.interactive_manager.create_filter_ui({}, "Filter Management")
    
    def render_companies_page(self, companies_df: pd.DataFrame):
        """Render the companies dashboard page with interactive filtering"""
        st.markdown('<h1 class="main-header">🏢 Companies Analytics</h1>', unsafe_allow_html=True)
        
        # Manual filter controls on main screen
        st.markdown('<h2 class="section-header">🔧 Filter Controls</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.interactive_manager.create_manual_filter_controls(companies_df, 'Primary Industry', 'Industry')
        
        with col2:
            self.interactive_manager.create_manual_filter_controls(companies_df, 'Size', 'Company Size')
        
        with col3:
            self.interactive_manager.create_manual_filter_controls(companies_df, 'State', 'Location')
        
        # Apply filters to data
        filtered_companies = self.interactive_manager.apply_filters_to_dataframe(
            companies_df, 
            {"Industry": "Primary Industry", "Company Size": "Size", "Location": "State"}
        )
        
        # Key metrics (updated based on filters)
        metrics = self.data_processor.get_companies_metrics(filtered_companies)
        self._render_metrics_grid(metrics, [
            "Total Companies", "Unique Industries", "States Covered", "Private Companies"
        ])
        
        # Industry distribution
        st.markdown('<h2 class="section-header">🏭 Industry Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            industry_counts = filtered_companies['Primary Industry'].value_counts()
            fig_industry = self.chart_creator.create_horizontal_bar(
                industry_counts, "Companies by Industry", "Number of Companies", "Industry", height=500
            )
            fig_industry = self.interactive_manager.create_interactive_chart(fig_industry, "industry_chart")
            
            st.plotly_chart(fig_industry, use_container_width=True, key="companies_industry")
        
        with col2:
            fig_industry_pie = self.chart_creator.create_pie_chart(
                industry_counts, "Industry Distribution"
            )
            fig_industry_pie = self.interactive_manager.create_interactive_chart(fig_industry_pie, "industry_pie_chart")
            
            st.plotly_chart(fig_industry_pie, use_container_width=True, key="companies_industry_pie")
        
        # Company size distribution
        st.markdown('<h2 class="section-header">📏 Company Size Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            size_counts = filtered_companies['Size'].value_counts()
            fig_size = self.chart_creator.create_pie_chart(size_counts, "Company Size Distribution")
            fig_size = self.interactive_manager.create_interactive_chart(fig_size, "company_size_chart")
            
            st.plotly_chart(fig_size, use_container_width=True, key="companies_size")
        
        with col2:
            fig_size_bar = self.chart_creator.create_vertical_bar(
                size_counts, "Company Size Distribution", "Company Size", "Number of Companies"
            )
            fig_size_bar = self.interactive_manager.create_interactive_chart(fig_size_bar, "company_size_bar_chart")
            
            st.plotly_chart(fig_size_bar, use_container_width=True, key="companies_size_bar")
        
        # Geographic distribution
        st.markdown('<h2 class="section-header">🌍 Geographic Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            country_counts = filtered_companies['Country'].value_counts()
            fig_country = self.chart_creator.create_vertical_bar(
                country_counts, "Companies by Country", "Country", "Number of Companies"
            )
            fig_country = self.interactive_manager.create_interactive_chart(fig_country, "country_chart")
            
            st.plotly_chart(fig_country, use_container_width=True, key="companies_country")
        
        with col2:
            state_counts = filtered_companies['State'].value_counts()
            fig_state = self.chart_creator.create_horizontal_bar(
                state_counts, "Companies by State", "Number of Companies", "State", height=400
            )
            fig_state = self.interactive_manager.create_interactive_chart(fig_state, "state_chart")
            
            st.plotly_chart(fig_state, use_container_width=True, key="companies_state")
        
        # Company type distribution
        st.markdown('<h2 class="section-header">🏢 Company Type Distribution</h2>', unsafe_allow_html=True)
        type_counts = filtered_companies['Type'].value_counts()
        fig_type = self.chart_creator.create_pie_chart(type_counts, "Company Type Distribution")
        fig_type = self.interactive_manager.create_interactive_chart(fig_type, "company_type_chart")
        
        st.plotly_chart(fig_type, use_container_width=True, key="companies_type")
        
        # Data table (filtered)
        self._render_companies_data_table(filtered_companies)
        
        # Filter management on main screen
        # self.interactive_manager.create_filter_ui({}, "Filter Management")
    
    def render_decision_makers_page(self, decision_makers_df: pd.DataFrame):
        """Render the decision makers dashboard page with interactive filtering"""
        st.markdown('<h1 class="main-header">👥 Decision Makers Analytics</h1>', unsafe_allow_html=True)
        
        # Manual filter controls on main screen
        st.markdown('<h2 class="section-header">🔧 Filter Controls</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.interactive_manager.create_manual_filter_controls(decision_makers_df, 'Job Title', 'Job Title')
        
        with col2:
            self.interactive_manager.create_manual_filter_controls(decision_makers_df, 'Seniority', 'Seniority')
        
        with col3:
            self.interactive_manager.create_manual_filter_controls(decision_makers_df, 'State', 'Location')
        
        # Apply filters to data
        filtered_decision_makers = self.interactive_manager.apply_filters_to_dataframe(
            decision_makers_df,
            {"Job Title": "Job Title", "Seniority": "Seniority", "Location": "State"}
        )
        
        # Key metrics (updated based on filters)
        metrics = self.data_processor.get_decision_makers_metrics(filtered_decision_makers)
        self._render_metrics_grid(metrics, [
            "Total Decision Makers", "Companies Represented", "Unique Job Titles", "Unique Locations"
        ])
        
        # Seniority and job title distribution
        st.markdown('<h2 class="section-header">💼 Seniority and Job Title Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            seniority_counts = filtered_decision_makers['Seniority'].value_counts()
            fig_seniority = self.chart_creator.create_pie_chart(
                seniority_counts, "Decision Makers by Seniority Level"
            )
            fig_seniority = self.interactive_manager.create_interactive_chart(fig_seniority, "seniority_chart")
            
            st.plotly_chart(fig_seniority, use_container_width=True, key="dm_seniority")
        
        with col2:
            title_counts = filtered_decision_makers['Job Title'].value_counts()
            fig_titles = self.chart_creator.create_horizontal_bar(
                title_counts, "Decision Makers by Job Title", "Number of People", "Job Title", height=400
            )
            fig_titles = self.interactive_manager.create_interactive_chart(fig_titles, "job_title_chart")
            
            st.plotly_chart(fig_titles, use_container_width=True, key="dm_titles")
        
        # Geographic distribution
        st.markdown('<h2 class="section-header">🌍 Geographic Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            state_counts = filtered_decision_makers['State'].value_counts()
            fig_state = self.chart_creator.create_horizontal_bar(
                state_counts, "Decision Makers by State", "Number of Decision Makers", "State", height=400
            )
            fig_state = self.interactive_manager.create_interactive_chart(fig_state, "state_chart")
            
            st.plotly_chart(fig_state, use_container_width=True, key="dm_state")
        
        with col2:
            country_counts = filtered_decision_makers['Country'].value_counts()
            fig_country = self.chart_creator.create_pie_chart(
                country_counts, "Decision Makers by Country"
            )
            fig_country = self.interactive_manager.create_interactive_chart(fig_country, "country_chart")
            
            st.plotly_chart(fig_country, use_container_width=True, key="dm_country")
        
        # Company representation
        st.markdown('<h2 class="section-header">🏢 Company Representation</h2>', unsafe_allow_html=True)
        company_counts = filtered_decision_makers['Company'].value_counts()
        fig_company = self.chart_creator.create_horizontal_bar(
            company_counts, "Decision Makers by Company", 
            "Number of Decision Makers", "Company", height=400
        )
        fig_company = self.interactive_manager.create_interactive_chart(fig_company, "company_chart")
        
        st.plotly_chart(fig_company, use_container_width=True, key="dm_company")
        
        # Data table (filtered)
        self._render_decision_makers_data_table(filtered_decision_makers)
        
        # Filter management on main screen
        # self.interactive_manager.create_filter_ui({}, "Filter Management")
    
    def render_jobs_page(self, jobs_df: pd.DataFrame):
        """Render the jobs dashboard page with interactive filtering"""
        st.markdown('<h1 class="main-header">💼 Jobs Analytics</h1>', unsafe_allow_html=True)
        
        # Manual filter controls on main screen
        st.markdown('<h2 class="section-header">🔧 Filter Controls</h2>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.interactive_manager.create_manual_filter_controls(jobs_df, 'Job Title', 'Job Title')
        
        with col2:
            self.interactive_manager.create_manual_filter_controls(jobs_df, 'Location', 'Location')
        
        with col3:
            self.interactive_manager.create_manual_filter_controls(jobs_df, 'Company Name', 'Company')
        
        # Apply filters to data
        filtered_jobs = self.interactive_manager.apply_filters_to_dataframe(
            jobs_df,
            {"Job Title": "Job Title", "Location": "Location", "Company": "Company Name"}
        )
        
        # Key metrics (updated based on filters)
        metrics = self.data_processor.get_jobs_metrics(filtered_jobs)
        self._render_metrics_grid(metrics, [
            "Total Job Postings", "Companies with Jobs", "Job Locations", "Jobs with Post Dates"
        ])
        
        # Job distribution
        st.markdown('<h2 class="section-header">💼 Job Distribution</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title_counts = filtered_jobs['Job Title'].value_counts()
            fig_job_titles = self.chart_creator.create_pie_chart(
                job_title_counts, "Jobs by Title"
            )
            fig_job_titles = self.interactive_manager.create_interactive_chart(fig_job_titles, "job_title_chart")
            
            st.plotly_chart(fig_job_titles, use_container_width=True, key="jobs_titles")
        
        with col2:
            company_job_counts = filtered_jobs['Company Name'].value_counts()
            fig_company_jobs = self.chart_creator.create_vertical_bar(
                company_job_counts, "Jobs by Company", "Company", "Number of Jobs"
            )
            fig_company_jobs = self.interactive_manager.create_interactive_chart(fig_company_jobs, "company_jobs_chart")
            
            st.plotly_chart(fig_company_jobs, use_container_width=True, key="jobs_company")
        
        # Geographic distribution
        st.markdown('<h2 class="section-header">🌍 Geographic Distribution</h2>', unsafe_allow_html=True)
        location_counts = filtered_jobs['Location'].value_counts()
        fig_location = self.chart_creator.create_vertical_bar(
            location_counts, "Jobs by Location", "Location", "Number of Jobs"
        )
        fig_location = self.interactive_manager.create_interactive_chart(fig_location, "location_chart")
        
        st.plotly_chart(fig_location, use_container_width=True, key="jobs_location")
        
        # Timeline analysis
        if filtered_jobs['Post On'].notna().any():
            st.markdown('<h2 class="section-header">📅 Job Posting Timeline</h2>', unsafe_allow_html=True)
            timeline_df = filtered_jobs[filtered_jobs['Post On'].notna()].copy()
            timeline_df['Post Date'] = pd.to_datetime(timeline_df['Post On']).dt.date
            timeline_counts = timeline_df['Post Date'].value_counts().sort_index()
            
            fig_timeline = self.chart_creator.create_line_chart(
                timeline_counts, "Job Postings Over Time", "Date", "Number of Job Postings"
            )
            fig_timeline = self.interactive_manager.create_interactive_chart(fig_timeline, "timeline_chart")
            
            st.plotly_chart(fig_timeline, use_container_width=True, key="jobs_timeline")
        
        # Data table (filtered)
        self._render_jobs_data_table(filtered_jobs)
        
        # Filter management on main screen
        # self.interactive_manager.create_filter_ui({}, "Filter Management")
    
    def _render_overview_metrics(self, companies_df: pd.DataFrame, 
                               decision_makers_df: pd.DataFrame, 
                               jobs_df: pd.DataFrame):
        """Render overview metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", len(companies_df))
        
        with col2:
            st.metric("Total Decision Makers", len(decision_makers_df))
        
        with col3:
            st.metric("Active Job Postings", len(jobs_df))
        
        with col4:
            unique_companies_with_jobs = jobs_df['Company Name'].nunique()
            st.metric("Companies with Jobs", unique_companies_with_jobs)
    
    def _render_metrics_grid(self, metrics: Dict[str, Any], labels: list):
        """Render metrics in a grid layout"""
        cols = st.columns(4)
        for i, (key, value) in enumerate(metrics.items()):
            if i < len(cols):
                with cols[i]:
                    if isinstance(value, float):
                        st.metric(labels[i], f"{value:.1f}")
                    else:
                        st.metric(labels[i], value)
    
    def _render_companies_data_table(self, companies_df: pd.DataFrame):
        """Render companies data table with filters"""
        st.markdown('<h2 class="section-header">📋 Companies Data</h2>', unsafe_allow_html=True)
        
        # Search and filter
        search_term = st.text_input("Search companies by name:", "")
        industry_filter = st.selectbox("Filter by industry:", ["All"] + list(companies_df['Primary Industry'].unique()))
        
        filtered_df = companies_df.copy()
        
        if search_term:
            filtered_df = filtered_df[filtered_df['Name'].str.contains(search_term, case=False, na=False)]
        
        if industry_filter != "All":
            filtered_df = filtered_df[filtered_df['Primary Industry'] == industry_filter]
        
        st.dataframe(
            filtered_df[['Name', 'Primary Industry', 'Size', 'Type', 'Location', 'Country']].head(50),
            use_container_width=True
        )
    
    def _render_decision_makers_data_table(self, decision_makers_df: pd.DataFrame):
        """Render decision makers data table with filters"""
        st.markdown('<h2 class="section-header">📋 Decision Makers Data</h2>', unsafe_allow_html=True)
        
        # Search and filter
        search_term = st.text_input("Search by name or company:", "")
        title_filter = st.selectbox("Filter by job title:", ["All"] + list(decision_makers_df['Job Title'].unique()))
        
        filtered_df = decision_makers_df.copy()
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Full Name'].str.contains(search_term, case=False, na=False) |
                filtered_df['Company'].str.contains(search_term, case=False, na=False)
            ]
        
        if title_filter != "All":
            filtered_df = filtered_df[filtered_df['Job Title'] == title_filter]
        
        st.dataframe(
            filtered_df[['Full Name', 'Job Title', 'Company', 'Location']].head(50),
            use_container_width=True
        )
    
    def _render_jobs_data_table(self, jobs_df: pd.DataFrame):
        """Render jobs data table with filters"""
        st.markdown('<h2 class="section-header">📋 Jobs Data</h2>', unsafe_allow_html=True)
        
        # Search and filter
        search_term = st.text_input("Search jobs by title or company:", "")
        location_filter = st.selectbox("Filter by location:", ["All"] + list(jobs_df['Location'].unique()))
        
        filtered_df = jobs_df.copy()
        
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Job Title'].str.contains(search_term, case=False, na=False) |
                filtered_df['Company Name'].str.contains(search_term, case=False, na=False)
            ]
        
        if location_filter != "All":
            filtered_df = filtered_df[filtered_df['Location'] == location_filter]
        
        st.dataframe(
            filtered_df[['Job Title', 'Company Name', 'Location', 'Post On']].head(50),
            use_container_width=True
        ) 