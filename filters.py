import dash
from dash import html, dcc

from controls import WELLS
well_filter = [
                html.Div(
                    [
                        html.P(
                            "Filter by operation date:",
                            className="control_label",
                        ),
                        dcc.RangeSlider(
                            id="year_slider",
                            min=2019,
                            max=2025,
                            marks={i: "{}".format(i) for i in range(2019, 2025+1)},
                            step=1,
                            value=[2019, 2025],
                            className="dcc_control",
                        ),
                        html.P("Filter by well name:", className="control_name_label"),
                        dcc.Dropdown(
                            id="wellSelect",
                            options=WELLS["Exploration"],
                            value="2X",
                            multi=False,
                            className="dcc_control",
                        ),
                        html.P("Filter by well type:", className="control_type_label"),
                        dcc.Dropdown(
                            id="well_type",
                            options=["Production", "Exploration"],
                            value="Exploration",
                            multi=False,
                            className="dcc_control",
                        ),
                    ],
                    className="pretty_container three columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="wellText"), html.P("Well Name")],
                                    id="well",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText"), html.P("Gas")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText"), html.P("Oil")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Water")],
                                    id="water",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilRate"), html.P("Oil Rate")],
                                    id="oilR",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasRate"), html.P("Gas Rate")],
                                    id="gasR",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="ten columns",
                ),
            ]