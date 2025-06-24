import dash
from dash import html, dcc, Input, Output, State, ClientsideFunction, callback
from data import load_wells, load_data
from graphs.map import update_mapbox_graph
from components.well.left_pannel import well_selection, mapbox_map
from components.well.right_pannel import well_statistics, right_charts,  update_well_statistics
from controls import WELLS

dash.register_page(__name__, 
                    name='Well Monitoring',
                    title='Well Monitoring',
                    description='Well Monitoring Page',
                    image='assets/logo-vpi.png',
                    path='/')

wells = load_wells()
data = load_data()

year_slider = dcc.RangeSlider(
                            id="year_slider",
                            min=2019,
                            max=2025,
                            marks={i: "{}".format(i) for i in range(2019, 2026)},
                            step=1,
                            value=[2019, 2025],
                            className="dcc_control",
                        )


left_panel = html.Div(
    [
        well_selection,
        year_slider,
        mapbox_map,
    ],
    className="pretty_container",
    style={"width": "30%",
            "display": "flex",
            "flex-direction": "column",
        },
)

right_panel = html.Div(
    [
        well_statistics,
        right_charts,
    ],
    id="right-column",
    className="ten columns",
)
# App layout
layout = html.Div(
    [
        left_panel,
        right_panel,
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "row"},
)

@callback(
    Output('wellSelect', 'options'),  # The property to update (options of wellSelect)
    Output('wellSelect', 'value'),    # The property to update (value of wellSelect)
    Input('typeSelect', 'value')      # The input that triggers the callback (value of typeSelect)
)
def set_wells_options(selected_type):
    if selected_type is None:
        # Handle case where no type is selected, or initial load if value is None
        return [], None # Return empty options and no value

    # Get the list of wells for the selected type
    wells_for_type = WELLS.get(selected_type, [])

    # Format them for the dcc.Dropdown options prop
    options = [{'label': well, 'value': well} for well in wells_for_type]

    # Set a default value for the wellSelect dropdown.
    # Choose the first well in the list if available, otherwise None.
    default_value = wells_for_type[0] if wells_for_type else None

    return options, default_value

