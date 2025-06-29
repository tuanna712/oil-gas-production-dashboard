import plotly.graph_objects as go
from dash import html, dcc, Input, Output, State, ClientsideFunction, callback

percentage_style={
    'display': 'flex',         # Enables flexbox for row alignment
    'flex-direction': 'row',   # Arranges items in a row
    'align-items': 'center',   # Vertically centers the items in the row
    'justify-content': 'space-between', # Pushes items to ends with space between
    'width': '80%',          # Adjust width as needed
}

well_statistics = html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(id="last_month_text", children="Placeholder", style={"font-size": "16px", "font-weight": "bold", "color": "#169046", 'text-align': 'center'},),
                                        html.H6(id="wellName", style={'color':'#169046', 'text-align': 'center'}), html.P("Well Name", style={'color':'#169046', 'text-align': 'center'}, id="stat_text"),
                                        html.Div(
                                            [
                                                html.H6(id="dayOn"),
                                                html.H6(id="dayOnChange"),
                                            ], style=percentage_style,
                                        ),
                                        html.P("Operated Days (Current Month)", id="stat_text"),
                                    ],
                                    id="well",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H6(id="gasMonth"), 
                                                html.H6(id="gasChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P(["Gas (km",html.Sup("3"),"/month)"], id="stat_text"),
                                        html.Div(
                                            [
                                                html.H6(id="gasRate"), 
                                                html.H6(id="gasRChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P(["Rate of Gas (km",html.Sup("3"),"/month)"], id="stat_text"),
                                     ],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H6(id="oilMonth"), 
                                                html.H6(id="oilChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P("Oil (tons/month)", id="stat_text"),
                                        html.Div(
                                            [
                                                html.H6(id="oilRate"), 
                                                html.H6(id="oilRChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P("Oil Rate (tons/day)", id="stat_text")
                                     ],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H6(id="waterMonth"), 
                                                html.H6(id="waterChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P(["Water (m",html.Sup("3"),"/month)"], id="stat_text"),
                                        html.Div(
                                            [
                                                html.H6(id="waterRate"), 
                                                html.H6(id="waterRChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P(["Water Rate (m",html.Sup("3"),"/month)"], id="stat_text")
                                    ],
                                    id="water",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.H6(id="GOR"), 
                                                html.H6(id="GORChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P(["GOR (m",html.Sup("3"),"/ton)"], id="stat_text"),
                                        html.Div(
                                            [
                                                html.H6(id="WCT"), 
                                                html.H6(id="WCTChange")
                                            ], style=percentage_style,
                                        ),
                                        html.P("WCT (%)", id="stat_text")
                                    ],
                                    id="wct",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                    ],
                )


right_charts = html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="well-graph-1",
                            config={"displayModeBar": False},
                            className="chart-item", # Apply a class for consistent sizing
                        ),
                        dcc.Graph(
                            id="well-graph-2",
                            config={"displayModeBar": False},
                            className="chart-item",
                        ),
                    ],
                    className="chart-pair-container", # Container for 1 and 2
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="well-graph-3",
                            config={"displayModeBar": False},
                            className="chart-item",
                        ),
                        dcc.Graph(
                            id="well-graph-4",
                            config={"displayModeBar": False},
                            className="chart-item",
                        ),
                    ],
                    className="chart-pair-container", # Container for 3 and 4
                ),
            ],
            id="right-charts-panel", # Give the main right panel an ID
            style={
                "width": "100%",
                "display": "flex",
                "flex-wrap": "wrap", # Allows items to wrap to the next line if needed
                "align-content": "stretch", # Distributes space between flex lines
                "padding": "10px",
                "boxSizing": "border-box",
            },
        )

# --- DATA AND FUNCTIONS ---
from data import load_data
data = load_data()

# Initiate mapbox hover data
@callback(
    Output("mapbox-graph", "hoverData"),
    Input("wellSelect", "value"),
)
def update_mapbox_hover_data(well_name):
    """Update the hover data for the mapbox graph based on selected well."""
    if not well_name:
        return None
    
    # Find the well in the data
    well_df = data[data["WellID"] == well_name]
    if well_df.empty:
        return None
    
    # Create hover data with well information
    hover_data = {
        'points': [{
            'lat': well_df['X'].values[0],
            'lon': well_df['Y'].values[0],
            'text': f"Well: {well_name}<br>Type: {well_df['Type'].values[0]}"
        }]
    }
    return hover_data

