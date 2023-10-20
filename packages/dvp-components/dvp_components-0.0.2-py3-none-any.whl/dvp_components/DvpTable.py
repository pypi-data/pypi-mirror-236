# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DvpTable(Component):
    """A DvpTable component.
An Ant Design Table component
See https://ant.design/components/table

Keyword arguments:

- id (string; optional):
    The ID used to identify this component.

- bordered (boolean; optional):
    Bordered.

- cellUpdateOptimize (boolean; default True):
    Whether to allow cell content rendering.

- className (string | dict; optional):
    CSS classes to be added to the component.

- columns (list of dicts; optional):
    Columns.

    `columns` is a list of dicts with keys:

    - align (a value equal to: 'left', 'center', 'right'; optional)

    - className (string; optional)

    - colSpan (number; optional)

    - colSpanRow (dict; optional)

    - dataIndex (string; required)

    - ellipsis (boolean | number | string | dict | list; optional)

    - filterResetToDefaultFilteredValue (boolean; optional)

    - filters (list; optional)

    - fixed (a value equal to: 'left', 'right'; optional)

    - group (string | list of strings; optional)

    - hidden (boolean; optional)

    - key (string; optional)

    - onCell (boolean | number | string | dict | list; optional)

    - render (boolean | number | string | dict | list; optional)

    - renderOptions (dict; optional)

        `renderOptions` is a dict with keys:

        - renderType (a value equal to: 'icon', 'link', 'node', 'checkbox', 'checkboxgroup', 'tag', 'tags', 'publication', 'radiogroup', 'rawhtml', 'icon-modal'; optional)

    - rotated (boolean; optional)

    - rowSpan (dict; optional)

    - search (boolean; optional)

    - sorter (boolean | number | string | dict | list; optional)

    - title (a list of or a singular dash component, string or number | string; required)

    - width (number | string; optional)

- data (list of dicts; optional):
    Column data.

    `data` is a list of dicts with strings as keys and values of type
    list of boolean | number | string | dict | lists | a list of or a
    singular dash component, string or number | string | number | dict
    with keys:

    - className (string; optional)

    - content (number

      Or string; optional) | dict with keys:

    - className (string; optional)

    - icon (string; optional)

    - id (string | dict; optional)

    - style (dict; optional) | dict with keys:

    - content (number | string; optional)

    - disabled (boolean; optional)

    - href (string; optional)

    - target (string; optional) | dict with keys:

    - abstract (string; optional)

    - collection (string; optional)

    - id (string; optional)

    - info (string; optional)

    - tagColor (string; optional)

    - title (string; optional) | dict with keys:

    - checked (boolean; optional)

    - className (string; optional)

    - content (number | string | a list of or a singular dash component, string or number; optional)

    - disabled (boolean; optional)

    - icon (dict; optional)

        `icon` is a dict with keys:

        - style (dict; optional)

    - id (string; optional)

    - labelMode (a value equal to: 'regular', 'button', 'icon'; optional) | dict with keys:

    - disabled (boolean; optional)

    - id (string; optional)

    - options (list of dicts; optional)

        `options` is a list of string | number | dict with keys:

        - disabled (boolean; optional)

        - label (a list of or a singular dash component, string or number; optional)

        - value (string | number; optional)s

    - value (string | number; optional) | dict with keys:

    - className (string; optional)

    - disabled (boolean; optional)

    - id (string; optional)

    - labelMode (a value equal to: 'regular', 'button'; optional)

    - options (list of dicts; optional)

        `options` is a list of string | number | dict with keys:

        - disabled (boolean; optional)

        - label (a list of or a singular dash component, string or number; optional)

        - value (string | number; optional)s

    - value (list of string | numbers; optional) | dict with keys:

    - bordered (boolean; optional)

    - color (string; optional)

    - content (number | string | a list of or a singular dash component, string or number; optional)

    - fullwidth (boolean; optional)

    - href (string; optional)

    - style (dict; optional) | list of dicts with keys:

    - bordered (boolean; optional)

    - color (string; optional)

    - content (number | string | a list of or a singular dash component, string or number; optional)

    - fullwidth (boolean; optional)

    - href (string; optional)

    - style (dict; optional)

- loadScript (list; optional):
    loadScript.

- loading_state (dict; optional):
    Loading state.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- maxHeight (number; optional):
    Set max height.

- maxWidth (number; optional):
    Set max width.

- pagination (dict; default {    defaultPageSize: 20,    hideOnSinglePage: True,    showSizeChanger: False,}):
    Config of pagination. You can ref table pagination config or full
    pagination document, hide it by setting it to False.

    `pagination` is a dict with keys:

    - current (number; optional)

    - disabled (boolean; optional)

    - hideOnSinglePage (boolean; optional)

    - pageSize (number; optional)

    - pageSizeOptions (list of numbers; optional)

    - position (a value equal to: 'topLeft', 'topCenter', 'topRight', 'bottomLeft', 'bottomCenter', 'bottomRight'; optional)

    - showQuickJumper (boolean; optional)

    - showSizeChanger (boolean; optional)

    - showTotal (boolean; optional)

    - showTotalPrefix (string; optional)

    - showTotalSuffix (string; optional)

    - simple (boolean; optional)

    - size (a value equal to: 'default', 'small'; optional)

    - total (number; optional) | boolean | dict

- pubURL (string; default ''):
    Publication URL, if render mode is publicatoin.

- selectedValues (list | dict | string | number; optional):
    Selected values.

- size (a value equal to: 'small', 'default', 'large'; default 'small'):
    Size.

- style (dict; optional):
    Inline CSS style."""
    _children_props = ['columns[].title']
    _base_nodes = ['children']
    _namespace = 'dvp_components'
    _type = 'DvpTable'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, columns=Component.UNDEFINED, data=Component.UNDEFINED, pubURL=Component.UNDEFINED, bordered=Component.UNDEFINED, maxHeight=Component.UNDEFINED, maxWidth=Component.UNDEFINED, size=Component.UNDEFINED, loadScript=Component.UNDEFINED, pagination=Component.UNDEFINED, cellUpdateOptimize=Component.UNDEFINED, selectedValues=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'bordered', 'cellUpdateOptimize', 'className', 'columns', 'data', 'loadScript', 'loading_state', 'maxHeight', 'maxWidth', 'pagination', 'pubURL', 'selectedValues', 'size', 'style']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'bordered', 'cellUpdateOptimize', 'className', 'columns', 'data', 'loadScript', 'loading_state', 'maxHeight', 'maxWidth', 'pagination', 'pubURL', 'selectedValues', 'size', 'style']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DvpTable, self).__init__(**args)
