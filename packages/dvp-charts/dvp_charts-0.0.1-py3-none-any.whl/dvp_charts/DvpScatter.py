# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpScatter(Component):
    """A DvpScatter component.
Ant Design word cloud

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- chartTitle (string; optional):
    Chart title.

- chartTitleStyle (dict; optional):
    Style of chart tile.

- className (string | dict; optional):
    CSS classes to be added to the component.

- data (list; optional):
    Data.

- groupbyField (string; optional):
    Group by field.

- hideXaxis (boolean; optional):
    Whether to hide x axis.

- hideYaxis (boolean; optional):
    Whether to hide y axis.

- legendDirection (a value equal to: 'horizontal', 'vertical'; default 'vertical'):
    Legend direction.

- legendPosition (a value equal to: 'top', 'top-left', 'top-right', 'left', 'left-top', 'left-bottom', 'right', 'right-top', 'right-bottom', 'bottom', 'bottom-left', 'bottom-right'; default 'right'):
    Legend position.

- lineDicts (list of dicts; optional):
    Dicts of regression lines.

- padding (list of numbers; optional):
    Padding.

- size (number | list; default 3):
    Size or size range.

- sizeField (string; optional):
    Size field.

- style (dict; optional):
    Inline CSS style.

- xAxisTitle (string; optional):
    X axis title.

- xField (string; optional):
    X axis.

- yAxisTitle (string; optional):
    Y axis title.

- yField (string; optional):
    X axis."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dvp_charts'
    _type = 'DvpScatter'
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, id=Component.UNDEFINED, xAxisTitle=Component.UNDEFINED, yAxisTitle=Component.UNDEFINED, sizeField=Component.UNDEFINED, size=Component.UNDEFINED, hideXaxis=Component.UNDEFINED, hideYaxis=Component.UNDEFINED, padding=Component.UNDEFINED, legendPosition=Component.UNDEFINED, legendDirection=Component.UNDEFINED, lineDicts=Component.UNDEFINED, chartTitle=Component.UNDEFINED, chartTitleStyle=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'chartTitle', 'chartTitleStyle', 'className', 'data', 'groupbyField', 'hideXaxis', 'hideYaxis', 'legendDirection', 'legendPosition', 'lineDicts', 'padding', 'size', 'sizeField', 'style', 'xAxisTitle', 'xField', 'yAxisTitle', 'yField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartTitle', 'chartTitleStyle', 'className', 'data', 'groupbyField', 'hideXaxis', 'hideYaxis', 'legendDirection', 'legendPosition', 'lineDicts', 'padding', 'size', 'sizeField', 'style', 'xAxisTitle', 'xField', 'yAxisTitle', 'yField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpScatter, self).__init__(**args)
