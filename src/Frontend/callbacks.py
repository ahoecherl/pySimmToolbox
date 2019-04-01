import base64
import io
import CRIF.CrifUtil
import pandas as pd
import json
import dash_core_components as dcc
import dash_html_components as html
import urllib

from dash.exceptions import PreventUpdate
from CRIF.Crif import Crif
from Calculation.StandardCalculation import StandardCalculation
from Calculation.EulerAllocation import EulerAllocation
from Calculation.StandaloneAllocation import StandaloneAllocation
from Frontend.FrontendDataFiltering import *
from Frontend.FrontendGraphs import *

def fill_CrifsStorage(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = CRIF.CrifUtil.read_csv(
            io.StringIO(decoded.decode('utf-8'))
        )
        json = df.to_json()
        return json

def initial_load_select_counterparty(data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    Cps = df.IMLedis.unique()
    options_dicts = [{'label':cp, 'value':cp} for cp in Cps]
    return options_dicts

def make_crif_select_card_orange(data, className):
    if data is None:
        raise PreventUpdate
    className=str.replace(className, 'z-depth-0', 'z-depth-3')
    return str.replace(className, 'white', 'd-fine-orange')

def make_crif_select_card_text_white(data, className):
    if data is None:
        raise PreventUpdate
    return str.replace(className, 'grey-text', 'white-text')

def make_label_white(data, className):
    if data is None:
        raise PreventUpdate
    if className is None:
        className = ''
    return className+' white-text'

def initial_select(options):
    if options is not None:
        return options[0]['value']

def initial_load_select_direction(value, data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    df = df[df.IMLedis==value]
    df.reset_index(drop=True, inplace=True)
    onlyPost = False
    onlyCollect = False
    if df.CollectRegulations.unique().size == 1 and df.CollectRegulations[0] == '':
        onlyPost = True
    if df.PostRegulations.unique().size == 1 and df.PostRegulations[0] == '':
        onlyCollect = True
    if onlyPost:
        return [{'label': 'post', 'value': 'post'}]
    elif onlyCollect:
        return [{'label': 'collect', 'value': 'collect'}]
    else:
        return [{'label': 'collect', 'value': 'collect'},
                {'label': 'post', 'value': 'post'}]

def initial_load_select_regulations(direction, counterparty, data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    if direction == 'post':
        df = df[(df.IMLedis==counterparty) & (df.CollectRegulations=='')]
        regs = df.PostRegulations.unique()
    else:
        df = df[(df.IMLedis==counterparty) & (df.PostRegulations=='')]
        regs = df.CollectRegulations.unique()
    options_dicts = [{'label': reg, 'value': reg} for reg in regs]
    return options_dicts

def load_single_crif_in_memory(n_clicks, counterparty, direction, regulation, data):
    if data is None:
        raise PreventUpdate
    df = pd.read_json(data)
    if direction == 'post':
        dfone = df[(df.IMLedis==counterparty) & (df.PostRegulations==regulation)]
    else:
        dfone = df[(df.IMLedis==counterparty) & (df.CollectRegulations==regulation)]
    json = dfone.to_json()
    return json

def disable_calculate_im_button(crifCalculated, crifInMemory):
    if crifInMemory is None and crifCalculated is None:
        raise PreventUpdate
    if crifInMemory is not None and crifCalculated is None:
        return False
    if crifInMemory != crifCalculated:
        return False
    else:
        return True

def store_identifier_of_crif_in_memory(data, counterparty, direction, regulation):
    asDict = {'counterparty': counterparty,
              'direction': direction,
              'regulation': regulation}
    return json.dumps(asDict)

def disable_load_crif_button(regulation, crif_in_memory_identifier, counterparty, direction):
    if crif_in_memory_identifier is None:
        return False
    crif_in_memory_identifier = json.loads(crif_in_memory_identifier)
    if (crif_in_memory_identifier['regulation'] == regulation) and (crif_in_memory_identifier['counterparty'] == counterparty) and (crif_in_memory_identifier['direction'] == direction):
        return True
    return False

def calculate_IM(crif):
    if crif is None:
        raise PreventUpdate
    crif = Crif(pd.read_json(crif))
    imTree = StandardCalculation.calculate(crif)
    return imTree.toDataFrame().to_json()

def set_current_crif_calculated(data):
    return data

def show_calculated_im_element(data, currentCrifInMemory, currentCrifCalculated, className):
    if data is None:
        raise PreventUpdate
    if currentCrifInMemory == currentCrifCalculated:
        return str.replace(className, ' hide', '')
    if currentCrifInMemory != currentCrifCalculated:
        return className + ' hide'

def generate_IMTree(data):
    if data is None:
        raise PreventUpdate
    return create_tree_graph(pd.read_json(data))

def create_crifs_information(filename, data):
    if data is None:
        raise PreventUpdate
    data = pd.read_json(data)
    crifCount = len(data[['IMLedis', 'CollectRegulations', 'PostRegulations']].drop_duplicates().index)
    rowcount = len(data.index)
    cpCount = len(data[['IMLedis']].drop_duplicates().index)
    div = html.Div([html.Span(['Uploaded File',
                              html.Strong(' ' + filename)],
                                       className='card-title'),
        html.Ul([
            html.Li(['The file contains ',
                     html.Strong(str(rowcount)),
                     ' rows.']),
            html.Li(['The file contains ',
                     html.Strong(str(crifCount)+ ' CRIFs '),
                     'of ',
                     html.Strong(str(cpCount)+' Counterparties'),
                     '.'])
        ])
    ])
    return div

def enableDownload(data):
    if data is None:
        raise PreventUpdate
    data = pd.read_json(data)
    csv_string = data.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

def unhide_element(data, className):
    if data is None:
        raise PreventUpdate
    return str.replace(className, 'hide', '')

def disable_allocation_button(data, calculated, memory):
    if calculated is None:
        raise PreventUpdate
    if calculated==memory and data==json.dumps({'boolean':False}):
        return False
    else:
        return True

def set_treeComponentIndicator(n_clicks, memory, calculated):
    if calculated is None:
        raise PreventUpdate
    if calculated != memory:
        return json.dumps({'boolean': False})
    else:
        return json.dumps({'boolean': True})

def show_download_Tree_link(calculated, memory, className):
    if calculated == memory:
        return str.replace (className, 'hide', '')
    else:
        return className+' hide'

def show_allocation_card(data, memory, calculated, className):
    if data is None:
        PreventUpdate
    if calculated == memory:
        return str.replace (className, 'hide', '')
    else:
        return className+' hide'

def allocate_im(crif):
    if crif is None:
        raise PreventUpdate
    crif = Crif(pd.read_json(crif))
    imTree = StandardCalculation.calculate(crif)
    imTree = EulerAllocation.calculate(imTree)
    imTree = StandaloneAllocation.calculate(imTree)
    imTree = imTree.toDataFrame()
    return imTree.to_json()

def set_crif_in_memory_title(data):
    dict = json.loads(data)
    return str(dict['counterparty'])+' '+str(dict['direction'])+' '+str(dict['regulation'])

def show_trade_count(crif):
    crif = pd.read_json(crif)
    tradeCount = len(crif.tradeId.unique())
    return str(tradeCount) + ' ' + 'Trades'

def show_row_count(crif):
    crif = pd.read_json(crif)
    rowCount = len(crif.index)
    return str(rowCount) + ' ' + 'Rows'

def show_schedule_count(crif):
    crif = pd.read_json(crif)
    scheduleCount = len(crif[crif.IMModel == 'Schedule'].tradeId.unique())
    return str(scheduleCount) + ' ' + 'Schedule Trades'

def show_IM(imTree):
    if imTree is None:
        raise PreventUpdate
    im = getIM(pd.read_json(imTree))
    return ['{:,.2f}'.format(im), ' USD', html.Br(), 'Initial Margin']

def save_node_id(clickData):
    if clickData is None:
        raise PreventUpdate
    return json.dumps(clickData['points'][0]['pointNumber'])

def update_tree_NavContent(node, alloc):
    if alloc is None:
        raise PreventUpdate
    alloc = pd.read_json(alloc)
    row = alloc[(alloc.identifier == int(node)) & (alloc.AllocationType == 'None')].squeeze()
    children = []
    if row[0] <= 4:
        startlevel = 1
    else:
        startlevel = row[0]-3
        children.append(html.A(children='...', className='breadcrumb', href='#!'))
    for i in range(startlevel, row[0]+1):
        Header = row.index[i]
        Label = row[i]
        children.append(html.A(children=[str(Label)], className='breadcrumb', href='#!'))
    return children

def create_standalone_treemap(selectedNode, allocTree, treeMapColors):
    if allocTree is None or treeMapColors is None:
        return PreventUpdate
    allocTree = pd.read_json(allocTree)
    treeMapColors = pd.read_json(treeMapColors)
    standaloneSeries = getNodeStandaloneAlloc(allocTree, selectedNode)
    return create_tree_map(standaloneSeries, 'Standalone Allocation', treeMapColors)

def create_euler_positive_treemap(selectedNode, allocTree, treeMapColors):
    if allocTree is None or treeMapColors is None:
        return PreventUpdate
    allocTree = pd.read_json(allocTree)
    treeMapColors = pd.read_json(treeMapColors)
    eulerPosSeries= getNodeEulerPosAlloc(allocTree, selectedNode)
    return create_tree_map(eulerPosSeries, 'Positive Euler Allocation', treeMapColors)

def create_euler_negative_treemap(selectedNode, allocTree, treeMapColors):
    if allocTree is None or treeMapColors is None:
        return PreventUpdate
    allocTree = pd.read_json(allocTree)
    treeMapColors = pd.read_json(treeMapColors)
    eulerPosSeries= getNodeEulerNegAlloc(allocTree, selectedNode)
    return create_tree_map(eulerPosSeries, 'Negative Euler Allocation', treeMapColors, negative = True)

def create_treemap_color_scheme(selectedNode, allocTree):
    if allocTree is None:
        return PreventUpdate
    color_brewer = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9','#bc80bd', '#ccebc5', '#ffed6f']
    allocTree = pd.read_json(allocTree)
    standaloneSeries = getNodeStandaloneAlloc(allocTree, selectedNode)
    colorSize = len(color_brewer)
    colorNum = 0
    colorSeries = pd.Series()
    for index, value in standaloneSeries.iteritems():
        colorSeries = colorSeries.append(pd.Series(data=[color_brewer[colorNum]], index=[index]))
        colorNum = colorNum+1
        if colorNum >= colorSize:
            colorNum = 0
    return pd.DataFrame(colorSeries, columns=['color']).to_json()