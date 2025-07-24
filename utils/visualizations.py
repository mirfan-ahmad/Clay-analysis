import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional, Callable
import streamlit as st

class ChartCreator:
    """Handles all chart creation and styling"""
    
    def __init__(self):
        """Initialize with professional color palette"""
        # Professional color palette for business dashboards
        self.color_palette = [
            '#1f4e79',  # Dark blue (primary)
            '#2c5aa0',  # Medium blue
            '#4a90e2',  # Light blue
            '#28a745',  # Green
            '#ffc107',  # Yellow
            '#dc3545',  # Red
            '#6c757d',  # Gray
            '#17a2b8',  # Cyan
            '#fd7e14',  # Orange
            '#6f42c1',  # Purple
            '#e83e8c',  # Pink
            '#20c997'   # Teal
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
    
    def create_horizontal_bar(self, data: pd.Series, title: str, x_label: str = "", 
                            y_label: str = "", height: int = 400) -> go.Figure:
        """Create a horizontal bar chart with professional styling"""
        fig = go.Figure(data=[
            go.Bar(
                y=data.index,
                x=data.values,
                orientation='h',
                marker_color=self.color_palette[0],
                marker_line_color='#ffffff',
                marker_line_width=1,
                text=data.values,
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        return fig
    
    def create_pie_chart(self, data: pd.Series, title: str, height: int = 400) -> go.Figure:
        """Create a pie chart with professional styling"""
        fig = go.Figure(data=[
            go.Pie(
                labels=data.index,
                values=data.values,
                marker_colors=self.color_palette[:len(data)],
                textinfo='label+percent',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#dee2e6',
                borderwidth=1
            )
        )
        
        return fig
    
    def create_vertical_bar(self, data: pd.Series, title: str, x_label: str = "", 
                          y_label: str = "", height: int = 400) -> go.Figure:
        """Create a vertical bar chart with professional styling"""
        fig = go.Figure(data=[
            go.Bar(
                x=data.index,
                y=data.values,
                marker_color=self.color_palette[1],
                marker_line_color='#ffffff',
                marker_line_width=1,
                text=data.values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        return fig
    
    def create_line_chart(self, data: pd.Series, title: str, x_label: str = "", 
                         y_label: str = "", height: int = 400) -> go.Figure:
        """Create a line chart with professional styling"""
        fig = go.Figure(data=[
            go.Scatter(
                x=data.index,
                y=data.values,
                mode='lines+markers',
                line=dict(color=self.color_palette[2], width=3),
                marker=dict(color=self.color_palette[2], size=6),
                fill='tonexty',
                fillcolor='rgba(74, 144, 226, 0.1)',
                hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        return fig
    
    def create_sunburst_chart(self, data: pd.DataFrame, title: str, height: int = 500) -> go.Figure:
        """Create a sunburst chart with professional styling"""
        fig = go.Figure(data=[
            go.Sunburst(
                ids=data['ids'],
                labels=data['labels'],
                parents=data['parents'],
                values=data['values'],
                hovertemplate='<b>%{label}</b><br>Value: %{value}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_treemap_chart(self, data: pd.Series, title: str, height: int = 600) -> go.Figure:
        """Create a treemap chart with professional styling - perfect for showing many companies"""
        # Prepare data for treemap
        df_treemap = pd.DataFrame({
            'company': data.index,
            'count': data.values
        })
        
        # Create treemap
        fig = go.Figure(data=[
            go.Treemap(
                labels=df_treemap['company'],
                parents=[''] * len(df_treemap),  # All companies are at root level
                values=df_treemap['count'],
                textinfo="label+value",
                hovertemplate='<b>%{label}</b><br>Decision Makers: %{value}<extra></extra>',
                marker=dict(
                    colors=df_treemap['count'],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="Decision Makers")
                ),
                textfont=dict(size=10)
            )
        ])
        
        fig.update_layout(
            title=title,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_scatter_plot(self, x_data: pd.Series, y_data: pd.Series, title: str, 
                           x_label: str = "", y_label: str = "", height: int = 400) -> go.Figure:
        """Create a scatter plot with professional styling"""
        fig = go.Figure(data=[
            go.Scatter(
                x=x_data,
                y=y_data,
                mode='markers',
                marker=dict(
                    color=self.color_palette[3],
                    size=8,
                    opacity=0.7,
                    line=dict(color='#ffffff', width=1)
                ),
                hovertemplate='<b>X: %{x}</b><br>Y: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50),
            showlegend=False
        )
        
        fig.update_xaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor='#e9ecef',
            zeroline=False,
            showline=True,
            linecolor='#dee2e6',
            linewidth=1
        )
        
        return fig
    
    def create_heatmap(self, data: pd.DataFrame, title: str, height: int = 400) -> go.Figure:
        """Create a heatmap with professional styling"""
        fig = go.Figure(data=[
            go.Heatmap(
                z=data.values,
                x=data.columns,
                y=data.index,
                colorscale='Blues',
                hovertemplate='<b>%{y}</b><br><b>%{x}</b><br>Value: %{z}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=title,
            height=height,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50)
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
    
    def style_chart(self, fig: go.Figure) -> go.Figure:
        """Apply consistent professional styling to any chart"""
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial, sans-serif", size=12, color='#2c3e50'),
            title_font=dict(size=16, color='#1f4e79'),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def add_selection_callback(self, fig: go.Figure, callback_func: Callable):
        """Add selection callback to a chart"""
        fig.update_layout(
            clickmode="event+select",
            dragmode='select'
        )
        return fig 