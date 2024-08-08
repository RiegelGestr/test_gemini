import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import request
import numpy as np
import datetime
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# Data Trips Users
df = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=100, freq='W'),
    'Kinto': [x + np.random.randint(-10, 10) for x in range(100, 200)],
    'Dott': [x + np.random.randint(-10, 10) for x in range(200, 300)],
    'Green Mobility': [x + np.random.randint(-3, 4) for x in range(10, 110)],
    'Users Kinto': [x + np.random.randint(-10, 10) for x in range(10, 110)],
    'Users Dott': [x + np.random.randint(-10, 10) for x in range(10, 110)],
    'Users Green Mobility': [x + np.random.randint(-3, 4) for x in range(10, 110)],
    'Distance Kinto': [x + np.random.randint(-10, 10) for x in range(100, 200)],
    'Distance Dott': [x + np.random.randint(-10, 10) for x in range(200, 300)],
    'Distance Green Mobility': [x + np.random.randint(-3, 4) for x in range(10, 110)],
    'Vehicles Kinto': [x + np.random.randint(-10, 10) for x in range(100, 200)],
    'Vehicles Dott': [x + np.random.randint(-10, 10) for x in range(200, 300)],
    'Vehicles Green Mobility': [x + np.random.randint(-3, 4) for x in range(10, 110)],
})
# Data Customer Satisfaction
df_customer = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=100, freq='W'),
    'Kinto_Good': np.random.randint(50, 150, size=100),
    'Kinto_Super': np.random.randint(10, 50, size=100),
    'Kinto_Bad': np.random.randint(0, 30, size=100),
    'Dott_Good': np.random.randint(50, 150, size=100),
    'Dott_Super': np.random.randint(10, 50, size=100),
    'Dott_Bad': np.random.randint(0, 30, size=100),
    'Green Mobility_Good': np.random.randint(50, 150, size=100),
    'Green Mobility_Super': np.random.randint(10, 50, size=100),
    'Green Mobility_Bad': np.random.randint(0, 30, size=100),
})
df_customer.set_index('Date', inplace=True)
# Data Share Points
df_punti = pd.DataFrame({
    'id': [1, 2, 3, 1, 2, 3, 1, 2, 3],
    'lat': [55.7681, 55.7828646, 55.8151363, 55.7681, 55.7828646, 55.8151363, 55.7681, 55.7828646, 55.8151363],
    'lon': [12.500, 12.5102707, 12.5314814, 12.500, 12.5102707, 12.5314814, 12.500, 12.5102707, 12.5314814],
    'Share Mode': ["Kinto", "Kinto", "Kinto", "Dott", "Dott", "Dott", "Green Mobility", "Green Mobility", "Green Mobility"],
    "Vehicles": [10, 5, 30, 20, 50, 60, 1000, 2000, 3000],
})
df_punti["Text"] = df_punti["Share Mode"] + " " + df_punti["Vehicles"].astype(str)
def concat_with_prefix(group):
    prefixed_strings = ["Providers " + s for s in group]
    return '\n '.join(prefixed_strings)
