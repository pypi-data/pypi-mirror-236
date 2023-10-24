# AUTO GENERATED FILE - DO NOT EDIT

export ''_runcommand

"""
    ''_runcommand(;kwargs...)

A RunCommand component.
Use this component to run command using CAD
Keyword arguments:
- `id` (String; optional): Unique ID to identify this component in Dash callbacks.
- `command` (optional): Command to run

It can be a macro or command name of the host software
___________________________________
Available complex command for Rhino

View from sun
E.g.
```
{
    name: 'ViewFromSun'
    param: {
        target: {'x': 0, 'y': 0, 'z': 0, 'type': 'Point3D'},
        direction: {'x': -0.062823, 'y': 1.904328, 'z': -0.42219, 'type': 'Vector3D'},
        displayName: 'Shaded'
    }
}
```

Add directional light
E.g.
```
{
    name: 'SetRhinoDirectLight'
    param: {
        vectors: [{'x': -0.062823, 'y': 1.904328, 'z': -0.42219, 'type': 'Vector3D'}]
    }
}
```. command has the following type: String | lists containing elements 'name', 'param'.
Those elements have the following types:
  - `name` (String; required)
  - `param` (String; required)
- `hideButton` (Bool; optional): Show/hide button
- `prefix` (String; optional): Prefix of the label
- `trigger` (Bool | Real | String | Dict | Array; optional): External trigger
"""
function ''_runcommand(; kwargs...)
        available_props = Symbol[:id, :command, :hideButton, :prefix, :trigger]
        wild_props = Symbol[]
        return Component("''_runcommand", "RunCommand", "pollination_dash_io", available_props, wild_props; kwargs...)
end

