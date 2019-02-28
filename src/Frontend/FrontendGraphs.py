import igraph
from igraph import *

import plotly.plotly as py
import plotly
plotly.tools.set_credentials_file(username='Hellvetia', api_key='jTDeo4nFrMbqn7Fr7339')
import plotly.graph_objs as go

def create_tree_graph(df):

    def create_edges(df):
        df_non_alloc = df[(df.AllocationType == 'None') & (df.parentIdentifier != '')]
        edges = []
        for index, row in df_non_alloc.iterrows():
            edges.append((int(row.identifier), int(row.parentIdentifier)))
        return edges

    def create_labels(df):
        df_non_alloc = df[(df.AllocationType == 'None')]
        labels = []
        for index, row in df_non_alloc.iterrows():
            labels.append(row[df_non_alloc.columns[row.Level]] + ' ' + '{0:,.2f}'.format(row.ExposureAmount))
        return labels

    nodeCount = df.shape[0]
    edges = create_edges(df)
    g=Graph(edges=edges)
    lay=g.layout_reingold_tilford(root=[0])
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
                      mode='markers+text',
                      name='',
                      marker=dict(symbol='circle',
                                size=18,
                                color='#6175c1',
                                line=dict(color='rgb(50,50,50)', width=1)
                                ),
                      text=labels,
                      textposition='top center',
                      hoverinfo='text',
                      hovertext='Click to Filter',
                      opacity=1
                      )

    axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                )

    def make_annotations(pos, text, font_size=10, font_color='rgb(250,250,250)'):
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
                    text =''
                )
            )

        return dictList

    layout = dict(title='Initial Margin Tree of selected counterparty',
                  # annotations=make_annotations(position, labels),
                  font=dict(size=12),
                  showlegend=False,
                  xaxis=go.layout.XAxis(axis),
                  yaxis=go.layout.YAxis(axis),
                  margin=dict(l=40, r=40, b=85, t=100),
                  hovermode='closest',
                  plot_bgcolor='white'
                  )

    fig = dict(data=[lines, dots], layout=layout)
    fig['layout'].update(annotations=make_annotations(position, labels))
    asdf =1
    return {
        'data' : fig['data'],
        'layout':fig['layout']
    }
    # py.plot(fig, filename='IMTreeTests')