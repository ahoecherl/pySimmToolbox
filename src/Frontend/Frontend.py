import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt


import pandas as pd
import CRIF.CrifUtil
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5('pySimmToolbox'),
    dcc.Upload(id='CrifUpload',
               children=html.Div([
                   'Drag and Drop your CRIF or ',
                   html.A('select it'),
                   '.'
                    ]),
               style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                    },
               multiple=True
                ),
    html.Button('CalculateIM', id='calc'),
    html.H5(id='InitialMargin', children=0),
    dcc.Store(id='Crifs'),
    dcc.Store(id='Crif'),
    dt.DataTable(id='CrifDataTable', data=[{}]),
    ]
)

@app.callback(Output('CrifDataTable','data'),
                [Input('CrifUpload', 'contents')])
def update_table(contents):
    if contents is None:
        return
    content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)
    df = CRIF.CrifUtil.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df.to_dict('rows')

@app.callback(Output('CrifDataTable','columns'),
                [Input('CrifUpload', 'contents')])
def update_table(contents):
    if contents is None:
        return
    content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)
    df = CRIF.CrifUtil.read_csv(io.StringIO(decoded.decode('utf-8')))
    return [{'name': i, 'id': i} for i in df.columns]

@app.callback(Output('Crifs', 'data'),
              [Input('CrifUpload', 'contents')])
def store_crifs(contents):
    if contents is None:
        return
    content_type, content_string = contents[0].split(',')
    decoded = base64.b64decode(content_string)
    df = CRIF.CrifUtil.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df.to_json()

@app.callback(Output('Crif', 'data'),
                [Input('Crifs', 'data')])
def store_crif(data):
    if data is None:
        return
    crifsDF = pd.read_json(data)
    firstCP = crifsDF.IMLedis.unique()[0]
    crifDF = crifsDF[crifsDF.IMLedis==firstCP]
    return crifDF.to_json()

@app.callback(Output('InitialMargin', 'children'),
                [Input('calc', 'n_clicks')],
                [State('Crif', 'data')])
def calculate_IM(n_clicks, data):
    if n_clicks is None:
        return 0
    crifDF = pd.read_json(data)
    crif = Crif(crifDF)
    imTree = StandardCalculation.calculate(crif)
    im = imTree.getMargin()
    return im

if __name__ == '__main__':
    app.run_server(debug=True)