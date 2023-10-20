from .DvpTemplate import *
from dash.development.base_component import Component
import plotly.express as px
from dash import dcc, html


def DvpHist(
    data=Component.UNDEFINED,
        column=Component.UNDEFINED,
        groupby=Component.UNDEFINED,
        name=Component.UNDEFINED,
        template='plotly_white+dmp',
        margin={'l': 20, 'r': 10, 't': 10, 'b': 10, 'pad': 5},
        marginal='box',
        xField=Component.UNDEFINED,
        groupbyField=None,
        labelFields=[],
        alias={},
        width=Component.UNDEFINED,
        height=Component.UNDEFINED,
        title=Component.UNDEFINED,
        xaxisTitle=None,
        yaxisTitle=None,
        category_orders=Component.UNDEFINED,
        chartTitle=Component.UNDEFINED,
        colorway=colorway):

    if not labelFields:
        labelFields = [x for x in [xField, groupbyField] if x]

    fig = px.histogram(
        data, x=xField, color=groupbyField, marginal=marginal,
        hover_data=labelFields, color_discrete_sequence=colorway,
        opacity=0.7, facet_row_spacing=0.05
    )

    fig.update_layout(
        template=template, margin=margin, autosize=True,
        plot_bgcolor='#eaf1f7'
    )

    if marginal == 'box':
        # fig.get_subplots(vertical_spacing=0.05)
        fig.update_traces(selector=dict(type='box'), boxpoints=False)

    if yaxisTitle:
        fig.update_yaxes(title=yaxisTitle, row=1, col=1)

    if xaxisTitle:
        fig.update_xaxes(title=xaxisTitle, row=1, col=1)
        hovertemplate = f'<i>{xaxisTitle}</i>:' + '%{x}' + '<extra></extra>'

    elif alias.get(xField):
        fig.update_xaxes(title=alias.get(xField), row=1, col=1)
        hovertemplate = f'<i>{alias.get(xField)}</i>:' + \
            '%{x}' + '<extra></extra>'

    else:
        hovertemplate = f'<i>{xField}</i>:' + '%{x}' + '<extra></extra>'

    fig.update_traces(
        hovertemplate=hovertemplate,
        selector=dict(type="histogram")
    )

    if groupbyField:
        fig.update_yaxes(autorange='reverse', row=0, col=1)
        fig.update_layout(legend_title_text='')

    if chartTitle:
        return html.Div(
            [
                html.Span(chartTitle, className='dvp-chart-title'),
                dcc.Graph(figure=fig, config=chart_config)
            ],
            className='dvp-hist-wrapper'
        )
    else:
        return dcc.Graph(figure=fig, config=chart_config)