# Heatmaps
'''heatmap_data = pd.DataFrame({
    'lat': np.random.uniform(55.7, 55.9, size=1000),  # Esempio di coordinate casuali
    'lon': np.random.uniform(12.4, 12.6, size=1000),  # Esempio di coordinate casuali
    'Utilizzo': np.random.randint(1, 100, size=1000)  # Esempio di dati casuali di utilizzo
})
'''
df_distance = pd.DataFrame({
    'distance': [np.random.randint(10,1000) for x in range(100*3)],
    'shared_provider':[np.random.choice(["Kinto","Dott","Green Mobility"]) for x in range(100*3)]
})
#
hubs = ['Hub A', 'Hub B']
vehicle_types = ["Green Mobility","Dott","Kinto"]
percentages = {
    'Hub A': {'Kinto': 40, 'Green Mobility': 30, 'Dott': 30},
    'Hub B': {'Kinto': 25, 'Green Mobility': 50, 'Dott': 25},
}
data = pd.DataFrame({
    'Hub': ['Hub 1', 'Hub 2'],
    'Dott': [220, 180],
    'Kinto': [250, 210],
    'Green Mobility': [270, 230]
})
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
color_map = {
    'Green Mobility': '#2a9d8f',
    'Kinto': '#1d3557',
    'Dott': '#f4a261',
}
# Creazione dell'app Dash
app = dash.Dash(external_stylesheets=[dbc.themes.MORPH],suppress_callback_exceptions=True)
server = app.server
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# Overlay per l'animazione di entrata
intro_overlay = html.Div(
    id='intro-overlay',
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1("GEMINI", 
                                style={'color': '#90bd1f', 'fontSize': '96px', 'fontFamily': 'Courier New, monospace'}
                        ),
                        html.P("GREENING EUROPEAN MOBILITY", 
                               style={'color': '#DEE0E3', 'fontSize': '48px', 'fontFamily': 'Courier New, monospace','marginBottom': '-2px'}
                        ),
                        html.P("THROUGH CASCADING INNOVATION INITIATIVES", 
                               style={'color': '#DEE0E3', 'fontSize': '36px', 'fontFamily': 'Courier New, monospace'}
                        ),
                        html.P([
                            "Copenhagen Living Labs: ",
                            html.Span("DTU", style={'color': '#850002', 'fontFamily': 'Courier New, monospace'}),
                            " x ",
                            html.Span("Rudersdal Kommune", style={'color': '#0D3077', 'fontFamily': 'Courier New, monospace'}),
                            ],
                            style={'color': '#DEE0E3', 'fontSize': '24px', 'fontFamily': 'Courier New, monospace'}
                        )
                    ],
                    style={'textAlign': 'left', 'marginLeft': '18px'}
                ),
                html.Div(
                    children=[
                        html.Img(src='/assets/logo.png', style={'width': '550px', 'margin-bottom': '20px'})
                    ],
                    style={'textAlign': 'center', 'flex': '1'}
                )
            ],
            style={
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'width': '100%',
                'height': '100%',
                'backgroundColor': 'rgba(23, 18, 21, 0.67)',
                'color': 'white',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center',
                'padding': '20px',
                'transition': 'opacity 1s ease-in-out',
                'opacity': 1.0,
                'zIndex': 9999,
            }
        )
    ]
)
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
jumbotron = html.Div(
    dbc.Container(
        [
            dbc.Row([
                    dbc.Col(
                        html.Img(src="assets/logo_t.png", style={'width': '50%', 'height': '100%'}),
                    ),
                    dbc.Col(
                        html.H1("Copenhagen Living Labs", 
                                style={
                                    'font-family': 'Courier New, monospace',
                                    'font-size': '48px',
                                    'color': '#151829',
                                    'text-align': 'right'
                                }
                        ),
                    ),
                ],
                align="center"
            ),
            html.Br(),
            html.P([
                "Before the GEMINI Living Lab, Rudersdal, near Copenhagen, faced significant transportation challenges.",
                html.Br(),
                "High car usage led to increased CO2 emissions, noise, congestion, and isolation for those without private vehicles. ",
                html.Br(),
                "The GEMINI Living Lab aims to tackle these issues by promoting sustainable transport.",
                html.Br(),
                "Key objectives include supporting local climate goals, increasing shared mobility, reducing car use and CO2 emissions, and improving urban safety and accessibility.",
                html.Br(),
                "The project has established six multimodal mobility hubs offering e-scooters, e-bikes, and car-sharing options.",
                html.Br(),
                "These hubs enhance public transport access and reduce the need for private car ownership.",
                html.Br(),
                "This dashboard provides updates on the lab progress, accessible to both citizens and policymakers, showcasing how these initiatives drive sustainable and connected community development."
                ],
                style = {'font-family': 'Courier New, monospace','color': '#293051'}
            ),
            html.P(
                dbc.Button("Learn more about GEMINI", 
                           color="primary",
                           href="https://www.geminiproject.eu"
                           ),
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3",
)
jumbo2 = html.Div(
    dbc.Container(
        [
            html.Hr(className="my-2"),
            html.P(
                [
                    "Technical University of Denmark, in collaboration with Rudersdal Municipality and shared mobility partners such as Dott, Green Mobility, and Kinto, is running and analyzing this pilot as part of the GEMINI project. This project has received funding from the European Union’s Horizon Innovation Actions programme under Grant agreement No. 10110380. The sole responsibility for the content of this website lies with the authors. It does not necessarily reflect the opinion of the European Union. Neither the Agency nor the European Commission are responsible for any use that may be made of the information contained therein. ",
                    html.Br(),
                    "The group is led by Professor Laura Alessandretti. ",
                    html.A("Learn more about her research.", href="http://laura.alessandretti.com", target="_blank", style={'color': '#6C7983'}),
                ],
                style={'font-family': 'Courier New, monospace', 'color': '#293051'}
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3",
)
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
def data_weekly(header, list_df):
    df0 = list_df[0].copy()
    today = datetime.datetime.now()
    nearest_row = df0.iloc[(df0['Date'] - today).abs().argsort()[:1]]
    x = nearest_row[header].iloc[0]
    y = nearest_row["Users "+header].iloc[0]
    z = nearest_row["Vehicles "+header].iloc[0]
    df1 = list_df[1].copy()
    avg_distance = np.mean(df1[df1["shared_provider"] == header]["distance"])
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
            [
               dcc.Markdown( dangerously_allow_html = True,
                   children = ["Number of Trips {0} <br><sub> Number of Users {1} <br><sub> Number of Vehicles {2} <br><sub>Average distance {3}".format(
                       str(x),str(y),str(z),str(round(avg_distance)))])
                ]

            )
        ]

    return card_content
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# Corpo principale dell'app
today = datetime.datetime.now()
body_app = dbc.Container(
    [
        html.Hr(className="my-2"),
        html.H1("Weekly Summary "+today.strftime("%d/%m/%Y"), style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px',"color":"#151829"}),
        dbc.Row([
        dbc.Col(dbc.Card(data_weekly("Kinto",[df,df_distance]), color = '#1d3557',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_weekly("Green Mobility",[df,df_distance]), color = '#2a9d8f',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'}),
        dbc.Col(dbc.Card(data_weekly("Dott",[df,df_distance]), color = '#f4a261',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 4, xl = 4, style = {'padding':'12px 12px 12px 12px'})
        ]),
        html.Br(),
        #
        dbc.Tabs(
            [
                dbc.Tab(label="Trips", tab_id="trip_graph"),
                dbc.Tab(label="Users", tab_id="users_graph"),
                dbc.Tab(label="Vehicles", tab_id="vehicles_graph"),
                dbc.Tab(label="Trip Distance", tab_id="trip_distance"),
                dbc.Tab(label="Hubs Map", tab_id="hub_map"),
                dbc.Tab(label="Enable Rate", tab_id = "enable_rate"),
                dbc.Tab(label="Customer Satisfaction", tab_id = "satisfaction")
            ],
            id="tabs",
            active_tab="trip_graph",
        ),
        html.Div(id="tab-content"),
        ########################################################################
        #
        html.Br(),
        #
        dcc.Interval(
            id='interval-component',
            interval=3*1000,  # in milliseconds
            n_intervals=0
        ),
        #
        html.Br(),
        #
    ], fluid=True
)
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
# Layout dell'app
app.layout = html.Div(id='parent', children=[intro_overlay, jumbotron, body_app, jumbo2])

# Callback per nascondere l'overlay dopo 0.5 secondi
@app.callback(
    Output('interval-component', 'interval'),
    [Input('intro-overlay', 'style')]
)
def update_intro_interval(style):
    if style['display'] == 'none':
        return 60*1000  # Ritorna l'intervallo originale per la heatmap
    else:
        return 3*1000  # Intervallo più breve per l'overlay introduttivo
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab == "trip_graph":
        return dbc.Row([
        html.H1("Number of Trips per Week", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
        dbc.Col([
            dcc.Dropdown(
                id='trip-dropdown',
                options=[
                    {'label': 'Green Mobility', 'value': 'Green Mobility'},
                    {'label': 'Kinto', 'value': 'Kinto'},
                    {'label': 'Dott', 'value': 'Dott'}
                ],
                placeholder="Filter by Shared Mobility Provider(s)",
                value='trips'
            ),
            dcc.Graph(id='trip-graph'),
        ], width=8),
        dbc.Col([
            html.H3("Weekly Trip Trends", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
            html.P("This plot shows the weekly count of trips made using the selected shared mobility service from the dropdown menu. Use the slider to select a specific week and view the number of trips for that period. This metric helps track how usage trends change over time and provides insights into the popularity of different services. Current week data is displayed in the card above."),
        ], width=4)
    ], ),
    elif active_tab == "users_graph":
        return dbc.Row([
            html.H1("New User Growth Over Time", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
            dbc.Col([
                dcc.Dropdown(
                    id='utenti-dropdown',
                    options=[
                        {'label': 'Green Mobility', 'value': 'Green Mobility'},
                        {'label': 'Kinto', 'value': 'Kinto'},
                        {'label': 'Dott', 'value': 'Dott'}
                    ],
                    placeholder="Filter by Shared Mobility Provider(s)",
                    value='utenti_auto'
                ),
                dcc.Graph(id='utenti-graph'),
            ], width = 8),
        dbc.Col([
            html.H3("What is this graph?", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
            html.P("This plot displays the number of new users registering for the chosen shared mobility service each week. Select a week using the slider to see how new user acquisition varies over time. This helps assess the growth and appeal of each service, revealing trends in user adoption and service expansion. The data for the current week is shown in the card above."),
        ], width=4)
        ],),
    elif active_tab == "vehicles_graph":
        return dbc.Row([
            html.H1("Fleet Size Dynamics", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
            dbc.Col([
                dcc.Dropdown(
                    id='vehicles-dropdown',
                    options=[
                        {'label': 'Green Mobility', 'value': 'Green Mobility'},
                        {'label': 'Kinto', 'value': 'Kinto'},
                        {'label': 'Dott', 'value': 'Dott'}
                    ],
                    placeholder="Filter by Shared Mobility Provider(s)",
                    value='vehicles_auto'
                ),
                dcc.Graph(id='vehicles-graph'),
            ], width = 8),
            dbc.Col([
                html.H3("What is this graph?", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
                html.P("This plot illustrates the weekly count of vehicles available for the selected shared mobility service. By adjusting the slider, you can see how fleet size changes over different weeks. This metric provides insights into how well the fleet aligns with user demand and the service provider's capacity to scale. The number of vehicles for the current week is available in the card above."),
            ], width=4)
        ],),
    elif active_tab == "trip_distance":
        return dbc.Row([
                html.H1("Trip Distance Distribution", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
                dbc.Col([
                    dcc.Dropdown(
                        id='distance-dropdown',
                        options=[
                            {'label': 'Green Mobility', 'value': 'Green Mobility'},
                            {'label': 'Kinto', 'value': 'Kinto'},
                            {'label': 'Dott', 'value': 'Dott'}
                        ],
                        placeholder="Filter by Shared Mobility Provider(s)",
                        value='utenti_auto'
                    ),
                    dbc.Col(dcc.Graph(id='distance-histogram')),
                    dbc.Col(dcc.Graph(id='distance-timeseries')),
                ], width = 8),
                dbc.Col([
                    html.H3("Trip Distance Insights?", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
                    html.P("This section features two plots for the selected shared mobility service. The upper plot is a boxplot showing the distribution of distances traveled within the selected week, compared to all services. The lower plot is a time series of average distances traveled over time. Use the slider to view how distance patterns evolve for the chosen service, offering insights into user behavior and trip length trends. The current week's average distance information is summarized in the card above."),
                ], width=4)
            ],),
    elif active_tab == "hub_map":
        return dbc.Row([
            html.H1("Hubs Location", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
            dbc.Col(dcc.Graph(id='mappa-interattiva',style={'height': '80vh', 'width': '100%'}), width = 12),
        ],),
    elif active_tab == "enable_rate":
        return dbc.Row([
            html.H1("Enable Rate Indicators", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
            dbc.Col(dcc.Graph(id='enable-rate-indicator', figure=generate_indicators()), width=8),
            dbc.Col([
                    html.H3("Enable Rate Insights?", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
                    html.P("This section presents a grid of indicators for each hub and sharing mobility provider, detailing the enable rate of vehicles. The enable rate represents the percentage of vehicles that are charged and ready for use, with values ranging from 0 to 100. The grid displays the enable rates for three different hubs and three sharing mobility providers, allowing you to assess the availability of vehicles across various locations. For detailed hub locations, refer to the 'Hubs Map' tab, where you can access the map of Copenhagen with hubs locations.")
                ], width=4)
        ])
    elif active_tab == "satisfaction":
        return dbc.Row([
            html.H1("Customer Satisfaction", style={'fontFamily': 'Courier New, monospace', 'fontSize': '32px'}),
            dbc.Col([
                dcc.Dropdown(
                    id='satisfaction-dropdown',
                    options=[
                        {'label': 'Green Mobility', 'value': 'Green Mobility'},
                        {'label': 'Kinto', 'value': 'Kinto'},
                        {'label': 'Dott', 'value': 'Dott'}
                    ],
                    placeholder="Filter by Shared Mobility Provider(s)",
                    value='vehicles_auto'
                ),
                dcc.Graph(id='satisfaction-graph'),
            ], width = 8),
            dbc.Col([
                    html.H3("Customer Satisfaction Insights?", style={'fontFamily': 'Courier New, monospace', 'fontSize': '24px'}),
                    html.P("This section displays a stacked bar chart illustrating customer satisfaction over time for the selected shared mobility provider. The chart shows the number of trips with satisfaction ratings, segmented into 'Super' (green), 'Good' (blue) and 'Bad' (red) categories. Use the dropdown menu to select different providers and observe how satisfaction levels and trends change over time. This visualization helps you understand customer feedback patterns and the overall service quality for each provider.")
                ], width=4)
        ])

########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
@app.callback(
    Output('trip-graph', 'figure'),
    [Input('trip-dropdown', 'value')]
)
def update_veicoli_graph(selected_veicolo):
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[selected_veicolo], mode='lines+markers', line_color=color_map[selected_veicolo]))
    for x in ["Dott", "Kinto", "Green Mobility"]:
        if x == selected_veicolo:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x], mode='lines', line=dict(color="grey")))
    fig.update_layout(
        title = "Number of Trips: " + selected_veicolo
    )
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
########################################################################
########################################################################
@app.callback(
    Output('utenti-graph', 'figure'),
    [Input('utenti-dropdown', 'value')]
)
def update_utenti_graph(selected_utente):
    filter = "Users " + selected_utente
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[filter], mode='lines+markers', line_color=color_map[selected_utente], marker_symbol='diamond'))
    for x in ["Users Dott", "Users Kinto", "Users Green Mobility"]:
        if x == filter:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x], mode='lines', line=dict(color="grey")))
    fig.update_layout(
        title = "Number of New Users: " + selected_utente
    )
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
########################################################################
########################################################################
@app.callback(
    Output('vehicles-graph', 'figure'),
    [Input('vehicles-dropdown', 'value')]
)
def update_vehicles_graph(selected_utente):
    filter = "Vehicles " + selected_utente
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[filter], mode='lines+markers', line_color=color_map[selected_utente], marker_symbol='diamond'))
    for x in ["Vehicles Dott", "Vehicles Kinto", "Vehicles Green Mobility"]:
        if x == filter:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x], mode='lines', line=dict(color="grey")))
    fig.update_layout(
        title = "Number of Vehicles: " + selected_utente
    )
    fig.update(layout_showlegend=False)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Vehicles",
        font=dict(
            family="Courier New, monospace",
            size=18,
        )
    )
    return fig
########################################################################
########################################################################
@app.callback(
    Output('mappa-interattiva', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_mappa_interattiva(n):
    gdf = df_punti.groupby(by=["id"]).agg({
        "lat": "first",
        "lon": "first",
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
########################################################################
########################################################################
@app.callback(
    Output('barchart-interattiva', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_barchart(n):
    data = []
    for vt in vehicle_types:
        data.append(
            go.Bar(
                x=hubs,
                y=[percentages[hub][vt] for hub in hubs],
                name=vt,
                marker=dict(cornerradius="30%"),
                marker_color=color_map[vt]
            )
        )
    figure = go.Figure(data=data)
    figure.update_layout(
        barmode='group',
        title='Enable Rate Hubs',
        xaxis_title='Hubs',
        yaxis_title='Percentage',
    )
    return figure

########################################################################
########################################################################
@app.callback(
    [Output('distance-histogram', 'figure'),
     Output('distance-timeseries', 'figure')],
    [Input('distance-dropdown', 'value')]
)
def update_distance(selected_distance):
    # Crea un istogramma
    fig1 = go.Figure(data=go.Box(x=df_distance[df_distance["shared_provider"] == selected_distance]["distance"],name = selected_distance, marker=dict(color = color_map[selected_distance])))
    fig1.add_trace(go.Box(x=df_distance["distance"],name = "All", marker=dict(color="grey")))
    fig1.update_layout(
        title="Trip Distance Distribution: " + selected_distance,
        xaxis_title="Distance",
        font=dict(
            family="Courier New, monospace",
            size=18,
        )
    )
    fig1.update_traces(opacity=0.75)
    #
    filter = "Distance " + selected_distance
    fig = go.Figure(data=go.Scatter(x=df["Date"], y=df[filter], mode='lines+markers', line_color=color_map[selected_distance], marker_symbol='diamond'))
    for x in ["Distance Dott", "Distance Kinto", "Distance Green Mobility"]:
        if x == filter:
            continue
        fig.add_trace(go.Scatter(x=df['Date'], y=df[x], mode='lines', line=dict(color="grey")))
    fig.update_layout(
        title = "Average distance for " + selected_distance
    )
    fig.update(layout_showlegend=False)
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Distance",
        font=dict(
            family="Courier New, monospace",
            size=18,
        )
    )
    return fig1,fig
########################################################################
########################################################################
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
########################################################################
########################################################################
def create_indicator(value, title_text, row, col,color):
    return go.Indicator(
        mode="number+gauge",
        value=value,
        domain={
            'x': [col * 0.33 + 0.05, col * 0.33 + 0.30],
            'y': [1 - (row + 1) * 0.30, 1 - row * 0.30]
        },
        title={'text': title_text},
        gauge=dict(
            axis=dict(range=[0, 100]),  # Set the range of the gauge
            bar=dict(color=color)
        )
    )

def generate_indicators():
    fig = go.Figure()
    # Add indicators for each hub and provider
    fig.add_trace(create_indicator(80, "Dott", 0, 0, color_map["Dott"]))
    fig.add_trace(create_indicator(50, "Kinto", 0, 1,color_map["Kinto"]))
    fig.add_trace(create_indicator(70, "Green Mobility", 0, 2,color_map["Green Mobility"]))
    #
    fig.add_trace(create_indicator(99, "Dott", 1, 0,color_map["Dott"]))
    fig.add_trace(create_indicator(80, "Kinto", 1, 1,color_map["Kinto"]))
    fig.add_trace(create_indicator(80, "Green Mobility", 1, 2,color_map["Green Mobility"]))
    #
    fig.add_trace(create_indicator(40, "Dott", 2, 0,color_map["Dott"]))
    fig.add_trace(create_indicator(55, "Kinto", 2, 1,color_map["Kinto"]))
    fig.add_trace(create_indicator(70, "Green Mobility", 2, 2,color_map["Green Mobility"]))
    #
    fig.update_layout(
        grid={'rows': 3, 'columns': 3, 'pattern': "independent"},  # Updated grid to 3 rows
        template={'data': {'indicator': [{
            'title': {'text': "Enable Rate"},
            'mode': "number+delta+gauge",
           }]}
        },
        height=900,  # Adjust height as needed for 3 rows
        width=900,   # Adjust width as needed
        margin=dict(t=50, b=50, l=50, r=50),  # Add margins for spacing
        annotations=[
            dict(
                x=0.5,
                y=1.05,
                text="Hub 1",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(family="Courier New, monospace", size=24, color="black", weight="bold"),
                align="center"
            ),
            dict(
                x=0.5,
                y=0.75,
                text="Hub 2",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(family="Courier New, monospace", size=24, color="black", weight="bold"),
                align="center"
            ),
            dict(
                x=0.5,
                y=0.45,
                text="Hub 3",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(family="Courier New, monospace", size=24, color="black", weight="bold"),
                align="center"
            )
        ]
    )
    return fig
########################################################################
########################################################################
@app.callback(
    Output('satisfaction-graph', 'figure'),
    Input('satisfaction-dropdown', 'value')
)
def update_graph(selected_provider):
    # Generate figure based on selected provider
    fig = go.Figure()
    dict_color = {
        "Good":"blue",
        "Super":"green",
        "Bad":"red"
    }
    # Create traces for the selected provider
    for category in ['Good', 'Super', 'Bad']:
        fig.add_trace(go.Bar(
            x=df_customer.index,
            y=df_customer[f'{selected_provider}_{category}'],
            name=f'{category}',
            marker_color = dict_color[category]
        ))

    # Update layout for the stacked bar chart
    fig.update_layout(
        barmode='stack',
        title=f'Customer Satisfaction for {selected_provider} Over Time',
        xaxis_title='Date',
        yaxis_title='Number of Trips',
        xaxis=dict(type='date'),
    )
    
    return fig


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
@app.callback(
    Output('intro-overlay', 'style'),
    [Input('interval-component', 'n_intervals')]
)
def hide_overlay(n_intervals):
    if n_intervals > 0:
        return {'display': 'none'}
    return {
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'width': '100%',
        'height': '100%',
        'backgroundColor': 'black',
        'color': 'white',
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'zIndex': '9999'
    }
#
if __name__ == '__main__':
    app.run_server(debug=True)
