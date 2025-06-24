import dash
from dash import html, dcc, Input, Output, State, ClientsideFunction, callback

# dash.register_page(__name__, 
#                     name='Field Monitoring',
#                     title='Field Monitoring',
#                     description='Field Monitoring Page',
#                     image='assets/logo-vpi.png',
#                     path='/field')

# App layout
# layout = html.Div([
#     html.H4(id="fieldWellText"),
#     html.P(
#             "This is a field page",
#         ),
#     dcc.Dropdown(
#                 id="fieldWellSelect",
#                 options=["Production", "Exploration"],
#                 value="Exploration",
#                 multi=False,
#                 className="dcc_control",
#             ),
# ])

# @callback(
#     Output('fieldWellText', 'children'),
#     Input('fieldWellSelect', 'value')
# )
# def update_selected(input_value):
#     return f'You selected: {input_value}'