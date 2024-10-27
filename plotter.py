# https://d-nb.info/1174250364/34#page=24&zoom=100,0,0
import pandas

import return_calculator as ReturnCalculator
import pandas as pd
import matplotlib
import plotly.graph_objs as go
from entropy import get_entropy

# Set the backend to a non-inline backend that supports interactive windows
matplotlib.use('TkAgg')  # or 'Qt5Agg', depending on your preference

class Plotter:
    def __init__(self, return_calculator: ReturnCalculator) -> None:
        self.return_calculator = return_calculator

    def plot_skewness_entropy_and_returns(self, ticker: str, dataframe: pandas.DataFrame, demo: bool = True):
        if demo:
            merged_df = dataframe
        else:
            # Fetch the data for the ticker
            data = self.return_calculator.financial_data[ticker].get_data()
            if data.empty:
                print(f"No data available for ticker {ticker}")
                return

            daily_returns = self.return_calculator.calculate_daily_returns(ticker)
            entropy_df = get_entropy()
            merged_df = pd.merge(entropy_df, daily_returns, left_on='Date', right_index=True, how='inner')

        # Save the entropy data into the database
        # save_entropy_data_to_db(merged_df[['Date', 'Adj Close', 'Entropy', 'Skewness']])

        fig = go.Figure()

        # Entropy (blue)
        fig.add_trace(go.Scatter(
            x=merged_df['Date'],
            y=merged_df['Entropy'],
            mode='lines+markers',
            name='Entropy',
            marker=dict(color='blue', size=3),
            line=dict(color='blue'),
            yaxis='y1',
            hovertemplate='Entropy: %{y:.4f}<extra></extra>'
        ))

        # SPX Price (green) on the primary y-axis
        fig.add_trace(go.Scatter(
            x=merged_df['Date'],
            y=merged_df['Adj Close'],
            mode='lines+markers',
            name='SPX Price',
            marker=dict(color='green', symbol='triangle-up', size=4),
            line=dict(color='green'),
            yaxis='y2',
            hovertemplate='SPX Price: %{y:.2f}<extra></extra>'
        ))

        # Skewness (red)
        fig.add_trace(go.Scatter(
            x=merged_df['Date'],
            y=merged_df['Skewness'],
            mode='lines+markers',
            name='Skewness',
            marker=dict(color='red', symbol='x', size=4),
            line=dict(color='red'),
            yaxis='y3',
            hovertemplate='Skewness: %{y:.4f}<extra></extra>'
        ))

        # Update layout for multiple y-axes
        fig.update_layout(
            title=f'Entropy, Skewness, and SPX Index for {ticker} Over Time',
            xaxis=dict(title='Date', tickformat='%Y-%m-%d'),
            yaxis=dict(
                title='Entropy',
                titlefont=dict(color='blue'),
                tickfont=dict(color='blue'),
                showgrid=False,
            ),
            yaxis2=dict(
                title='SPX Price',
                titlefont=dict(color='green'),
                tickfont=dict(color='green'),
                overlaying='y',  # Overlays SPX Price on the same axis
                side='right',
                showgrid=False,
                automargin=True,  # Ensure the y-axis adjusts based on data range when zoomed
                range=[merged_df['Adj Close'].min(), merged_df['Adj Close'].max()]  # SPX price range
            ),
            yaxis3=dict(
                title='Skewness',
                titlefont=dict(color='red'),
                tickfont=dict(color='red'),
                overlaying='y',  # Overlays Skewness on the same axis
                side='right',
                position=0.95,  # Moves Skewness to the far right
                showgrid=False,
                automargin=True
            ),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
            template='plotly_white'
        )

        # Show the plot in a browser
        fig.show()
