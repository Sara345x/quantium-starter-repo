import dash
from dash import html, dcc, Dash, Input, Output
import pandas as pd
import plotly.express as px

# Load processed data
df = pd.read_csv("data/formatted_output.csv")
df['Date'] = pd.to_datetime(df['Date']).dt.date
df.sort_values('Date', inplace=True)

# Get unique regions for dropdown
regions = df['Region'].unique()

# Initialize the app
app = Dash(__name__)

# Define the layout
background_color = '#E6E6FA'

# Layout
app.layout = html.Div(
    style={'backgroundColor': background_color, 'padding': '20px'},
    children=[
        html.H1(
            "Pink Morsel Sales Visualizer",
            style={'textAlign': 'center', 'color': 'black'}
        ),
        html.Label("Select Region:", style={'color': 'black', 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': r, 'value': r} for r in regions],
            value=regions[0],
            clearable=False,
            style={'width': '50%'}
        ),
        dcc.Graph(id='sales-line-chart')
    ]
)

# Callback
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-dropdown', 'value')
)
def update_chart(selected_region):
    filtered_df = df[df['Region'] == selected_region]

    # Group by Date and sum Sales
    grouped = (
        filtered_df
        .groupby('Date', as_index=False)['Sales']
        .sum()
    )

    fig = px.line(
        grouped,
        x='Date',
        y='Sales',
        title=f'Daily Pink Morsel Sales - {selected_region}',
        labels={'Sales': 'Total Sales', 'Date': 'Date'}
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#E6E6FA',
        font_color='black'
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)