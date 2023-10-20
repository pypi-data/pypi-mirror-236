# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpSpin(Component):
    """A DvpSpin component.
An Ant Design Spin component
See https://ant.design/components/spin

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The content of the tab - will only be displayed if this tab is
    selected.

- id (string; optional):
    ID of the component.

- className (string | dict; optional):
    CSS classname.

- debug (boolean; default False):
    Debug.

- delay (number; optional):
    Delay.

- excludeProps (list of strings; optional):
    Exclude props.

- includeProps (list of strings; optional):
    Include props.

- indicator (a list of or a singular dash component, string or number; optional):
    Indicator.

- key (string; optional)

- listenPropsMode (a value equal to: 'default', 'exclude', 'include'; default 'default'):
    listen Props Mode.

- loading_state (dict; optional):
    Loading state.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- size (a value equal to: 'small', 'middle', 'large'; default 'middle'):
    Size.

- spinning (boolean; default False):
    Spinning.

- style (dict; optional):
    CSS style.

- text (string; optional):
    Text.

- wrapperClassName (string | dict; optional):
    Wrapper classname."""
    _children_props = ['indicator']
    _base_nodes = ['indicator', 'children']
    _namespace = 'dvp_components'
    _type = 'DvpSpin'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, className=Component.UNDEFINED, wrapperClassName=Component.UNDEFINED, style=Component.UNDEFINED, key=Component.UNDEFINED, spinning=Component.UNDEFINED, size=Component.UNDEFINED, delay=Component.UNDEFINED, text=Component.UNDEFINED, debug=Component.UNDEFINED, listenPropsMode=Component.UNDEFINED, excludeProps=Component.UNDEFINED, includeProps=Component.UNDEFINED, indicator=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'className', 'debug', 'delay', 'excludeProps', 'includeProps', 'indicator', 'key', 'listenPropsMode', 'loading_state', 'size', 'spinning', 'style', 'text', 'wrapperClassName']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'className', 'debug', 'delay', 'excludeProps', 'includeProps', 'indicator', 'key', 'listenPropsMode', 'loading_state', 'size', 'spinning', 'style', 'text', 'wrapperClassName']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        super(DvpSpin, self).__init__(children=children, **args)
