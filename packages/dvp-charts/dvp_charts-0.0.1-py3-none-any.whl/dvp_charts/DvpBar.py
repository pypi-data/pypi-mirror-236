# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpBar(Component):
    """A DvpBar component.
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

- colors (dict; optional):
    Dict of colors.

- data (list; optional):
    Data.

- direction (a value equal to: 'horizontal', 'vertical'; default 'horizontal'):
    Direction of the bar.

- groupbyField (string; optional):
    Group by field.

- hideLegend (boolean; optional):
    Whether to hide legend.

- hideXaxis (boolean; optional):
    Whether to hide x axis.

- hideXaxisTitle (boolean; optional):
    Whether to hide x axis title.

- hideYaxis (boolean; optional):
    Whether to hide y axis.

- hideYaxisTitle (boolean; optional):
    Whether to hide y axis title.

- isPercent (boolean; optional):
    100% percent mode.

- isStack (boolean; default True):
    Stack mode.

- labelField (string; optional):
    Field to show as label.

- labelPosition (a value equal to: 'left', 'middle', 'right'; default 'middle'):
    Position of label.

- legendPosition (a value equal to: 'top', 'top-left', 'top-right', 'left', 'left-top', 'left-bottom', 'right', 'right-top', 'right-bottom', 'bottom', 'bottom-left', 'bottom-right'; default 'right'):
    Legend position.

- padding (list of numbers; optional):
    Padding.

- style (dict; optional):
    Inline CSS style.

- subInfo (a list of or a singular dash component, string or number; optional):
    Sub info.

- xAxisTitle (string; optional):
    X axis title.

- xField (string; optional):
    X axis.

- yAxisTitle (string; optional):
    Y axis title.

- yField (string; optional):
    X axis."""
    _children_props = ['subInfo']
    _base_nodes = ['subInfo', 'children']
    _namespace = 'dvp_charts'
    _type = 'DvpBar'
    @_explicitize_args
    def __init__(self, data=Component.UNDEFINED, id=Component.UNDEFINED, colors=Component.UNDEFINED, labelPosition=Component.UNDEFINED, padding=Component.UNDEFINED, subInfo=Component.UNDEFINED, xAxisTitle=Component.UNDEFINED, yAxisTitle=Component.UNDEFINED, hideXaxis=Component.UNDEFINED, hideYaxis=Component.UNDEFINED, hideXaxisTitle=Component.UNDEFINED, hideYaxisTitle=Component.UNDEFINED, hideLegend=Component.UNDEFINED, isStack=Component.UNDEFINED, isPercent=Component.UNDEFINED, legendPosition=Component.UNDEFINED, chartTitle=Component.UNDEFINED, chartTitleStyle=Component.UNDEFINED, direction=Component.UNDEFINED, xField=Component.UNDEFINED, yField=Component.UNDEFINED, labelField=Component.UNDEFINED, groupbyField=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'chartTitle', 'chartTitleStyle', 'className', 'colors', 'data', 'direction', 'groupbyField', 'hideLegend', 'hideXaxis', 'hideXaxisTitle', 'hideYaxis', 'hideYaxisTitle', 'isPercent', 'isStack', 'labelField', 'labelPosition', 'legendPosition', 'padding', 'style', 'subInfo', 'xAxisTitle', 'xField', 'yAxisTitle', 'yField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'chartTitle', 'chartTitleStyle', 'className', 'colors', 'data', 'direction', 'groupbyField', 'hideLegend', 'hideXaxis', 'hideXaxisTitle', 'hideYaxis', 'hideYaxisTitle', 'isPercent', 'isStack', 'labelField', 'labelPosition', 'legendPosition', 'padding', 'style', 'subInfo', 'xAxisTitle', 'xField', 'yAxisTitle', 'yField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpBar, self).__init__(**args)
