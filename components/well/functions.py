"""
@callback(
    Output("last_month_text", "children"),
    Input("wellSelect", "value"),
)
def update_last_month_text(wellSelect):
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
)
def line_chart_monthly(wellSelect, year_slider):
    title_text = f"{wellSelect} - Monthly Production Trends"

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
        y3 = well_df["WatMo"]

    traces = [
        go.Scatter(
            x=date, y=y1, mode='lines', name='Oil',
            line=dict(color='#2ca02c', shape='spline', smoothing=1.1)
        ),
        go.Scatter(
            x=date, y=y2, mode='lines', name='Gas',
            line=dict(color='#ff7f0e', shape='spline', smoothing=1.1)
        ),
        go.Scatter(
            x=date, y=y3, mode='lines', name='Water',
            line=dict(color='#1f77b4', shape='spline', smoothing=1.1)
        )
    ]

    # --- Add annotations for line labels at the end of each line ---
    annotations = []
    # Note: well_df must be sorted by 'Date' for this to reliably get the last point

    if not well_df.empty:
        last_date = well_df["Date"].iloc[-1] # Get the last date for positioning

        # Annotation for Oil
        if not y1.empty:
            annotations.append(
                dict(
                    x=last_date,
                    y=y1.iloc[-1], # Last value of OilMo
                    xref="x", yref="y",
                    text="Oil",
                    showarrow=False,
                    xanchor="left", # Align text to the left of the point
                    font=dict(color='#2ca02c', size=10),
                    xshift=5 # Small shift to the right to avoid overlap with line end
                )
            )

        # Annotation for Gas
        if not y2.empty:
            annotations.append(
                dict(
                    x=last_date,
                    y=y2.iloc[-1], # Last value of GasMo
                    xref="x", yref="y",
                    text="Gas",
                    showarrow=False,
                    xanchor="left",
                    font=dict(color='#ff7f0e', size=10),
                    xshift=5
                )
            )

        # Annotation for Water
        if not y3.empty:
            annotations.append(
                dict(
                    x=last_date,
                    y=y3.iloc[-1], # Last value of WatMo
                    xref="x", yref="y",
                    text="Water",
                    showarrow=False,
                    xanchor="left",
                    font=dict(color='#1f77b4', size=10),
                    xshift=5
                )
            )


    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            title=dict(
                text=title_text,
                font=dict(size=14, color='#205072'),
            ),
            margin=dict(l=20, r=40, t=40, b=20), # Increase right margin to make space for labels
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                automargin=True # Ensure x-axis labels don't get cut off
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#D3D3D3',
                automargin=True # Ensure y-axis labels don't get cut off
            ),
            showlegend=False, # <--- IMPORTANT: HIDE THE LEGEND
            annotations=annotations # <--- ADD THE ANNOTATIONS HERE
        )
    )
    return fig

"""