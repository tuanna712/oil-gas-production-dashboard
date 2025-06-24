import plotly.graph_objects as go
from dash import dcc, html, callback, Input, Output
from data import load_wells, load_data

# Mapbox configuration
MAPBOX_STYLE_URL = "mapbox://styles/vpimaps/clicpykux000n01r0gpia4pxh"
MAPBOX_ACCESS_TOKEN= "pk.eyJ1IjoidnBpbWFwcyIsImEiOiJjbGkxNHVpam0wM205M3FtdmpzN2phZTQ0In0.2o76HfADkKZphFBPlQ_fSA"
# Dim colors for background wells
DIM_COLOR_PROD = 'rgba(0, 128, 0, 0.4)'  # Semi-transparent green
DIM_COLOR_EXPL = 'rgba(0, 0, 255, 0.4)' # Semi-transparent blue

# Highlight colors for selected well
HIGHLIGHT_COLOR_PROD = 'rgba(0, 255, 0, 1)' # Bright green
HIGHLIGHT_COLOR_EXPL = 'rgba(0, 0, 255, 1)' # Bright blue

# --- Callback to update the Mapbox graph ---
@callback(
    Output('mapbox-graph', 'figure'),  # Output is the figure property of the dcc.Graph
    Input('wellSelect', 'value')       # Input is the value of the wellSelect dropdown
)
def update_mapbox_graph(selected_well_name):
    # Load the data
    data = load_data()
    wells_df = load_wells()
    all_wells_df = wells_df.rename(columns={'X': 'lat', 'Y': 'lon', 'WellID': 'well_name', 'Type': 'well_type'})

    # Initialize the list of traces for the map
    traces = []

    # --- 1. Create the base layer with all wells (dimmed) ---
    base_marker_size = 12
    base_marker_opacity = 0.8

    # Separate dataframes for dim production and exploration wells
    dim_prod_df = all_wells_df[(all_wells_df['well_type'] == 'Production') & (all_wells_df['well_name'] != selected_well_name)]
    dim_expl_df = all_wells_df[(all_wells_df['well_type'] == 'Exploration') & (all_wells_df['well_name'] != selected_well_name)]
    if not dim_prod_df.empty:
            traces.append(go.Scattermapbox(
                lat=dim_prod_df['lat'],
                lon=dim_prod_df['lon'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=base_marker_size,
                    color=DIM_COLOR_PROD,
                    opacity=base_marker_opacity
                ),
                text=[f"Well: {row['well_name']}<br>Type: {row['well_type']}" for index, row in dim_prod_df.iterrows()],
                hoverinfo='text',
                name='Production Wells'
            ))

    if not dim_expl_df.empty:
        traces.append(go.Scattermapbox(
            lat=dim_expl_df['lat'],
            lon=dim_expl_df['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=base_marker_size,
                color=DIM_COLOR_EXPL,
                opacity=base_marker_opacity
            ),
            text=[f"Well: {row['well_name']}<br>Type: {row['well_type']}" for index, row in dim_expl_df.iterrows()],
            hoverinfo='text',
            name='Exploration Wells'
        ))

    # --- 2. Add the highlighted well if one is selected ---
    center_lat = all_wells_df['lat'].mean()
    center_lon = all_wells_df['lon'].mean()
    zoom_level = 10 # Default zoom to show all wells in the region
    if selected_well_name:
        highlighted_well_df = all_wells_df[all_wells_df['well_name'] == selected_well_name]
        if not highlighted_well_df.empty:
            well_data = highlighted_well_df.iloc[0]
            highlight_lat = well_data['lat']
            highlight_lon = well_data['lon']
            highlight_type = well_data['well_type']

            # Determine highlight color and label based on well type
            highlight_color = HIGHLIGHT_COLOR_PROD if highlight_type == 'Production' else HIGHLIGHT_COLOR_EXPL
            highlight_label = f"{well_data['well_name'][:-1]}-{well_data['well_type']}"

            traces.append(go.Scattermapbox(
                lat=[highlight_lat],
                lon=[highlight_lon],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=18, # Larger size for emphasis
                    color=highlight_color,
                    opacity=1,
                    symbol='star' # Use a distinct symbol
                ),
                text=[f"Well: {well_data['well_name']}<br>Lat: {well_data['lat']:.4f}<br>Lon: {well_data['lon']:.4f}<br>Type: {well_data['well_type']}"],
                hoverinfo='text',
                name=highlight_label
            ))

            # Center map on the selected well and zoom in
            center_lat = highlight_lat
            center_lon = highlight_lon
            zoom_level = zoom_level # Zoom in more for a single selected well
        else:
            # If selected_well_name somehow doesn't match any well (shouldn't happen with proper dropdown linking)
            pass

    # --- Configure the Mapbox layout ---
    fig = go.Figure(data=traces)

    fig.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=center_lat,
                lon=center_lon
            ),
            pitch=0,
            zoom=zoom_level,
            # style='street',#MAPBOX_STYLE_URL,
        ),
        margin={"r":0,"t":0,"l":0,"b":0}, # Remove outer margins
        showlegend=True, # Show the legend to differentiate dim vs. highlighted
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig