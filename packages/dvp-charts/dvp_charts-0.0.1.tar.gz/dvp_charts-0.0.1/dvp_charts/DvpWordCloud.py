# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpWordCloud(Component):
    """A DvpWordCloud component.
Ant Design word cloud

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string | dict; optional):
    CSS classes to be added to the component.

- colorField (string; optional):
    colorField.

- data (list; optional):
    Data.

- fontSize (list of numbers; default [24, 80]):
    Range of font size.

- queryURL (string; default 'https://www.google.com/search?q='):
    Query url.

- style (dict; optional):
    Inline CSS style.

- weightField (string; optional):
    weightField.

- wordField (string; optional):
    wordField."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dvp_charts'
    _type = 'DvpWordCloud'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, wordField=Component.UNDEFINED, colorField=Component.UNDEFINED, weightField=Component.UNDEFINED, fontSize=Component.UNDEFINED, queryURL=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'colorField', 'data', 'fontSize', 'queryURL', 'style', 'weightField', 'wordField']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'colorField', 'data', 'fontSize', 'queryURL', 'style', 'weightField', 'wordField']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpWordCloud, self).__init__(**args)
