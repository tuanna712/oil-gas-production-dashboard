LAT_CENTER = 20.567326
LONG_CENTER = 106.688371
BLUE = "#2A398C"
GREEN = "#169046"
COLOR_PALETTE = {
    "b0": "#1A84C4",
    "b1": "#1967AC",
    "bl": "#000000",
    "g0": "#32B52B",
    "g1": "#32B52B",
}
COLOR_PALETTE_2 = {
    "c0": "#205072",
    "c1": "#329D9C",
    "c2": "#56C596",
    "c3": "#7BE495",
    "c4": "#CFF4D2",
}
# Global Chart Template
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        style="open-street-map",
        center=dict(lon=LONG_CENTER, lat=LAT_CENTER),
        zoom=7,
    ),
)

WELLS = {
    "Exploration": ['2X', '3X', '4X', '5X', '7X'],
    "Production": ['101P', '104P', '106P', '105P', '102P', '107P', '103P', '108P', '201P', '211P', '204P', '202P'],
}