@callback(
    Output("wellName", "children"),
    Output("dayOn", "children"),
    Output("oilMonth", "children"),
    Output("oilRate", "children"),
    Output("gasMonth", "children"),
    Output("gasRate", "children"),
    Output("waterMonth", "children"),
    Output("waterRate", "children"),
    Output("GOR", "children"),
    Output("WCT", "children"),
    Output("oilChange", "children"),
    Output("gasChange", "children"),
    Output("waterChange", "children"),
    Output("oilRChange", "children"),
    Output("gasRChange", "children"),
    Output("waterRChange", "children"),
    Output("GORChange", "children"),
    Output("WCTChange", "children"),
    Output("dayOnChange", "children"),
    Input("wellSelect", "value"),
    Input("mapbox-graph", "hoverData"),
)
def update_well_statistics(well_name, map_hover_data):
    """Update well statistics based on selected well and year."""
    
    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    well_name = _text.split("<br>")[0].split(": ")[1] if map_hover_data else well_name

    # If no well is selected, return empty statistics
    if not well_name:
        return [""] * 10
    
    well_df = data[(data["WellID"] == well_name)]
    if well_df.empty:
        return [""] * 10
    # Sort by date to get the latest data
    well_df_last = well_df.sort_values(by="Date", ascending=False).iloc[0]
    # The second latest month data
    well_df_prev = well_df.sort_values(by="Date", ascending=False).iloc[1]
    # Percentage change calculation
    def calculate_percentage_change(current, previous):
        if previous == 0:
            return "0 %"
        change = ((current) / previous) * 100
        return f"{round(change,2)} %"
    oil_change = calculate_percentage_change(well_df_last["OilMo"], well_df_prev["OilMo"])
    gas_change = calculate_percentage_change(well_df_last["GasMo"], well_df_prev["GasMo"])
    water_change = calculate_percentage_change(well_df_last["WatMo"], well_df_prev["WatMo"])
    oilR_change = calculate_percentage_change(well_df_last["OilR"], well_df_prev["OilR"])
    gasR_change = calculate_percentage_change(well_df_last["GasR"], well_df_prev["GasR"])
    waterR_change = calculate_percentage_change(well_df_last["WatR"], well_df_prev["WatR"])
    GOR_change = calculate_percentage_change(well_df_last["GOR"], well_df_prev["GOR"])
    WCT_change = calculate_percentage_change(well_df_last["WCT"], well_df_prev["WCT"])
    dayOn_change = calculate_percentage_change(well_df_last["DayOn"], well_df_prev["DayOn"])
    
    # Get data from columns: #['DayOn', 'OilMo', 'GasMo', 'WatMo', 'LiqMo', 'GOR', 'OilR', 'GasR', 'WatR', 'LiqR', 'WCT']
    return (
        well_df_last["WellID"],
        well_df_last["DayOn"],
        well_df_last["OilMo"],
        round(well_df_last["OilR"], 2),
        well_df_last["GasMo"],
        round(well_df_last["GasR"], 2),
        well_df_last["WatMo"],
        round(well_df_last["WatR"], 2),
        round(well_df_last["GOR"], 2),
        round(well_df_last["WCT"], 2),
        oil_change, gas_change, water_change, 
        oilR_change, gasR_change, waterR_change, 
        GOR_change, WCT_change, 
        dayOn_change,
    )

def get_color_style(percentage_value):
    """
    Returns a dictionary with the color style based on the percentage value.
    """
    if percentage_value is None:
        return {'color': 'black'}

    if percentage_value < 90:
        return {'color': '#c30010', 'font-weight': 'bold'}
    elif 90 <= percentage_value < 100:
        return {'color': '#1967AC', 'font-weight': 'bold'}
    else:
        return {'color': '#169046', 'font-weight': 'bold'}
    
import re
    
