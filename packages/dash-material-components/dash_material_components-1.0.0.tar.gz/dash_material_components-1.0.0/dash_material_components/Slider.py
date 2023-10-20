# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Slider(Component):
    """A Slider component.
Slider component

Keyword arguments:

- id (string; default 'slider'):
    Used to identify dash components in callbacks.

- labelText (string; optional):
    Text to display above the slider form.

- marks (list of dicts; optional):
    Array of selection marks to display below the slider form.

    `marks` is a list of dicts with keys:

    - label (string; optional):
        Mark label.

    - value (number; optional):
        Mark value.

- maxValue (number; default 100):
    Maximum selection allowed in the slider.

- minValue (number; default 0):
    Minimum selection allowed in the slider.

- selected (number; default 50):
    Active slider selection.

- showInputText (boolean; default False):
    Enable input text.

- stepValue (number; default 10):
    Slider selection increment.

- width (string | number; default '100%'):
    Width of slider form."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_material_components'
    _type = 'Slider'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, labelText=Component.UNDEFINED, width=Component.UNDEFINED, maxValue=Component.UNDEFINED, minValue=Component.UNDEFINED, stepValue=Component.UNDEFINED, marks=Component.UNDEFINED, selected=Component.UNDEFINED, showInputText=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'labelText', 'marks', 'maxValue', 'minValue', 'selected', 'showInputText', 'stepValue', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'labelText', 'marks', 'maxValue', 'minValue', 'selected', 'showInputText', 'stepValue', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(Slider, self).__init__(**args)
