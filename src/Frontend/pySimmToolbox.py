import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt

import pandas as pd
import CRIF.CrifUtil
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation
from Frontend.FrontendDataFiltering import *
from Frontend.FrontendGraphs import *

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5('pySimmToolbox'),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='CRIF', value='CRIF', children=[
            html.Div([
                dcc.Store(id='Crifs'),
                dcc.Store(id='Crif')
            ]),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style = {
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin' : '30px',
                },
                multiple=True
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.H6('Selected CRIF: ',
                                style={'textAlign': 'right'})
                    ], className="col s2"),

                    html.Div([
                        dcc.Dropdown(id='counterpartySelect',
                                     placeholder='Please upload a CRIF',
                                     clearable=False)
                    ], className="col s2"),
                    html.Div([
                        html.Button('Calculate IM', id='Calculate IM', n_clicks='on',
                                    style={
                                        'width': '100%',
                                        'height': '35px',
                                        'lineHeight': '35px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '0px',
                                    }
                                    )
                    ], className="col s2"),
                    html.Div([
                        html.Button('Calculate Allocation', id='Calculate Allocation', n_clicks='on',
                                    style={
                                        'width': '100%',
                                        'height': '35px',
                                        'lineHeight': '35px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'solid',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '0px'
                                    }
                                    )
                    ], className="col s2")
                ], className="row")
            ]),
            html.Hr(),
            html.Div(id='output-data-upload')
        ]),
        dcc.Tab(label='IM', value='Initial Margin', children=[
            html.Div([
                dcc.Store(id='IMResult')]),
            html.H5(id='calculated IM', style={'textAlign':'center',
                                               'topMargin' : '20px'}),
            html.Hr(),
            dcc.Graph(id='IMTree')
        ]),

        dcc.Tab(label='Allocation', value='IM Allocation')
    ])
])

def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        df = CRIF.CrifUtil.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

# Nachdem ein CRIF hochgeladen wurde werden alle Einträge des Crifs im CRIF Tab eingeblendet
@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        df = parse_contents(list_of_contents[0])
        return html.Div([
                            html.H5(list_of_names[0]),
                            html.H6(datetime.datetime.fromtimestamp(list_of_dates[0])),
                            dt.DataTable(
                                data=df.to_dict('rows'),
                                columns=[{'name': i, 'id': i} for i in df.columns]),
                            html.Hr(),
                            html.Div('Raw Content'),
                            html.Pre(list_of_contents[0][0:200] + '...', style={
                                'whiteSpace': 'pre-wrap',
                                'wordBreak': 'break-all'
                            })])

# Nachdem ein CRIF (mit möglicherweise mehreren Gegenparteien) hochgeladen wurde wird es abgespeichert.
@app.callback(Output('Crifs', 'data'),
              [Input('upload-data', 'contents')])
def fill_CrifsStorage(contents):
    if contents is not None:
        df = parse_contents(contents[0])
        json = df.to_json()
        return json

# Nachdem ein CRIF hochgeladen wurde wird das erste CRIF als analysierbares CRIF abgespeichert.
# Wenn man im Dropdownmenü eine anderes CRIF auswählt wird das gespeicherte CRIF zur Analyse entsprechend angepasst.
@app.callback(Output('Crif', 'data'),
              [Input('counterpartySelect', 'value')],
              [State('Crifs', 'data')])
def fill_CrifStorage(value, data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    if value is None or df[df.IMLedis == value].empty:
        cp = df.IMLedis.unique()[0]
    else:
        cp = value
    dfone = df[df.IMLedis==cp]
    json = dfone.to_json()
    return json

# Nachdem ein CRIF hochgeladen wurde werden die Gegenparteien des CRIFs im Dropdownmenü zur Auswahl angelegt.
@app.callback(Output('counterpartySelect', 'options'),
              [Input('Crifs', 'data')])
def initial_load_selectDropdown(data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    Cps = df.IMLedis.unique()
    options_dicts = [{'label':cp, 'value':cp} for cp in Cps]
    return options_dicts

# Nachdem ein neues CRIF hochgeladen wurde wähle die erste CP als Value aus.
@app.callback(Output('counterpartySelect', 'value'),
              [Input('Crifs', 'data')])
def initial_dropdown_value(data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    cp0 = df.IMLedis.unique()[0]
    return cp0

# Button werden grün nachdem ein CRIF ausgewählt wurde
@app.callback(Output('Calculate IM', 'style'),
              [Input('counterpartySelect', 'value')],
              [State('Calculate IM', 'style')])
def change_Calculate_IM_Button_color(value, style):
    if value is not None:
        style['backgroundColor'] = '#00e600'
    return style


# Button werden grün nachdem ein CRIF ausgewählt wurde
@app.callback(Output('Calculate Allocation', 'style'),
              [Input('counterpartySelect', 'value')],
              [State('Calculate Allocation', 'style')])
def change_Calculate_IM_Button_color(value, style):
    if value is not None:
        style['backgroundColor'] = '#00e600'
    return style

# When calculate IM is pressed IM is calculated and non-allocated result is saved
@app.callback(Output('IMResult', 'data'),
                        [Input('Calculate IM', 'n_clicks')],
                        [State('Crif', 'data')])
def calculate_IM(n_clicks, data):
    if data is None:
        raise PreventUpdate
    crif = Crif(pd.read_json(data))
    imTree = StandardCalculation.calculate(crif)
    df = imTree.toDataFrame()
    return df.to_json()

@app.callback(Output('calculated IM', 'children'),
              [Input('IMResult', 'data')])
def show_calculated_IM(data):
    if data is None:
        raise PreventUpdate
    im = getIM(pd.read_json(data))
    ResultString = 'The calculated IM is ' + '{:,.2f}'.format(im)
    return ResultString

@app.callback(Output('IMTree', 'figure'),
              [Input('IMResult', 'data')])
def generate_IMTree(data):
    if data is None:
        raise PreventUpdate
    return create_tree_graph(pd.read_json(data))

# @app.callback(Output('calculated IM', 'children'),
#                 [Input('Calculate IM', 'n_clicks')],
#                 [State('Crif', 'data')])
# def calculate_IM(n_clicks, data):
#     if data is None:
#         raise PreventUpdate
#     crif = Crif(pd.read_json(data))
#     imTree = StandardCalculation.calculate(crif)
#     imTree.to_json()
#     ResultString = 'The calculated IM is ' + '{:,.2f}'.format(imTree.getMargin())
#     return ResultString

# Wenn man im Dropdownmenü eine andere Gegenpartei auswählt wird das gespeicherte CRIF zur Analyse entsprechend angepasst.
# @app.callback(Output('Crif', 'data'),
#               [Input('counterpartySelect', 'value')],
#               [State('Crifs', 'data')])
# def cp_select(selectedCp, data):
#     if selectedCp != 'Default':
#         df = pd.read_json(data)
#         json = df[df.IMLedis==selectedCp].to_json()
#         return json

# Wenn man auf das CRIF Tab wechselt so wird die Gegenpartei des aktuellen gespeicherten CRIF als Startwert genommen

if __name__ == '__main__':
    app.run_server(debug=True)