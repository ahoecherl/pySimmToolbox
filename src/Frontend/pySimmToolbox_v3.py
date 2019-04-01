import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import Frontend.callbacks as callbacks
import json

external_stylesheets = ['https://fonts.googleapis.com/icon?family=Material+Icons']

external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']

VALID_USERNAME_PASSWORD_PAIRS = [
    ['pySimmToolbox', 'pySimmToolbox']
]

app = dash.Dash(__name__
                , external_stylesheets=external_stylesheets
                , external_scripts=external_scripts)

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = \
    html.Div([
        dcc.Store(id='Crifs'),
        dcc.Store(id='Crif'),
        dcc.Store(id='currentCrifInMemory'),
        dcc.Store(id='currentCrifCalculated'),
        dcc.Store(id='IMResult'),
        dcc.Store(id='allocTree'),
        dcc.Store(id='hasNonAlloc', data=json.dumps({'boolean':False})),
        dcc.Store(id='hasAllocation', data=json.dumps({'boolean':False})),
        dcc.Store(id='selectedNode'),
        dcc.Store(id='treeMapColors'),
        html.Nav([
            html.Div([
                html.A([html.Img(src='assets/d-fine_logo-white_RGB.svg',
                                 className='d-fine-logo')],
                       className='brand-logo left',
                       href='https://www.d-fine.com/'),
                html.Ul([
                    html.Li([html.A(['FutureTool'],className='d-fine-electric')]),
                    html.Li([html.A(['pySIMMToolbox'],className='d-fine-electric')])
                ],
                className='right')
            ],className= 'nav-wrapper')
        ]),
        html.Div(className='container', children=[
            dcc.Tabs(id='tabs', value='File Upload', className='custom-tabs-container center', parent_className='custom-tabs', children=[
                dcc.Tab(label='File Upload', value='File Upload', className='custom-tab leftTab', selected_className='custom-tab--selected', children=[
                    html.Div(className='section', style={'margin-top':66}, children=[
                        html.Div(className='row', children=[
                            html.Div(className='col s6', children=[
                                dcc.Upload(className='CRIFUpload card z-depth-3', id='CRIFUpload',children=[
                                    html.Div(className='card-content', children= [
                                        html.Span(className='card-title', children=['Drag and Drop or ',
                                               html.A('Select a file containing CRIF(s)', className='UploadLink')])
                            ])])]),
                            html.Div(className='col s6', children=[
                                html.Div(className='card z-depth-1 right', children=[
                                    html.Div(className='card-content d-fine-prussian-text',id='uploaded-file-info', children=[
                                        html.Span('Uploaded File',className='card-title'),
                                        html.P('No File has been uploaded')
                                    ])
                                ])
                            ])
                        ])
                    ])
                ]),
                dcc.Tab(label='Analyze single CRIF', value='Analyze single CRIF', className='custom-tab', selected_className='custom-tab--selected', children=[
                    html.Div(className='section', children=[
                        html.Div(className='right-align', children=[
                            html.Div(html.Button('Standalone and Euler Allocation',
                                                 className='btn-large',
                                                 disabled=True,
                                                 id='allocation_button'),
                                     className='right ButtonRow'),
                            html.Div(html.Button('Calculate IM',
                                                 className='btn-large',
                                                 disabled=True,
                                                 id='calculate_im_button'),
                                     className='right ButtonRow'),
                            html.Div(html.Button('Load Crif in Memory',
                                                 className='btn-large',
                                                 disabled=True,
                                                 id='load_crif_button'),
                                     className='ButtonRow right-align'),
                        ]),
                        html.Div(className='row', children=[
                            html.Div(className='col s8 row', children=[
                                html.Div(className='row innerRow', children=[
                                    html.Div(className='col s6', children=[
                                        html.Div(className='card white z-depth-0', id='crif-select-card', children=[
                                            html.Div(className='card-content grey-text', id='crif-select-card-content', children=[
                                                html.Span('Select a single CRIF from your file',
                                                           className='card-title'),
                                                html.Label('Select counterparty', id='select_counterparty_label'),
                                                dcc.Dropdown(id='select_counterparty',
                                                              clearable=False),
                                                html.Label('Select direction', id='select_direction_label'),
                                                dcc.Dropdown(id='select_direction',
                                                              clearable=False),
                                                html.Label('Select regulation', id='select_regulation_label'),
                                                dcc.Dropdown(id='select_regulation',
                                                              clearable=False)
                                            ])
                                        ])
                                    ]),
                                    html.Div(className='col s6', children=[
                                        html.Div(className='card d-fine-prussian z-depth-1 hide', id='CRIFCard', children=[
                                            html.Div(className='card-content white-text', children=[
                                                html.Span('No CRIF in Memory', id='crifInMemoryCard',
                                                            className='card-title'),
                                                html.Div(className='row innerRow', children=[
                                                    html.Div(className='col s4 innerDiv', children=[
                                                        html.Div(className='card-panel d-fine-silver d-fine-prussian-text valign-wrapper innerPanel', id='tradeCount')
                                                    ]),
                                                    html.Div(className='col s4 innerDiv', children=[
                                                        html.Div(className='card-panel d-fine-silver d-fine-prussian-text valign-wrapper innerPanel', id='rowCount')
                                                    ]),
                                                    html.Div(className='col s4 innerDiv', children=[
                                                        html.Div(className='card-panel d-fine-silver d-fine-prussian-text valign-wrapper innerPanel', id='scheduleCount')
                                                    ])]),
                                        html.Div(className='row innerRow', children=[
                                                    html.Div(className='col s6 offset-s3 innerDiv', children=[
                                                        html.Div(className='z-depth-1 card-panel d-fine-electric valign-wrapper innerPanel center hide', id='IMdisplay')

                                                    ]),
                                        ]),
                                                html.Div(className='row innerRow', children=[
                                                    html.Div(className='col s4 offset-s1 innerDiv', children=[
                                                        html.Div(className='z-depth-0 card-panel d-fine-silver d-fine-prussian-text valign-wrapper innerPanel center hide', children=['Euler Allocated'], id='eulerCard')
                                                ]),
                                                    html.Div(className='col s4 offset-s2 innerDiv', children=[
                                                    html.Div(className='z-depth-0 card-panel d-fine-silver d-fine-prussian-text valign-wrapper innerPanel center hide', children=['Standalone Allocated'], id='standaloneCard')
                                                ])
                                                ])
                                            ]),
                                            html.Div(className='card-action', children=[
                                                html.A(className='left-align cardLink',id='Download CRIF', href='',download='CRIF.csv', children='Download CRIF'),
                                                html.A(className='right-align hide cardLink', id='Download IM Tree',download='IMTree.csv', children='Download IM Tree')
                                            ])
                                        ])
                                    ])
                                ]),
                                html.Div(className='card col s12 white z-depth-1 hide treecard', id = 'IMTreeContainer', children=[
                                     html.Div([
                                         html.Span('IM Tree - Select node to analyze', className='card-title treeheading', style={'textAlign': 'left'}),
                                         dcc.Graph(id='IMTree', config={'displayModeBar': False}, style={'overflowX':'scroll'})],
                                         className = 'card-content center-align treecardcontent',
                                     )])
                            ]),
                            html.Div(className='col s4 row', children=[
                                html.Div(className='card col s12 white z-depth1 treecard', id='TreeMapContainer', children=[
                                    html.Div(className='card-content center-allign treecardcontent', children=[
                                        html.Nav(className='treeNav', children=[
                                            html.Div(className= 'nav-wrapper valign-wrapper', id='treeNavContent', style={'padding-left': 10}, children=[
                                                html.Div(children=[
                                                    html.A('Please select a node', className='breadcrumb', href='#!')
                                                ])
                                            ])
                                        ]),
                                        dcc.Graph(id='TreeMapStandalone', config={'displayModeBar': False}, style={'max-height':'30vh'}),
                                        html.Div(' ', style={'height':20, 'width':'100%'}),
                                        dcc.Graph(id='TreeMapEulerPositive', config={'displayModeBar': False}, style={'max-height':'30vh'}),
                                        html.Div(' ', style={'height':20, 'width':'100%'}),
                                        dcc.Graph(id='TreeMapEulerNegative', config={'displayModeBar': False}, style={'max-height':'30vh'}),
                                    ])
                                ])
                            ])
                        ])
                    ])
                ]),
                dcc.Tab(label='Analyze multiple CRIFs',
                        value='Analyze multiple CRIFs',
                        className='custom-tab rightTab',
                        selected_className='custom-tab--selected')
            ])
        ])
    ])


