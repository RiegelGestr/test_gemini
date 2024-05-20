import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import request
import numpy as np
import os

df = pd.DataFrame({
    'Date': pd.date_range(start='2021-01-01', periods=100, freq='W'),
    'Kinto':[x + np.random.randint(-10, 10) for x in range(100, 200)],
    'Tier':[x + np.random.randint(-10, 10) for x in range(200, 300)],
    'Green Mobility':[x + np.random.randint(-3, 4) for x in range(10, 110)],
    'Utenti Kinto':[x + np.random.randint(-10, 10) for x in range(10, 110)],
    'Utenti Tier':[x + np.random.randint(-10, 10) for x in range(10, 110)],
    'Utenti Green Mobility':[x + np.random.randint(-3, 4) for x in range(10, 110)]
})

df_punti = pd.DataFrame({
    'id':[1,2,3,1,2,3,1,2,3],
    'lat': [55.7681, 55.7828646,55.8151363, 55.7681, 55.7828646,55.8151363, 55.7681, 55.7828646,55.8151363],
    'lon': [12.500, 12.5102707, 12.5314814, 12.500, 12.5102707, 12.5314814, 12.500, 12.5102707, 12.5314814],
    'Share Mode':["Kinto","Kinto","Kinto","Tier","Tier","Tier","Green Mobility","Green Mobility","Green Mobility"],
    "Vehicles":[10,5,30,20,50,60,1000,2000,3000],
})
df_punti["Text"] = df_punti["Share Mode"] + " " + df_punti["Vehicles"].astype(str)
def concat_with_prefix(group):
    prefixed_strings = ["Providers " + s for s in group]
    return '\n '.join(prefixed_strings)

heatmap_data = pd.DataFrame({
    'lat': np.random.uniform(55.7, 55.9, size=1000),  # Esempio di coordinate casuali
    'lon': np.random.uniform(12.4, 12.6, size=1000),  # Esempio di coordinate casuali
    'Utilizzo': np.random.randint(1, 100, size=1000)  # Esempio di dati casuali di utilizzo
})


# Definizione dei colori per ogni tipo di veicolo e utente
color_map = {
    'Green Mobility': 'green',
    'Kinto': 'blue',
    'Tier': 'orange',
    'Utenti Green Mobility': 'green',
    'Utenti Kinto': 'blue',
    'Utenti Tier': 'orange',
}

# Creazione dell'app Dash
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    #
    html.Div([
        html.H1("Number of Trips per Week", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
        dcc.Dropdown(
            id='veicolo-dropdown',
            options=[
                {'label': 'Green Mobility', 'value': 'Green Mobility'},
                {'label': 'Kinto', 'value': 'Kinto'},
                {'label': 'Tier', 'value': 'Tier'}
            ],
            value='auto'
        ),
        dcc.Graph(id='veicoli-graph'),
    ], style={'width': '48%', 'display': 'inline-block'}),
    #
    html.Div([
        html.H1("Number of Users per Week", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
        dcc.Dropdown(
            id='utenti-dropdown',
            options=[
                {'label': 'Utenti Green Mobility', 'value': 'Utenti Green Mobility'},
                {'label': 'Utenti Kinto', 'value': 'Utenti Kinto'},
                {'label': 'Utenti Tier', 'value': 'Utenti Tier'}
            ],
            value='utenti_auto'
        ),
        dcc.Graph(id='utenti-graph'),
    ], style={'width': '48%', 'display': 'inline-block'}),
    #
    html.Div([
        html.H1("Enable Rate", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
        dcc.Graph(id='mappa-interattiva'),
    ],style={'width': '48%', 'display': 'inline-block'}),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div([
    html.H1("Trips Heatmap", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
    dcc.Graph(id='heatmap-graph')
    ], style={'width': '48%', 'display': 'inline-block'}),
    #
    html.Div([
        html.Button("Stop Server", id="stop-button")
    ])
])

@app.callback(
    Output('veicoli-graph', 'figure'),
    [Input('veicolo-dropdown', 'value')]
)
def update_veicoli_graph(selected_veicolo):
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[selected_veicolo],mode='lines+markers', line_color=color_map[selected_veicolo]))
    for x in ["Tier","Kinto","Green Mobility"]:
        if x == selected_veicolo:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x],mode='lines', line=dict(color="grey")))
    fig.update(layout_showlegend=False)
    fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Trips",
    font=dict(
        family="Courier New, monospace",
        size=18,
    )
    )
    return fig

@app.callback(
    Output('utenti-graph', 'figure'),
    [Input('utenti-dropdown', 'value')]
)
def update_utenti_graph(selected_utente):
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[selected_utente],mode='lines+markers', line_color=color_map[selected_utente],marker_symbol='diamond'))
    for x in ["Utenti Tier","Utenti Kinto","Utenti Green Mobility"]:
        if x == selected_utente:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x],mode='lines', line=dict(color="grey")))
    fig.update(layout_showlegend=False)
    fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Users",
    font=dict(
        family="Courier New, monospace",
        size=18,
    )
    )
    return fig

@app.callback(
    Output('mappa-interattiva', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_mappa_interattiva(n):
    gdf = df_punti.groupby(by = ["id"]).agg({
        "lat":"first",
        "lon":"first",
        "Text": concat_with_prefix
    }).reset_index()    
    # Imposta la dimensione dei marker in base al numero di veicoli
    sizes = 30
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=gdf['lat'],
        lon=gdf['lon'],
        mode='markers',
        marker=dict(
            size=sizes,
            color='blue',
            opacity=0.7,
        ),
        text=gdf["Text"],
    ))
    # Imposta il layout della mappa
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            zoom=11,
            center=dict(lat=df_punti['lat'].mean(), lon=df_punti['lon'].mean())
        )
    )

    return fig

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_heatmap(n):
    fig = go.Figure(go.Densitymapbox(lat=heatmap_data['lat'], lon=heatmap_data['lon'], z=heatmap_data['Utilizzo'], radius=30))
    fig.update_layout(mapbox_style="open-street-map",mapbox=dict(
            zoom=11,
            center=dict(lat=df_punti['lat'].mean(), lon=df_punti['lon'].mean())
        ))
    return fig

@app.callback(
    Output('stop-button', 'children'),
    [Input('stop-button', 'n_clicks')]
)
def stop_server(n_clicks):
    if n_clicks:
        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()
        return "Server fermato"
    return "Stop Server"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, port=port, host='0.0.0.0')
