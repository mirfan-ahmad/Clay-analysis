import pandas as pd
import streamlit as st
from typing import Tuple, Optional
import re

class DataProcessor:
    """Handles data loading and preprocessing for the Clay Analytics Dashboard"""
    
    def __init__(self):
        self.companies_df = None
        self.decision_makers_df = None
        self.jobs_df = None
    
    def load_data(self) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
        """Load all CSV data files with error handling"""
        return load_data_files()
    
    def preprocess_companies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess companies data"""
        df = df.copy()
        
        # Clean company names
        df['Name'] = df['Name'].fillna('Unknown')
        
        # Extract state from location
        df['State'] = df['Location'].str.extract(r',\s*([A-Z]{2}|[A-Za-z\s]+)$')
        df['State'] = df['State'].fillna('Unknown')
        
        # Clean industry data
        df['Primary Industry'] = df['Primary Industry'].fillna('Unknown')
        
        # Clean size data
        df['Size'] = df['Size'].fillna('Unknown')
        
        # Clean company type
        df['Type'] = df['Type'].fillna('Unknown')
        
        # Extract country
        df['Country'] = df['Country'].fillna('Unknown')
        
        # Add derived fields
        df['Has_LinkedIn'] = df['LinkedIn URL'].notna()
        df['Has_Domain'] = df['Domain'].notna()
        
        return df
    
    def preprocess_decision_makers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess decision makers data"""
        df = df.copy()
        
        # Clean names
        df['Full Name'] = df['Full Name'].fillna('Unknown')
        df['Job Title'] = df['Job Title'].fillna('Unknown')
        df['Location'] = df['Location'].fillna('Unknown')
        
        # Extract state from location
        df['State'] = df['Location'].str.extract(r',\s*([A-Z]{2}|[A-Za-z\s]+)$')
        df['State'] = df['State'].fillna('Unknown')
        
        # Extract company
        df['Company'] = df['Company Table Data'].fillna('Unknown')
        
        # Add seniority level
        df['Seniority'] = df['Job Title'].apply(self._get_seniority_level)
        
        # Extract country
        df['Country'] = df['Location'].apply(self._extract_country)
        
        return df
    
    def preprocess_jobs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess jobs data"""
        df = df.copy()
        
        # Clean job data
        df['Job Title'] = df['Job Title'].fillna('Unknown')
        df['Location'] = df['Location'].fillna('Unknown')
        df['Company Name'] = df['Company Name'].fillna('Unknown')
        
        # Convert post date to datetime and ensure timezone-naive
        df['Post On'] = pd.to_datetime(df['Post On'], errors='coerce')
        
        # Add derived fields
        df['Post Date'] = df['Post On'].dt.date
        df['Post Month'] = df['Post On'].dt.to_period('M')
        
        # Calculate days since posted (handle timezone issues)
        try:
            current_time = pd.Timestamp.now().tz_localize(None)  # Make timezone-naive
            # Ensure Post On is also timezone-naive
            df['Post On'] = df['Post On'].dt.tz_localize(None)
            df['Days Since Posted'] = (current_time - df['Post On']).dt.days
        except Exception:
            # If timezone handling fails, set to NaN
            df['Days Since Posted'] = pd.NA
        
        return df
    
    def _get_seniority_level(self, title: str) -> str:
        """Extract seniority level from job title"""
        title_lower = title.lower()
        if any(word in title_lower for word in ['ceo', 'president', 'founder', 'owner', 'principal']):
            return 'C-Level/Principal'
        elif any(word in title_lower for word in ['vp', 'vice president', 'director', 'head']):
            return 'VP/Director'
        elif any(word in title_lower for word in ['manager', 'lead', 'senior']):
            return 'Manager/Senior'
        else:
            return 'Other'
    
    def _extract_country(self, location: str) -> str:
        """Extract country from location string"""
        if pd.isna(location) or location == 'Unknown':
            return 'Unknown'
        if 'United States' in location:
            return 'United States'
        elif 'Canada' in location:
            return 'Canada'
        elif 'United Kingdom' in location:
            return 'United Kingdom'
        elif 'India' in location:
            return 'India'
        else:
            return 'Other'
    
    def get_companies_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate key metrics for companies"""
        return {
            'total_companies': len(df),
            'unique_industries': df['Primary Industry'].nunique(),
            'unique_states': df['State'].nunique(),
            'private_companies': len(df[df['Type'] == 'Privately Held']),
            'companies_with_linkedin': df['Has_LinkedIn'].sum(),
            'companies_with_domain': df['Has_Domain'].sum()
        }
    
    def get_decision_makers_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate key metrics for decision makers"""
        return {
            'total_decision_makers': len(df),
            'unique_companies': df['Company'].nunique(),
            'unique_titles': df['Job Title'].nunique(),
            'unique_locations': df['Location'].nunique(),
            'c_level_count': len(df[df['Seniority'] == 'C-Level/Principal']),
            'vp_director_count': len(df[df['Seniority'] == 'VP/Director'])
        }
    
    def get_jobs_metrics(self, df: pd.DataFrame) -> dict:
        """Calculate key metrics for jobs"""
        return {
            'total_jobs': len(df),
            'unique_companies': df['Company Name'].nunique(),
            'unique_locations': df['Location'].nunique(),
            'recent_jobs': len(df[df['Post On'].notna()]),
            'avg_days_since_posted': df['Days Since Posted'].mean()
        }

@st.cache_data
def load_data_files() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Load all CSV data files with caching"""
    try:
        companies_df = pd.read_csv("data/companies.csv", encoding='utf-8')
        decision_makers_df = pd.read_csv("data/decision-makers.csv", encoding='utf-8')
        jobs_df = pd.read_csv("data/jobs.csv", encoding='utf-8')
        return companies_df, decision_makers_df, jobs_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None 