# Speichere CRIF-Datei ab, die hochgeladen wird:
@app.callback(Output('Crifs', 'data'),
              [Input('CRIFUpload', 'contents')])
def fill_CrifsStorage(contents):
    return callbacks.fill_CrifsStorage(contents)

# Zeige Informationen über die hochgeladene Datei an:
@app.callback(Output('uploaded-file-info', 'children'),
              [Input('CRIFUpload', 'filename'),
               Input('Crifs', 'data')])
def create_crifs_information(filename, data):
    return callbacks.create_crifs_information(filename, data)

# Nachdem eine CRIF Datei hochgeladen wurde wird die Select Card Orange
@app.callback(Output('crif-select-card', 'className'),
              [Input('Crifs', 'data')],
              [State('crif-select-card', 'className')])
def make_crif_select_card_orange(data, className):
    return callbacks.make_crif_select_card_orange(data, className)

# Nachdem eine CRIF Datei hochgeladen wurde wird die Select Schrift Weiß
@app.callback(Output('crif-select-card-content', 'className'),
              [Input('Crifs', 'data')],
              [State('crif-select-card-content', 'className')])
def make_crif_select_card_text_white(data, className):
    return callbacks.make_crif_select_card_text_white(data, className)

# Nachdem eine CRIF Datei hochgeladen wurde wird die Schrift der Labels weiß
@app.callback(Output('select_counterparty_label', 'className'),
              [Input('Crifs', 'data')],
              [State('select_counterparty_label', 'className')])