@callback(
    Output('oilChange', 'style'),
    Output('gasChange', 'style'),
    Output('waterChange', 'style'),
    Output('oilRChange', 'style'),
    Output('gasRChange', 'style'),
    Output('waterRChange', 'style'),
    Output('GORChange', 'style'),
    Output('WCTChange', 'style'),
    Output('dayOnChange', 'style'),
    Input('oilChange', 'children'),
    Input('gasChange', 'children'),
    Input('waterChange', 'children'),
    Input('oilRChange', 'children'),
    Input('gasRChange', 'children'),
    Input('waterRChange', 'children'),
    Input('GORChange', 'children'),
    Input('WCTChange', 'children'),
    Input('dayOnChange', 'children')
)
def update_all_styles(oil_change_children, gas_change_children, water_change_children,
                      oilR_change_children, gasR_change_children, waterR_change_children,
                      GOR_change_children, WCT_change_children, dayOn_change_children):
    
    # Helper to parse the string like "95%" to a float 95.0
    def parse_percentage_string(s):
        if s is None:
            return None
        # Use regex to find digits and an optional decimal point
        match = re.search(r'(\d+(\.\d+)?)', str(s))
        if match:
            return float(match.group(1))
        return None # Return None if parsing fails

    # Parse all input children values to numbers
    oil_change_val = parse_percentage_string(oil_change_children)
    gas_change_val = parse_percentage_string(gas_change_children)
    water_change_val = parse_percentage_string(water_change_children)
    oilR_change_val = parse_percentage_string(oilR_change_children)
    gasR_change_val = parse_percentage_string(gasR_change_children)
    waterR_change_val = parse_percentage_string(waterR_change_children)
    GOR_change_val = parse_percentage_string(GOR_change_children)
    WCT_change_val = parse_percentage_string(WCT_change_children)
    dayOn_change_val = parse_percentage_string(dayOn_change_children)

    # Apply the styling logic to each value
    oil_style = get_color_style(oil_change_val)
    gas_style = get_color_style(gas_change_val)
    water_style = get_color_style(water_change_val)
    oilR_style = get_color_style(oilR_change_val)
    gasR_style = get_color_style(gasR_change_val)
    waterR_style = get_color_style(waterR_change_val)
    GOR_style = get_color_style(GOR_change_val)
    WCT_style = get_color_style(WCT_change_val)
    dayOn_style = get_color_style(dayOn_change_val)

    # Return a tuple of styles, in the exact order of the Outputs
    return (oil_style, gas_style, water_style,
            oilR_style, gasR_style, waterR_style,
            GOR_style, WCT_style, dayOn_style)

@callback(
    Output("last_month_text", "children"),
    Input("wellSelect", "value"),
    Input("mapbox-graph", "hoverData"),
)
def update_last_month_text(wellSelect, map_hover_data):
    """Update the text for the last month based on the selected well."""

    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    wellSelect = _text.split("<br>")[0].split(": ")[1] if map_hover_data else wellSelect

    # If no well is selected, return a placeholder message
    if not wellSelect:
        return "Select a well to view last month's data."
    
    well_df = data[data["WellID"] == wellSelect]
    if well_df.empty:
        return "No data available for this well."
    
    # Get the last month from the data
    last_month = well_df["Date"].max().strftime("%B %Y")
    return f"{last_month}"

# --- CHARTS ---
@callback(
    Output("well-graph-1", "figure"),
    Input("wellSelect", "value"),
    Input("year_slider", "value"),
    Input("mapbox-graph", "hoverData"),
)
def line_chart_monthly(wellSelect, year_slider, map_hover_data):
    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    wellSelect = _text.split("<br>")[0].split(": ")[1] if map_hover_data else wellSelect

    title_text = f"{wellSelect} - Oil/Gas Production Trends"

    if not wellSelect or not year_slider or len(year_slider) != 2:
        return go.Figure()
    
    start_year, end_year = year_slider
    well_df = data[
        (data["WellID"] == wellSelect) &
        (data["year"] >= start_year) &
        (data["year"] <= end_year)
    ]

    if well_df.empty:
        return go.Figure()
    else:
        date = well_df["Date"]
        y1 = well_df["OilMo"]
        y2 = well_df["GasMo"]

    fig = go.Figure(
        data=[
            go.Scatter(
                x=date, y=y1, mode='lines', name='Oil',
                line=dict(color='#2ca02c', shape='spline', smoothing=1.1),
                yaxis='y1'
            ),
            go.Scatter(
                x=date, y=y2, mode='lines', name='Gas',
                line=dict(color='#ff7f0e', shape='spline', smoothing=1.1),
                yaxis='y2'
            ),
        ],
        layout=go.Layout(
            title=dict(
                text=title_text,
                font=dict(size=14, color='#205072'),
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                title='Oil (tons)',
                showgrid=True,
                gridcolor='#D3D3D3',
            ),
            yaxis2=dict(
                title='Gas (km3)',
                overlaying='y',
                side='right',
                showgrid=False,
            ),
            legend=dict(
                x=1,
                y=1,
                xanchor='right',
                yanchor='top'
            ),
        )
    )
    return fig

