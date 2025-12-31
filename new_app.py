import dash
from dash import html, dcc, Dash, Input, Output
import pandas as pd
import plotly.express as px

# Load processed data
df = pd.read_csv("data/formatted_output.csv")
df['Date'] = pd.to_datetime(df['Date']).dt.date
df.sort_values('Date', inplace=True)

# Define regions
regions = ['north', 'east', 'south', 'west', 'all']

# Initialize the app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    style={'backgroundColor': '#DCD0E5', 'padding': '40px', 'fontFamily': 'Arial, sans-serif'},
    children=[
        html.H1(
            "Pink Morsel Sales Visualizer",
            style={'textAlign': 'center', 'color': '#4B0082', 'marginBottom': '40px'}
        ),
        html.Div([
            html.Label("Select Region:", style={'color': '#4B0082', 'fontWeight': 'bold', 'fontSize': '18px'}),
            dcc.RadioItems(
                id='region-radio',
                options=[{'label': r.capitalize(), 'value': r} for r in regions],
                value='all',
                inline=True,
                labelStyle={'marginRight': '20px', 'color': '#4B0082', 'fontWeight': 'bold'}
            )
        ], style={'marginBottom': '30px'}),
        dcc.Graph(
            id='sales-line-chart',
            style={'border': '2px solid #4B0082', 'borderRadius': '10px', 'padding': '10px', 'backgroundColor': 'white'}
        )
    ]
)

# Callback
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['Region'].str.lower() == selected_region.lower()]

    grouped = filtered_df.groupby('Date', as_index=False)['Sales'].sum()

    fig = px.line(
        grouped,
        x='Date',
        y='Sales',
        title=f'Daily Pink Morsel Sales - {selected_region.capitalize()}',
        labels={'Sales': 'Total Sales', 'Date': 'Date'}
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='#E6E6FA',
        font_color='#4B0082',
        title_font_size=22,
        xaxis=dict(showgrid=True, gridcolor='#D3D3D3'),
        yaxis=dict(showgrid=True, gridcolor='#D3D3D3')
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)