def make_select_counterparty_label_white(data, className):
    return callbacks.make_label_white(data, className)

@app.callback(Output('select_direction_label', 'className'),
              [Input('Crifs', 'data')],
              [State('select_direction_label', 'className')])
def make_select_counterparty_label_white(data, className):
    return callbacks.make_label_white(data, className)

@app.callback(Output('select_regulation_label', 'className'),
              [Input('Crifs', 'data')],
              [State('select_regulation_label', 'className')])
def make_select_counterparty_label_white(data, className):
    return callbacks.make_label_white(data, className)

# Nachdem ein CRIF hochgeladen wurde werden die Gegenparteien des CRIFs im Dropdownmenü zur Auwahl angelegt
@app.callback(Output('select_counterparty', 'options'),
              [Input('Crifs', 'data')])
def initial_load_select_counterparty(data):
    return callbacks.initial_load_select_counterparty(data)

# Nachdem ein neues CRIF hochgeladen wurde wähle die erste CP als Value aus.
@app.callback(Output('select_counterparty', 'value'),
              [Input('select_counterparty', 'options')])
def initial_counterparty_select(options):
    return callbacks.initial_select(options)

# Nachdem eine Counterparty ausgewählt wurde scanne welche directions vorliegen.
@app.callback(Output('select_direction', 'options'),
              [Input('select_counterparty', 'value')],
              [State('Crifs', 'data')])
def initial_load_select_direction(value, data):
    return callbacks.initial_load_select_direction(value, data)

# Nachdem neue directions vorliegen wähle die erste als aktuellen Wert aus.
@app.callback(Output('select_direction', 'value'),
              [Input('select_direction', 'options')])
def initial_directions_select(options):
    return callbacks.initial_select(options)

# Nachdem eine direction ausgewählt wurde scanne, welche Regime/Regularien vorliegen.
@app.callback(Output('select_regulation', 'options'),
              [Input('select_direction', 'value')],
              [State('select_counterparty', 'value'),
               State('Crifs', 'data')])
def inital_load_select_regulation(direction, counterparty, data):
    return callbacks.initial_load_select_regulations(direction, counterparty, data)

# Nachdem neue regularien vorliegen, wähle die erste als aktuellen Wert aus.
@app.callback(Output('select_regulation', 'value'),
              [Input('select_regulation', 'options')])
def initial_regulation_select(options):
    return callbacks.initial_select(options)

# Nachdem die Regularie upgedated worden ist, kann ein neues CRIF in memory geladen werden - aktiviere den Button
# Falls gewähltes CRIF und CRIF in Memory nicht mehr übereinstimmen aktiviere den Knopf
@app.callback(Output('load_crif_button', 'disabled'),
              [Input('select_counterparty', 'value'),
               Input('select_direction', 'value'),
               Input('select_regulation', 'value'),
               Input('currentCrifInMemory', 'data')])
def disable_load_crif_button(counterparty, direction, regulation, crif_in_memory_identifier):
    return callbacks.disable_load_crif_button(regulation, crif_in_memory_identifier, counterparty, direction)

# Nachdem load_crif_button gedrück wird, wird neues CRIF geladen
@app.callback(Output('Crif', 'data'),
              [Input('load_crif_button', 'n_clicks')],
              [State('select_counterparty', 'value'),
               State('select_direction', 'value'),
               State('select_regulation', 'value'),
               State('Crifs', 'data')])
def load_single_crif_in_memory(n_clicks, counterparty, direction, regulation, data):
    return callbacks.load_single_crif_in_memory(n_clicks, counterparty, direction, regulation, data)