@callback(
    Output("well-graph-2", "figure"),
    Input("wellSelect", "value"),
    Input("year_slider", "value"),
    Input("mapbox-graph", "hoverData"),
)
def stacked_bar_chart_monthly(wellSelect, year_slider, map_hover_data):
    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    wellSelect = _text.split("<br>")[0].split(": ")[1] if map_hover_data else wellSelect

    title_text = f"{wellSelect} - Production Flow Rates"
    if not wellSelect or not year_slider or len(year_slider) != 2:
        return go.Figure()
    
    start_year, end_year = year_slider
    well_df = data[
        (data["WellID"] == wellSelect) &
        (data["year"] >= start_year) &
        (data["year"] <= end_year)
    ]
    if well_df.empty:
        return go.Figure()
    else:
        date = well_df["Date"]
        y1 = well_df["OilR"]
        y2 = well_df["GasR"]
        y3 = well_df["WatR"]

    fig = go.Figure(
        data=[
            go.Bar(x=date, y=y3, name='Water Rate', marker_color='#1f77b4'), 
            go.Bar(x=date, y=y2, name='Gas Rate', marker_color='#ff7f0e'),
            go.Bar(x=date, y=y1, name='Oil Rate', marker_color='#2ca02c'),
        ],
        layout=go.Layout(
            title=dict(
                text=title_text,
                font=dict(size=14, color='#205072'),
            ),
            barmode='stack',
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,  # Remove vertical gridlines
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#D3D3D3',  # Change gridline color to grey
            ),
        )
    )
    return fig

@callback(
    Output("well-graph-3", "figure"),
    Input("wellSelect", "value"),
    Input("year_slider", "value"),
    Input("mapbox-graph", "hoverData"),
)
def bar_chart_dayon(wellSelect, year_slider, map_hover_data):
    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    wellSelect = _text.split("<br>")[0].split(": ")[1] if map_hover_data else wellSelect

    title_text = f"{wellSelect} - Days On Stream (days/month)"
    if not wellSelect or not year_slider or len(year_slider) != 2:
        return go.Figure()
    
    start_year, end_year = year_slider
    well_df = data[
        (data["WellID"] == wellSelect) &
        (data["year"] >= start_year) &
        (data["year"] <= end_year)
    ]
    if well_df.empty:
        return go.Figure()
    else:
        date = well_df["Date"]
        day_on = well_df["DayOn"]

    fig = go.Figure(
        data=[
            go.Bar(x=date, y=day_on, name='Days On Stream', marker_color='#329D9C')
        ],
        layout=go.Layout(
            title=dict(
                text=title_text,
                font=dict(size=14, color='#205072'),
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#D3D3D3',
                # title='Days On Stream (d/mo)'
            ),
        )
    )
    return fig

@callback(
    Output("well-graph-4", "figure"),
    Input("wellSelect", "value"),
    Input("year_slider", "value"),
    Input("mapbox-graph", "hoverData"),
)
def stacked_line_chart(wellSelect, year_slider, map_hover_data):
    # Update well name from hover data if available
    _text = map_hover_data['points'][0]['text']
    wellSelect = _text.split("<br>")[0].split(": ")[1] if map_hover_data else wellSelect

    title_text = f"{wellSelect} - Accumulated Oil/Gas/Water Production"

    if not wellSelect or not year_slider or len(year_slider) != 2:
        return go.Figure()
    
    start_year, end_year = year_slider
    well_df = data[
        (data["WellID"] == wellSelect) &
        (data["year"] >= start_year) &
        (data["year"] <= end_year)
    ].sort_values("Date")

    if well_df.empty:
        return go.Figure()
    else:
        date = well_df["Date"]
        oil_cum = well_df["OilMo"].cumsum()
        gas_cum = well_df["GasMo"].cumsum()
        water_cum = well_df["WatMo"].cumsum()

    fig = go.Figure(
        data=[
            go.Scatter(
                x=date, y=water_cum, mode='lines', name='Water (m3)',
                stackgroup='one', line=dict(color='#1f77b4', shape='spline', smoothing=1.1)
            ),
            go.Scatter(
                x=date, y=gas_cum, mode='lines', name='Gas (km3)',
                stackgroup='one', line=dict(color='#ff7f0e', shape='spline', smoothing=1.1)
            ),
            go.Scatter(
                x=date, y=oil_cum, mode='lines', name='Oil (tons)',
                stackgroup='one', line=dict(color='#2ca02c', shape='spline', smoothing=1.1)
            ),
        ],
        layout=go.Layout(
            title=dict(
                text=title_text,
                font=dict(size=14, color='#205072'),
            ),
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#D3D3D3',
            ),
        )
    )
    return fig