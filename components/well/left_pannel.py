import dash
from dash import html, dcc

from controls import WELLS

well_selection = html.Div(
    [
        html.Div(
        [
            html.P("Filter by well type:", className="control_name_label", id="stat_text"),
            dcc.Dropdown(
                id="typeSelect",
                options=['Production', 'Exploration'],
                value="Production",
                multi=False,
                className="dcc_control",
            ),
        ],
        id="cross-filter-options",
        style={"width": "50%"},
        ),
        html.Div(
        [
            html.P("Filter by well name:", className="control_name_label", id="stat_text"),
            dcc.Dropdown(
                id="wellSelect",
                options=WELLS['Production'],
                value="2X",
                multi=False,
                className="dcc_control",
            ),
        ],
        id="cross-filter-options",
        style={"width": "50%"},
        ),
    ],
    id="cross-filter-options",
    style={"display": "flex", "flex-direction": "row"},
)

mapbox_map = html.Div(
    [
        dcc.Graph(
            id="mapbox-graph",
            config={"displayModeBar": False},
            style={
                "width": "100%",
                # "height": "100vh", 
            },
        ),
    ],
)