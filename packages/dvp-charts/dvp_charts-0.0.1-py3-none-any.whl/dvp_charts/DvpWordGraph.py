# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpWordGraph(Component):
    """A DvpWordGraph component.
Word network graph based on Echarts

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string | dict; optional):
    CSS classes to be added to the component.

- data (dict; optional):
    Data.

- draggable (boolean; default True):
    Draggable.

- force (dict; optional):
    Force.

- layoutType (string; default 'none'):
    Layout type.

- lineStyle (dict; default {    color: 'source',    curveness: 0.3,}):
    Line style.

- queryURL (string; default 'https://www.google.com/search?q='):
    Query url.

- style (dict; optional):
    Inline CSS style."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dvp_charts'
    _type = 'DvpWordGraph'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, className=Component.UNDEFINED, layoutType=Component.UNDEFINED, lineStyle=Component.UNDEFINED, force=Component.UNDEFINED, draggable=Component.UNDEFINED, queryURL=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'draggable', 'force', 'layoutType', 'lineStyle', 'queryURL', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'draggable', 'force', 'layoutType', 'lineStyle', 'queryURL', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpWordGraph, self).__init__(**args)
