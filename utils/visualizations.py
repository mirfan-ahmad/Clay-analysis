import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional, Callable
import streamlit as st

class ChartCreator:
    """Handles creation of all visualizations for the dashboard"""
    
    def __init__(self):
        # Define consistent color schemes
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'light': '#8c564b',
            'dark': '#e377c2'
        }
        
        self.color_palette = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
    
    def create_metric_card(self, title: str, value: str, delta: Optional[str] = None, 
                          delta_color: str = "normal") -> go.Figure:
        """Create a metric card visualization"""
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="number+delta" if delta else "number",
            value=value,
            delta={'reference': delta} if delta else None,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        
        fig.update_layout(
            height=120,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(size=16)
        )
        
        return fig
    
    def create_horizontal_bar(self, data: pd.Series, title: str, 
                            x_label: str = "Count", y_label: str = "Category",
                            color: str = None, height: int = 400, 
                            clickmode: str = "event+select") -> go.Figure:
        """Create an interactive horizontal bar chart"""
        fig = px.bar(
            x=data.values,
            y=data.index,
            orientation='h',
            title=title,
            labels={'x': x_label, 'y': y_label},
            color_discrete_sequence=[color] if color else self.color_palette
        )
        
        fig.update_layout(
            height=height,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode,
            dragmode='select'
        )
        
        # Add interactive features
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
            hoverinfo='x+y'
        )
        
        return fig
    
    def create_pie_chart(self, data: pd.Series, title: str, 
                        height: int = 400, clickmode: str = "event+select") -> go.Figure:
        """Create an interactive pie chart"""
        fig = px.pie(
            values=data.values,
            names=data.index,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            height=height,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode
        )
        
        # Add interactive features
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
            hoverinfo='label+value+percent'
        )
        
        return fig
    
    def create_vertical_bar(self, data: pd.Series, title: str,
                          x_label: str = "Category", y_label: str = "Count",
                          color: str = None, height: int = 400, 
                          clickmode: str = "event+select") -> go.Figure:
        """Create an interactive vertical bar chart"""
        fig = px.bar(
            x=data.index,
            y=data.values,
            title=title,
            labels={'x': x_label, 'y': y_label},
            color_discrete_sequence=[color] if color else self.color_palette
        )
        
        fig.update_layout(
            height=height,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode,
            dragmode='select'
        )
        
        # Add interactive features
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
            hoverinfo='x+y'
        )
        
        return fig
    
    def create_line_chart(self, data: pd.Series, title: str,
                         x_label: str = "Date", y_label: str = "Count",
                         height: int = 400, clickmode: str = "event+select") -> go.Figure:
        """Create an interactive line chart"""
        fig = px.line(
            x=data.index,
            y=data.values,
            title=title,
            labels={'x': x_label, 'y': y_label},
            color_discrete_sequence=[self.colors['primary']]
        )
        
        fig.update_layout(
            height=height,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode,
            dragmode='select'
        )
        
        # Add interactive features
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
            hoverinfo='x+y'
        )
        
        return fig
    
    def create_sunburst_chart(self, df: pd.DataFrame, path: List[str], 
                            values: str, title: str, height: int = 500,
                            clickmode: str = "event+select") -> go.Figure:
        """Create an interactive sunburst chart for hierarchical data"""
        fig = px.sunburst(
            df,
            path=path,
            values=values,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            height=height,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode
        )
        
        return fig
    
    def create_scatter_plot(self, df: pd.DataFrame, x: str, y: str, 
                          color: str = None, size: str = None,
                          title: str = "", height: int = 400,
                          clickmode: str = "event+select") -> go.Figure:
        """Create an interactive scatter plot"""
        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size=size,
            title=title,
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            height=height,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode,
            dragmode='select'
        )
        
        return fig
    
    def create_heatmap(self, data: pd.DataFrame, title: str,
                      height: int = 400, clickmode: str = "event+select") -> go.Figure:
        """Create an interactive heatmap"""
        fig = px.imshow(
            data,
            title=title,
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            height=height,
            margin=dict(l=20, r=20, t=40, b=20),
            title_x=0.5,
            clickmode=clickmode
        )
        
        return fig
    
    def create_subplot_charts(self, charts: List[go.Figure], 
                            rows: int, cols: int, 
                            subplot_titles: List[str] = None) -> go.Figure:
        """Create subplot layout with multiple charts"""
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=subplot_titles,
            specs=[[{"secondary_y": False}] * cols] * rows
        )
        
        for i, chart in enumerate(charts):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            for trace in chart.data:
                fig.add_trace(trace, row=row, col=col)
        
        fig.update_layout(
            height=300 * rows,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20),
            clickmode="event+select"
        )
        
        return fig
    
    def create_metric_grid(self, metrics: Dict[str, str], 
                          cols: int = 4) -> List[go.Figure]:
        """Create a grid of metric cards"""
        metric_cards = []
        for title, value in metrics.items():
            card = self.create_metric_card(title, value)
            metric_cards.append(card)
        return metric_cards
    
    def style_chart(self, fig: go.Figure, template: str = "plotly_white") -> go.Figure:
        """Apply consistent styling to a chart"""
        fig.update_layout(
            template=template,
            font=dict(family="Arial", size=12),
            title_font=dict(size=16, color=self.colors['primary']),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray',
                zeroline=False
            ),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        return fig
    
    def add_selection_callback(self, fig: go.Figure, callback_func: Callable):
        """Add selection callback to a chart"""
        fig.update_layout(
            clickmode="event+select",
            dragmode='select'
        )
        return fig 