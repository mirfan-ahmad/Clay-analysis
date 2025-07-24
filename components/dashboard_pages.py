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
        """Render the executive overview with strategic KPIs"""
        # Executive KPIs
        self._render_executive_kpis(companies_df, decision_makers_df, jobs_df)
        
        # Strategic insights in 2x2 grid
        col1, col2 = st.columns(2)
        
        with col1:
            # Market concentration analysis
            st.markdown("**Market Concentration by Industry**")
            st.markdown("*This chart reveals which industries dominate our market landscape, helping identify where the most business opportunities exist and which sectors are most competitive.*")
            
            industry_counts = companies_df['Primary Industry'].value_counts().head(6)
            fig_market = self.chart_creator.create_horizontal_bar(
                industry_counts, "Market Concentration by Industry", "Number of Companies", "Industry"
            )
            st.plotly_chart(fig_market, use_container_width=True, key="overview_market")
        
        with col2:
            # Leadership distribution
            st.markdown("**Leadership Distribution by Seniority**")
            st.markdown("*This visualization shows the breakdown of decision makers by their level of authority, helping us understand who holds the power to make important business decisions.*")
            
            seniority_counts = decision_makers_df['Seniority'].value_counts()
            fig_leadership = self.chart_creator.create_pie_chart(
                seniority_counts, "Leadership Distribution by Seniority"
            )
            st.plotly_chart(fig_leadership, use_container_width=True, key="overview_leadership")
        
        # # Market penetration analysis
        # st.markdown('<h3 class="section-header">🎯 Market Penetration Analysis</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows which companies have both strong leadership presence and active hiring, indicating organizations that are growing and have multiple decision makers we can engage with.*")
        
        # # Companies with both decision makers and jobs
        # companies_with_dm = set(decision_makers_df['Company'].unique())
        # companies_with_jobs = set(jobs_df['Company Name'].unique())
        # companies_with_both = companies_with_dm.intersection(companies_with_jobs)
        
        # penetration_data = pd.Series({
        #     'Companies with Decision Makers Only': len(companies_with_dm - companies_with_jobs),
        #     'Companies with Jobs Only': len(companies_with_jobs - companies_with_dm),
        #     'Companies with Both': len(companies_with_both),
        #     'Companies with Neither': len(set(companies_df['Name'].unique()) - companies_with_dm - companies_with_jobs)
        # })
        
        # fig_penetration = self.chart_creator.create_pie_chart(
        #     penetration_data, "Market Penetration Analysis"
        # )
        # st.plotly_chart(fig_penetration, use_container_width=True, key="overview_penetration")
        
        # Geographic market presence
        st.markdown('<h3 class="section-header">🌍 Geographic Market Presence</h3>', unsafe_allow_html=True)
        st.markdown("*This chart shows where our target companies are located globally, helping identify which markets are most active and where we should focus our expansion efforts.*")
        
        country_counts = companies_df['Country'].value_counts().head(8)
        fig_geography = self.chart_creator.create_vertical_bar(
            country_counts, "Companies by Geographic Market"
        )
        st.plotly_chart(fig_geography, use_container_width=True, key="overview_geography")
        
        # Market activity timeline
        if jobs_df['Post On'].notna().any():
            st.markdown('<h3 class="section-header">📈 Market Activity Timeline</h3>', unsafe_allow_html=True)
            st.markdown("*This timeline tracks hiring activity over time, showing when companies are most active in recruiting and revealing seasonal patterns in business growth.*")
            
            timeline_df = jobs_df[jobs_df['Post On'].notna()].copy()
            timeline_df['Post Date'] = pd.to_datetime(timeline_df['Post On']).dt.date
            timeline_counts = timeline_df['Post Date'].value_counts().sort_index()
            
            fig_timeline = self.chart_creator.create_line_chart(
                timeline_counts, "Job Market Activity Over Time", "Date", "Job Postings"
            )
            st.plotly_chart(fig_timeline, use_container_width=True, key="overview_timeline")
    
    def render_companies_page(self, companies_df: pd.DataFrame):
        """Render strategic company intelligence"""
        # Strategic metrics
        metrics = self.data_processor.get_companies_metrics(companies_df)
        self._render_metrics_grid(metrics, [
            "Total Companies", "Unique Industries", "States Covered", "Private Companies"
        ])
        
        # Strategic analysis in 2x2 grid
        col1, col2 = st.columns(2)
        
        with col1:
            # Industry market share
            st.markdown("**Industry Market Share**")
            st.markdown("*This chart shows which industries have the most companies, helping us understand where the biggest business opportunities lie and which sectors are most competitive.*")
            
            industry_counts = companies_df['Primary Industry'].value_counts().head(8)
            fig_industry = self.chart_creator.create_horizontal_bar(
                industry_counts, "Industry Market Share", "Number of Companies", "Industry"
            )
            st.plotly_chart(fig_industry, use_container_width=True, key="companies_industry")
        
        with col2:
            # Company size distribution
            st.markdown("**Company Size Distribution**")
            st.markdown("*This chart reveals whether our market is dominated by small startups, mid-size companies, or large enterprises, helping us understand the business landscape and target the right company types.*")
            
            size_counts = companies_df['Size'].value_counts()
            fig_size = self.chart_creator.create_pie_chart(size_counts, "Company Size Distribution")
            st.plotly_chart(fig_size, use_container_width=True, key="companies_size")
        
        # # Competitive intelligence - companies with digital presence
        # st.markdown('<h3 class="section-header">💻 Digital Presence Analysis</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows which companies have strong digital footprints with both LinkedIn profiles and websites, indicating organizations that are more likely to be receptive to digital outreach and modern business practices.*")
        
        # digital_presence = pd.Series({
        #     'LinkedIn + Website': len(companies_df[(companies_df['Has_LinkedIn']) & (companies_df['Has_Domain'])]),
        #     'LinkedIn Only': len(companies_df[(companies_df['Has_LinkedIn']) & (~companies_df['Has_Domain'])]),
        #     'Website Only': len(companies_df[(~companies_df['Has_LinkedIn']) & (companies_df['Has_Domain'])]),
        #     'No Digital Presence': len(companies_df[(~companies_df['Has_LinkedIn']) & (~companies_df['Has_Domain'])])
        # })
        
        # fig_digital = self.chart_creator.create_pie_chart(
        #     digital_presence, "Digital Presence Analysis"
        # )
        # st.plotly_chart(fig_digital, use_container_width=True, key="companies_digital")
        
        # # Geographic expansion opportunities
        # st.markdown('<h3 class="section-header">🌍 Geographic Expansion Opportunities</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows where companies are located around the world, helping us identify which markets are most active and where we should focus our business development efforts.*")
        
        # country_counts = companies_df['Country'].value_counts().head(10)
        # fig_country = self.chart_creator.create_vertical_bar(
        #     country_counts, "Companies by Geographic Market"
        # )
        # st.plotly_chart(fig_country, use_container_width=True, key="companies_country")
        
        # # Company type analysis
        # st.markdown('<h3 class="section-header">🏢 Company Type Analysis</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows the mix of public and private companies in our market, helping us understand the business model landscape and identify the best targets for our services.*")
        
        # type_counts = companies_df['Type'].value_counts()
        # fig_type = self.chart_creator.create_pie_chart(type_counts, "Company Type Distribution")
        # st.plotly_chart(fig_type, use_container_width=True, key="companies_type")
        
        # Data table with integrated export
        self._render_companies_data_table(companies_df)
    
    def render_decision_makers_page(self, decision_makers_df: pd.DataFrame, companies_df: pd.DataFrame):
        """Render strategic decision maker analysis"""
        # Strategic metrics
        metrics = self.data_processor.get_decision_makers_metrics(decision_makers_df)
        self._render_metrics_grid(metrics, [
            "Total Decision Makers", "Companies Represented", "Unique Job Titles", "Unique Locations"
        ])
        
        # Strategic analysis in 2x2 grid
        # col1, col2 = st.columns(2)
        
        # with col1:
        # Leadership hierarchy
        st.markdown("**Leadership Hierarchy Distribution**")
        st.markdown("*This chart shows the breakdown of decision makers by their level of authority, helping us understand who has the power to make important business decisions and approve deals.*")
        
        seniority_counts = decision_makers_df['Seniority'].value_counts()
        fig_seniority = self.chart_creator.create_pie_chart(
            seniority_counts, "Leadership Hierarchy Distribution"
        )
        st.plotly_chart(fig_seniority, use_container_width=True, key="dm_seniority")
        
        # with col2:
            # # Key decision maker roles
            # st.markdown("**Key Decision Maker Roles**")
            # st.markdown("*This chart identifies the most common job titles among decision makers, showing us which roles are most important for making business decisions and who we should target in our outreach.*")
            
            # title_counts = decision_makers_df['Job Title'].value_counts().head(8)
            # fig_titles = self.chart_creator.create_horizontal_bar(
            #     title_counts, "Key Decision Maker Roles", "Number of People", "Job Title"
            # )
            # st.plotly_chart(fig_titles, use_container_width=True, key="dm_titles")
        
        # # Decision maker influence mapping
        # st.markdown('<h3 class="section-header">🎯 Decision Maker Influence Mapping</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows which companies have the highest concentration of decision makers, helping us identify organizations where we have multiple potential entry points and stronger relationship opportunities.*")
        
        # # Calculate decision maker density per company
        # dm_density = decision_makers_df['Company'].value_counts().head(10)
        # fig_influence = self.chart_creator.create_horizontal_bar(
        #     dm_density, "Decision Maker Influence by Company", "Number of Decision Makers", "Company"
        # )
        # st.plotly_chart(fig_influence, use_container_width=True, key="dm_influence")
        
        # Geographic leadership distribution
        st.markdown('<h3 class="section-header">🌍 Geographic Leadership Distribution</h3>', unsafe_allow_html=True)
        st.markdown("*This chart shows where decision makers are located geographically, helping us identify which regions have the most business leaders and where we should focus our relationship building efforts.*")
        
        state_counts = decision_makers_df['State'].value_counts().head(10)
        fig_state = self.chart_creator.create_vertical_bar(
            state_counts, "Decision Makers by Geographic Location"
        )
        st.plotly_chart(fig_state, use_container_width=True, key="dm_state")
        
        # Comprehensive decision maker distribution across all companies
        st.markdown('<h3 class="section-header">🏢 Decision Maker Distribution Across All Companies</h3>', unsafe_allow_html=True)
        st.markdown("*This comprehensive visualization shows decision makers across all companies in our database, helping us understand the complete market landscape and identify companies with strong leadership presence regardless of size.*")
        
        # Group by company and count decision makers
        company_dm_counts = decision_makers_df['Company'].value_counts()
        
        # Create treemap chart for all companies
        fig_treemap = self.chart_creator.create_treemap_chart(
            company_dm_counts, "Decision Makers Across All Companies"
        )
        st.plotly_chart(fig_treemap, use_container_width=True, key="dm_treemap_all")
        
        # # Company representation analysis (top companies)
        # st.markdown('<h3 class="section-header">🏢 Top Companies by Decision Maker Count</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart highlights the companies with the highest concentration of decision makers, helping us identify organizations where we have multiple potential entry points and stronger relationship opportunities.*")
        
        # company_counts = decision_makers_df['Company'].value_counts().head(15)
        # fig_company = self.chart_creator.create_horizontal_bar(
        #     company_counts, "Top Companies by Decision Maker Count", "Number of Decision Makers", "Company"
        # )
        # st.plotly_chart(fig_company, use_container_width=True, key="dm_company")
        
        # Data table with integrated export
        self._render_decision_makers_data_table(decision_makers_df)
    
    def render_jobs_page(self, jobs_df: pd.DataFrame):
        """Render market intelligence and job analytics"""
        # Strategic metrics
        metrics = self.data_processor.get_jobs_metrics(jobs_df)
        self._render_metrics_grid(metrics, [
            "Total Job Postings", "Companies with Jobs", "Job Locations", "Jobs with Post Dates"
        ])
        
        # Market intelligence in 2x2 grid
        # col1, col2 = st.columns(2)
        
        # with col1:
            # # Skill demand analysis
            # st.markdown("**Skill Demand Analysis**")
            # st.markdown("*This chart shows which job titles are most in demand, helping us understand what skills companies are looking for and where the biggest hiring needs exist in the market.*")
            
            # job_title_counts = jobs_df['Job Title'].value_counts().head(8)
            # fig_skills = self.chart_creator.create_horizontal_bar(
            #     job_title_counts, "Skill Demand Analysis", "Number of Job Postings", "Job Title"
            # )
            # st.plotly_chart(fig_skills, use_container_width=True, key="jobs_skills")
        
        # with col2:
            # Company hiring activity
        st.markdown("**Company Hiring Activity**")
        st.markdown("*This chart shows which companies are hiring the most, helping us identify organizations that are growing and might be more open to new business opportunities.*")
        
        company_job_counts = jobs_df['Company Name'].value_counts().head(8)
        fig_hiring = self.chart_creator.create_vertical_bar(
            company_job_counts, "Company Hiring Activity"
        )
        st.plotly_chart(fig_hiring, use_container_width=True, key="jobs_hiring")
        
        # # Business opportunity scoring
        # st.markdown('<h3 class="section-header">🎯 Business Opportunity Scoring</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart identifies companies that are actively hiring and likely growing, helping us prioritize which organizations to approach first based on their current business activity and expansion needs.*")
        
        # # Calculate opportunity score (companies with multiple job postings)
        # opportunity_scores = jobs_df['Company Name'].value_counts()
        # high_opportunity = opportunity_scores[opportunity_scores > 1].head(8)
        
        # fig_opportunity = self.chart_creator.create_horizontal_bar(
        #     high_opportunity, "High-Growth Companies (Multiple Job Postings)", "Number of Job Postings", "Company"
        # )
        # st.plotly_chart(fig_opportunity, use_container_width=True, key="jobs_opportunity")
        
        # Geographic job market
        # st.markdown('<h3 class="section-header">🌍 Geographic Job Market</h3>', unsafe_allow_html=True)
        # st.markdown("*This chart shows where job opportunities are located, helping us understand which markets are most active and where companies are expanding their operations.*")
        
        # location_counts = jobs_df['Location'].value_counts().head(10)
        # fig_location = self.chart_creator.create_vertical_bar(
        #     location_counts, "Job Opportunities by Location"
        # )
        # st.plotly_chart(fig_location, use_container_width=True, key="jobs_location")
        
        # Market activity timeline
        if jobs_df['Post On'].notna().any():
            st.markdown('<h3 class="section-header">📈 Market Activity Timeline</h3>', unsafe_allow_html=True)
            st.markdown("*This timeline shows hiring activity over time, helping us understand when companies are most active in recruiting and identify seasonal patterns in business growth.*")
            
            timeline_df = jobs_df[jobs_df['Post On'].notna()].copy()
            timeline_df['Post Date'] = pd.to_datetime(timeline_df['Post On']).dt.date
            timeline_counts = timeline_df['Post Date'].value_counts().sort_index()
            
            fig_timeline = self.chart_creator.create_line_chart(
                timeline_counts, "Job Market Activity Over Time", "Date", "Job Postings"
            )
            st.plotly_chart(fig_timeline, use_container_width=True, key="jobs_timeline")
        
        # Data table with integrated export
        self._render_jobs_data_table(jobs_df)
    
    def _render_executive_kpis(self, companies_df: pd.DataFrame, 
                              decision_makers_df: pd.DataFrame, 
                              jobs_df: pd.DataFrame):
        """Render executive KPIs"""
        st.markdown('<h3 class="section-header">📊 Executive KPIs</h3>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Market Size", len(companies_df))
        
        with col2:
            st.metric("Leadership Pool", len(decision_makers_df))
        
        with col3:
            st.metric("Active Opportunities", len(jobs_df))
        
        with col4:
            unique_companies_with_jobs = jobs_df['Company Name'].nunique()
            st.metric("Companies Hiring", unique_companies_with_jobs)
    
    def _render_metrics_grid(self, metrics: Dict[str, Any], labels: list):
        """Render metrics in a grid layout"""
        st.markdown('<h3 class="section-header">📊 Key Metrics</h3>', unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (key, value) in enumerate(metrics.items()):
            if i < len(cols):
                with cols[i]:
                    if isinstance(value, float):
                        st.metric(labels[i], f"{value:.1f}")
                    else:
                        st.metric(labels[i], value)
    
    def _render_companies_data_table(self, companies_df: pd.DataFrame):
        """Render companies data table with integrated export"""
        st.markdown('<h3 class="section-header">📋 Company Intelligence Data</h3>', unsafe_allow_html=True)
        
        # Create display dataframe with direct URLs
        display_df = companies_df[['Name', 'Primary Industry', 'Size', 'Location', 'LinkedIn URL', 'Domain']].copy()
        
        # Rename columns for better display
        display_df = display_df.rename(columns={
            'LinkedIn URL': 'LinkedIn Profile',
            'Domain': 'Company Website'
        })
        
        # Use st.dataframe with direct URLs
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "LinkedIn Profile": st.column_config.LinkColumn("LinkedIn Profile"),
                "Company Website": st.column_config.LinkColumn("Company Website")
            }
        )
        
        # Export functionality
        csv_data = companies_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Company Data (CSV)",
            data=csv_data,
            file_name="company_intelligence_data.csv",
            mime="text/csv",
            key="export_companies_csv"
        )
    
    def _render_decision_makers_data_table(self, decision_makers_df: pd.DataFrame):
        """Render decision makers data table with integrated export"""
        st.markdown('<h3 class="section-header">📋 Decision Maker Intelligence Data</h3>', unsafe_allow_html=True)
        
        # Create display dataframe with direct URLs
        display_df = decision_makers_df[['Full Name', 'Job Title', 'Company', 'Location', 'LinkedIn URL']].copy()
        
        # Rename columns for better display
        display_df = display_df.rename(columns={
            'LinkedIn URL': 'LinkedIn Profile'
        })
        
        # Use st.dataframe with direct URLs
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "LinkedIn Profile": st.column_config.LinkColumn("LinkedIn Profile")
            }
        )
        
        # Export functionality
        csv_data = decision_makers_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Decision Maker Data (CSV)",
            data=csv_data,
            file_name="decision_maker_intelligence_data.csv",
            mime="text/csv",
            key="export_dm_csv"
        )
    
    def _render_jobs_data_table(self, jobs_df: pd.DataFrame):
        """Render jobs data table with integrated export"""
        st.markdown('<h3 class="section-header">📋 Market Intelligence Data</h3>', unsafe_allow_html=True)
        
        # Create display dataframe with direct URLs
        display_df = jobs_df[['Job Title', 'Company Name', 'Location', 'Post On', 'Job URL']].copy()
        
        # Rename columns for better display
        display_df = display_df.rename(columns={
            'Job URL': 'Apply Now'
        })
        
        # Use st.dataframe with direct URLs
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Apply Now": st.column_config.LinkColumn("Apply Now")
            }
        )
        
        # Export functionality
        csv_data = jobs_df.to_csv(index=False)
        st.download_button(
            label="📥 Export Market Intelligence Data (CSV)",
            data=csv_data,
            file_name="market_intelligence_data.csv",
            mime="text/csv",
            key="export_jobs_csv"
        ) 