# Nachdem ein CRIF geladen wurde wird abgespeichert, was das für ein CRIF ist
@app.callback(Output('currentCrifInMemory', 'data'),
              [Input('Crif', 'data')],
              [State('select_counterparty', 'value'),
               State('select_direction', 'value'),
               State('select_regulation', 'value')])
def store_identifier_of_crif_in_memory(data, counterparty, direction, regulation):
    return callbacks.store_identifier_of_crif_in_memory(data, counterparty, direction, regulation)

# Nachdem ein CRIF in Memory ist ändere überschrift der CRIF in Memory Card
@app.callback(Output('crifInMemoryCard', 'children'),
              [Input('currentCrifInMemory', 'data')])
def set_crif_in_memory_title(data):
    return callbacks.set_crif_in_memory_title(data)

# Nachdem crif geladen wurde wird CRIF in Memory Card eingeblendet
@app.callback(Output('CRIFCard', 'className'),
              [Input('currentCrifInMemory', 'data')],
              [State('CRIFCard', 'className')])
def show_crif_card(data, className):
    return callbacks.unhide_element(data, className)

# Nachdem CRIF geladen wurde wird tradeCount, rowCount und ScheduleTradeCount berechnet
@app.callback(Output('tradeCount', 'children'),
              [Input('Crif', 'data')])
def show_trade_count(crif):
    return callbacks.show_trade_count(crif)

@app.callback(Output('rowCount', 'children'),
              [Input('Crif', 'data')])
def show_row_count(crif):
    return callbacks.show_row_count(crif)

@app.callback(Output('scheduleCount', 'children'),
              [Input('Crif', 'data')])
def show_schedule_count(crif):
    return callbacks.show_schedule_count(crif)

# Enable the Downloadlink as soon as as CRIF has been put into memory
@app.callback(
    Output('Download CRIF', 'href'),
    [Input('Crif', 'data')])
def enableCrifDownload(data):
    return callbacks.enableDownload(data)

# Nachdem CRIF in Memory ist aktiviere den Calulate IM Button
@app.callback(Output('calculate_im_button', 'disabled'),
               [Input('currentCrifCalculated', 'data'),
               Input('currentCrifInMemory', 'data')])
def disable_calculate_im_button(crifCalculated, crifInMemory):
    return callbacks.disable_calculate_im_button(crifCalculated, crifInMemory)

# When calculate IM is pressed IM is calculated and non-allocated result is saved
@app.callback(Output('IMResult', 'data'),
              [Input('calculate_im_button', 'n_clicks')],
              [State('Crif', 'data')])
def calculate_IM(n_clicks, crif):
    return callbacks.calculate_IM(crif)

# When a CRIF has been calculated, save the information, which CRIF is currently stored as calculated
@app.callback(Output('currentCrifCalculated', 'data'),
              [Input('IMResult', 'data')],
              [State('currentCrifInMemory', 'data')])
def set_current_crif_calculated(notNeeded, data):
    return callbacks.set_current_crif_calculated(data)

# After the IM has been calculated the IM Tree plot is created
@app.callback(Output('IMTree', 'figure'),
              [Input('IMResult', 'data')])
def generate_IMTree(data):
    return callbacks.generate_IMTree(data)

# After the IM has been calculated unhide the download IM Tree button
@app.callback(Output('Download IM Tree', 'className'),
              [Input('currentCrifCalculated', 'data'),
               Input('currentCrifInMemory', 'data')],
              [State('Download IM Tree', 'className')])
def show_download_Tree_link(calculated, memory, className):
    return callbacks.show_download_Tree_link(calculated, memory, className)

# After the IM has been calculated display the Overall amount
@app.callback(Output('IMdisplay', 'children'),
              [Input('IMResult', 'data')])
def show_IM(imTree):
    return callbacks.show_IM(imTree)

# If IM for crif in memory has been calculted unhide IM Result Card
@app.callback(Output('IMdisplay', 'className'),
              [Input('currentCrifCalculated','data'),
               Input('currentCrifInMemory', 'data')],
              [State('IMResult', 'data'),
               State('IMdisplay', 'className')])
def show_IM_result_card(calculated, memory, data, className):
    return callbacks.show_allocation_card(data, memory, calculated, className)

# If an IM Tree plot matching the CRIF in memory is available it may be displayed
@app.callback(Output('IMTreeContainer', 'className'),
              [Input('IMResult', 'data'),
               Input('currentCrifInMemory', 'data'),
               Input('currentCrifCalculated', 'data')],
              [State('IMTreeContainer', 'className')])
def show_im_tree(figure, currentCrifInMemory, currentCrifCalculated, className):
    return callbacks.show_calculated_im_element(figure, currentCrifInMemory, currentCrifCalculated, className)

