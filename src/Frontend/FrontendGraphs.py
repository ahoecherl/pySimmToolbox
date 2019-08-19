import igraph
from igraph import *
import pandas as pd
import squarify

import plotly.plotly as py
import plotly
plotly.tools.set_credentials_file(username='Hellvetia', api_key='jTDeo4nFrMbqn7Fr7339')
import plotly.graph_objs as go

factor = 0.7 #Factor to quickly change size of output

def create_tree_graph(df):

    def create_edges(df):
        df_non_alloc = df[(df.AllocationType == 'None') & (df.parentIdentifier != '')]
        edges = []
        for index, row in df_non_alloc.iterrows():
            edges.append([int(row.parentIdentifier),int(row.identifier)])
        return edges

    def create_labels(df):
        df_non_alloc = df[(df.AllocationType == 'None')]
        df_non_alloc = df_non_alloc.sort_values(['identifier'], inplace=False)
        text = []
        hovertext = []
        color = []
        for index, row in df_non_alloc.iterrows():
            text.append(row[df_non_alloc.columns[row.Level]])
            hovertext.append('{0:,.2f}'.format(row.ExposureAmount))
            color.append(row.ExposureAmount)
            # labels.append(row[df_non_alloc.columns[row.Level]] + ' ' + '{0:,.2f}'.format(row.ExposureAmount))
        return {'text':text, 'hovertext':hovertext, 'color':color}

    nodeCount = df.shape[0]
    edges = create_edges(df)
    g=Graph(nodeCount,edges=edges)
    # g=Graph(edges=edges)
    # lay = g.layout('rt')
    lay=g.layout_reingold_tilford(root=[0])
    coordinates=pd.DataFrame(lay.coords)
    width = coordinates[0].unique().size
    height = coordinates[1].unique().size
    position = {k: lay[k] for k in range(nodeCount)}
    Y = [lay[k][1] for k in range(nodeCount)]
    M = max(Y)

    E = [e.tuple for e in g.es]

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2*M-position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]
    labels = create_labels(df)

    lines = go.Scatter(x=Xe,
                       y=Ye,
                       mode='lines',
                       line=dict(color='rgb(210,210,210)', width=1),
                       hoverinfo='none'
                       )
    dots = go.Scatter(x=Xn,
                      y=Yn,
                      mode='markers',
                      name='',
                      marker=dict(symbol='diamond-wide',
                                size=(60*factor),
                                color=labels['color'],
                                colorbar=dict(title='Colorbar', thickness = 10),
                                colorscale='Portland',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                      text=labels['hovertext'],
                      textposition='top center',
                      hoverinfo='text',
                      opacity=1
                      )

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    def make_annotations(pos, text, font_size=(10*factor), font_color='white'):
        L = len(pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        dictList = []
        for k in range(L):
            dictList.append(
                dict(
                    x=pos[k][0],
                    y=2 * M - position[k][1],
                    xref='x1',
                    yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False,
                    text='<b>'+labels['text'][k]+'</b>',
                    textposition = 'top center'
                )
            )

        return dictList

    layout = dict(
                  # annotations=make_annotations(position, labels),
                  font=dict(size=(12 * factor)),
                  showlegend=False,
                  xaxis=go.layout.XAxis(axis),
                  yaxis=go.layout.YAxis(axis),
                  height = (height*90) * factor,#height*50,
                  width = (200*factor+width*70) * factor,
                  margin=dict(l=0, r=0, b=0, t=0),
                  hovermode='closest',
                  plot_bgcolor='white',
                  )

    fig = dict(data=[lines, dots], layout=layout)
    fig['layout'].update(annotations=make_annotations(position, labels['text']))
    asdf =1
    return {
        'data' : fig['data'],
        'layout':fig['layout']
    }
    # py.plot(fig, filename='IMTreeTests')

def create_tree_map(series, title, treeMapColors, negative=False):
    hashtagThreshold = 0.03
    blankThreshold = 0.01

    x = 0.
    y = 0.
    width = 0.6
    height = 1

    if negative:
        series = series[series < 0]
        values=series.values*-1
    else:
        series = series[series > 0]
        values = series.values

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    df = pd.DataFrame(series, columns=['exposure'])
    df['percentage'] = df.exposure.values / df.exposure.sum()
    df['label'] = ''
    df['label'][df.percentage > hashtagThreshold] = df.index.to_series()[df.percentage > hashtagThreshold]
    df['number'] = df.reset_index().index.values + 1
    try:
        df['label'][(df.percentage < hashtagThreshold) & (df.percentage > blankThreshold)] = '#' + df.number[(df.percentage < hashtagThreshold) & (df.percentage > blankThreshold)].apply(str)
    except:
        pass

    labels = df['label'].values

    color_brewer = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']

    shapes = []
    annotations = []
    counter = 0
    label_counter = 0

    for r in rects:
        trade = series.index[counter]
        shapes.append(
            dict(
                type='rect',
                x0=r['x'],
                y0=r['y'],
                x1=r['x'] + r['dx'],
                y1=r['y'] + r['dy'],
                line=dict(width=2),
                fillcolor=treeMapColors.color[trade]
            )
        )
        annotations.append(
            dict(
                x=r['x'] + (r['dx'] / 2),
                y=r['y'] + (r['dy'] / 2),
                text=labels[label_counter],
                showarrow=False
            )
        )
        counter = counter + 1
        label_counter = label_counter + 1

    # For hover text
    trace0 = go.Scatter(
        x=[r['x'] + (r['dx'] / 2) for r in rects],
        y=[r['y'] + (r['dy'] / 2) for r in rects],
        text=[str(index + ': ' + '{0:,.2f}'.format(value)) for (index, value) in series.iteritems()],
        # text=[str(v) for v in values],
        mode='none',
        hoverinfo='text'
    )

    layout = dict(
        title=title,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=25
        )
    )

    # With hovertext
    figure = dict(data=[trace0], layout=layout)

    return figure