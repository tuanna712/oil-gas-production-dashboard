import dash
from dash import html, dcc
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    use_pages=True,
    suppress_callback_exceptions=True,
)

app.title = "Oil & Gas Wells"
server = app.server

# App layout
app.layout = html.Div(
    [
        # Dashboard title
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo-vpi.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-left": "50px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Oil and Gas Production Monitoring",
                                    style={"margin-bottom": "0px", "color": "#205072"},
                                ),
                                html.H5(
                                    "Production Overview", style={"margin-top": "0px", "color": "#205072"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div([
                    html.Div(
                        dcc.Link(f"{page['name']}", 
                                 href=page["relative_path"],
                                 className="button-link"
                                 )
                    ) for page in dash.page_registry.values()
                ],
                    className="button-container one-third column",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        # Sub-pages container
        dash.page_container,
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# Main
if __name__ == "__main__":
    app.run(debug=True)