# If an according calculation button is pressed this is stored. If new CRIF is loaded things are reset.
@app.callback(Output('hasNonAlloc', 'data'),
              [Input('calculate_im_button', 'n_clicks'),
               Input('currentCrifInMemory', 'data')],
              [State('currentCrifCalculated', 'data')])
def set_hasNonAlloc(n_clicks, memory, calculated):
    return callbacks.set_treeComponentIndicator(n_clicks, memory, calculated)

@app.callback(Output('hasAllocation', 'data'),
              [Input('allocation_button', 'n_clicks'),
               Input('currentCrifInMemory', 'data')],
              [State('currentCrifCalculated', 'data')])
def set_Alloc(n_clicks, memory, calculated):
    return callbacks.set_treeComponentIndicator(n_clicks, memory, calculated)

# Activate StandaloneAllocButton only if not yet calculated
@app.callback(Output('allocation_button', 'disabled'),
              [Input('hasAllocation', 'data'),
               Input('currentCrifCalculated', 'data')],
              [State('currentCrifInMemory', 'data')])
def disable_allocation_button(data, calculated, memory):
    return callbacks.disable_allocation_button(data, calculated, memory)

# Enable the Downloadlink as soon as as CRIF has been put into memory
@app.callback(
    Output('Download IM Tree', 'href'),
    [Input('allocTree', 'data')])
def enableCrifDownload(data):
    return callbacks.enableDownload(data)

# Perform IM Allocation
@app.callback(Output('allocTree', 'data'),
              [Input('allocation_button', 'n_clicks')],
              [State('Crif', 'data')])
def allocate_im(n_clicks, crif):
    return callbacks.allocate_im(crif)

# After allocation has been done show the Standalone and Euler Allocation cards
@app.callback(Output('eulerCard', 'className'),
              [Input('allocTree', 'data'),
               Input('currentCrifInMemory', 'data')],
              [State('currentCrifCalculated', 'data'),
               State('eulerCard', 'className')])
def hide_eulerCard(data, memory, calculated, className):
    return callbacks.show_allocation_card(data, memory, calculated, className)

@app.callback(Output('standaloneCard', 'className'),
              [Input('allocTree', 'data'),
               Input('currentCrifInMemory', 'data')],
              [State('currentCrifCalculated', 'data'),
               State('standaloneCard', 'className')])
def hide_standaloneCard(data, memory, calculated, className):
    return callbacks.show_allocation_card(data, memory, calculated, className)

# When Node is clicked save the ID of the currently selected Node
@app.callback(
    Output('selectedNode', 'data'),
    [Input('IMTree', 'clickData')])
def save_node_id(clickData):
    return callbacks.save_node_id(clickData)

# When new node is selected display the currently selected node in the Allocation Nav Bar
@app.callback(Output('treeNavContent', 'children'),
              [Input('selectedNode', 'data')],
              [State('allocTree', 'data')])
def update_tree_NavContent(node, alloc):
    return callbacks.update_tree_NavContent(node, alloc)

# When a new node is selected, create the Treemap Color Scheme
@app.callback(Output('treeMapColors', 'data'),
              [Input('selectedNode', 'data')],
              [State('allocTree', 'data')])
def create_treemap_color_scheme(selectedNode, allocTree):
    return callbacks.create_treemap_color_scheme(selectedNode, allocTree)

# When a new node is selected load the appropriate Standalone Allocation
@app.callback(Output('TreeMapStandalone', 'figure'),
              [Input('treeMapColors', 'data')],
              [State('allocTree', 'data'),
               State('selectedNode', 'data')])
def create_standalone_treemap(treeMapColors, allocTree, selectedNode):
    return callbacks.create_standalone_treemap(selectedNode, allocTree, treeMapColors)

# When a new node is selected load the appropriate positive Euler Allocation
@app.callback(Output('TreeMapEulerPositive', 'figure'),
              [Input('treeMapColors', 'data')],
              [State('allocTree', 'data'),
               State('selectedNode', 'data')])
def create_euler_positive_treemap(treeMapColors, allocTree, selectedNode):
    return callbacks.create_euler_positive_treemap(selectedNode, allocTree, treeMapColors)

# When a new node is selected load the appropriate negative Euler Allocation
@app.callback(Output('TreeMapEulerNegative', 'figure'),
              [Input('treeMapColors', 'data')],
              [State('allocTree', 'data'),
               State('selectedNode', 'data')])
def create_euler_negative_treemap(treeMapColors, allocTree, selectedNode):
    return callbacks.create_euler_negative_treemap(selectedNode, allocTree, treeMapColors)

if __name__ == '__main__':
    app.run_server(debug=True)