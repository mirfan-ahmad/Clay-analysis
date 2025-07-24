import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Any
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class InteractiveManager:
    """Manages interactive filtering and cross-chart communication"""
    
    def __init__(self):
        self.filters = {}
        self.original_data = {}
        self.filtered_data = {}
        
    def initialize_session_state(self):
        """Initialize session state for filters"""
        if 'filters' not in st.session_state:
            st.session_state.filters = {}
        if 'selected_industry' not in st.session_state:
            st.session_state.selected_industry = None
        if 'selected_size' not in st.session_state:
            st.session_state.selected_size = None
        if 'selected_location' not in st.session_state:
            st.session_state.selected_location = None
        if 'selected_seniority' not in st.session_state:
            st.session_state.selected_seniority = None
        if 'selected_job_title' not in st.session_state:
            st.session_state.selected_job_title = None
    
    def add_filter(self, filter_name: str, filter_value: Any):
        """Add or update a filter"""
        st.session_state.filters[filter_name] = filter_value
    
    def remove_filter(self, filter_name: str):
        """Remove a filter"""
        if filter_name in st.session_state.filters:
            del st.session_state.filters[filter_name]
    
    def clear_all_filters(self):
        """Clear all filters"""
        st.session_state.filters = {}
        st.session_state.selected_industry = None
        st.session_state.selected_size = None
        st.session_state.selected_location = None
        st.session_state.selected_seniority = None
        st.session_state.selected_job_title = None
    
    def get_active_filters(self) -> Dict[str, Any]:
        """Get all active filters"""
        return st.session_state.filters.copy()
    
    def apply_filters_to_dataframe(self, df: pd.DataFrame, filter_config: Dict[str, str]) -> pd.DataFrame:
        """Apply filters to a dataframe"""
        filtered_df = df.copy()
        
        for filter_name, column_name in filter_config.items():
            if filter_name in st.session_state.filters:
                filter_value = st.session_state.filters[filter_name]
                if filter_value and filter_value != "All":
                    filtered_df = filtered_df[filtered_df[column_name] == filter_value]
        
        return filtered_df
    
    def create_manual_filter_controls(self, df: pd.DataFrame, column: str, filter_name: str):
        """Create manual filter controls for a specific column"""
        unique_values = ["All"] + list(df[column].unique())
        selected_value = st.selectbox(
            f"Filter by {filter_name}:",
            unique_values,
            key=f"filter_{filter_name}"
        )
        
        if selected_value == "All":
            # Automatically remove filter when "All" is selected
            self.remove_filter(filter_name)
        elif selected_value != "All":
            self.add_filter(filter_name, selected_value)
        
        return selected_value
    
    def create_filter_ui(self, filter_options: Dict[str, List[str]], title: str = "Active Filters"):
        """Create a filter UI component for main screen"""
        st.markdown(f"### {title}")
        
        # Show active filters
        active_filters = self.get_active_filters()
        if active_filters:
            st.markdown("**Active Filters:**")
            filter_cols = st.columns(min(len(active_filters), 3))
            
            for i, (filter_name, filter_value) in enumerate(active_filters.items()):
                col_idx = i % 3
                with filter_cols[col_idx]:
                    st.write(f"• {filter_name}: {filter_value}")
                    if st.button("❌ Remove", key=f"remove_{filter_name}"):
                        self.remove_filter(filter_name)
                        st.rerun()
            
            if st.button("🗑️ Clear All Filters"):
                self.clear_all_filters()
                st.rerun()
        else:
            st.info("No filters applied - Showing all data")
        
        st.markdown("---")
    
    def create_interactive_chart(self, fig: go.Figure, chart_name: str, 
                               filter_column: str = None) -> go.Figure:
        """Create an interactive chart with click handling"""
        # Add custom JavaScript for click handling
        fig.update_layout(
            clickmode="event+select",
            dragmode='select'
        )
        
        # Add custom hover template based on chart type
        for trace in fig.data:
            if trace.type == 'pie':
                # Pie charts use different hover properties
                trace.update(
                    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                    hoverinfo='label+value+percent'
                )
            elif trace.type == 'bar':
                # Bar charts
                if trace.orientation == 'h':
                    # Horizontal bar charts
                    trace.update(
                        hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
                        hoverinfo='y+x'
                    )
                else:
                    # Vertical bar charts
                    trace.update(
                        hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
                        hoverinfo='x+y'
                    )
            elif trace.type == 'scatter':
                # Scatter plots
                trace.update(
                    hovertemplate="<b>%{x}</b><br>Value: %{y}<extra></extra>",
                    hoverinfo='x+y'
                )
            else:
                # Default for other chart types
                trace.update(
                    hovertemplate="<b>%{fullData.name}</b><br>Value: %{y}<extra></extra>",
                    hoverinfo='y'
                )
        
        return fig
    
    def render_filter_status(self):
        """Render current filter status"""
        active_filters = self.get_active_filters()
        
        if active_filters:
            st.info(f"**Active Filters:** {len(active_filters)} filter(s) applied")
            for filter_name, filter_value in active_filters.items():
                st.write(f"• {filter_name}: {filter_value}")
        else:
            st.success("**No filters applied** - Showing all data")
    
    def create_drill_down_chart(self, df: pd.DataFrame, drill_column: str, 
                               value_column: str, title: str) -> go.Figure:
        """Create a drill-down chart that responds to selections"""
        # Apply current filters
        filtered_df = self.apply_filters_to_dataframe(df, {})
        
        # Group by drill column and count
        drill_data = filtered_df[drill_column].value_counts()
        
        # Create interactive chart
        fig = go.Figure(data=[
            go.Bar(
                x=drill_data.values,
                y=drill_data.index,
                orientation='h',
                marker_color=self.get_color_scale(len(drill_data))
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Count",
            yaxis_title=drill_column,
            height=400,
            clickmode="event+select",
            dragmode='select'
        )
        
        return fig
    
    def get_color_scale(self, n_colors: int) -> List[str]:
        """Get a color scale for charts"""
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        return colors[:n_colors]
    
    def create_cross_filter_dashboard(self, data_dict: Dict[str, pd.DataFrame], 
                                    chart_configs: List[Dict[str, Any]]) -> List[go.Figure]:
        """Create a cross-filter dashboard with multiple interactive charts"""
        charts = []
        
        for config in chart_configs:
            chart_name = config['name']
            chart_type = config['type']
            data_key = config['data_key']
            x_col = config.get('x_col')
            y_col = config.get('y_col')
            title = config['title']
            
            # Get filtered data
            df = self.apply_filters_to_dataframe(data_dict[data_key], config.get('filters', {}))
            
            if chart_type == 'bar':
                if config.get('orientation') == 'h':
                    fig = go.Figure(data=[
                        go.Bar(
                            x=df[x_col].value_counts().values,
                            y=df[x_col].value_counts().index,
                            orientation='h',
                            marker_color=self.get_color_scale(len(df[x_col].value_counts()))
                        )
                    ])
                else:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=df[x_col].value_counts().index,
                            y=df[x_col].value_counts().values,
                            marker_color=self.get_color_scale(len(df[x_col].value_counts()))
                        )
                    ])
            
            elif chart_type == 'pie':
                fig = go.Figure(data=[
                    go.Pie(
                        labels=df[x_col].value_counts().index,
                        values=df[x_col].value_counts().values
                    )
                ])
            
            # Add interactive features
            fig.update_layout(
                title=title,
                clickmode="event+select",
                dragmode='select'
            )
            
            charts.append(fig)
        
        return charts 