# limits

Auto-rxn enforces limits on all control points for the duration of a reaction.
These limits exist to help enforce safety conditions during unattended reactions.
Like any software-based saftey feature, auto-rxn limits should be paired with hardware safety features such as runaway heater shutoff controllers.

If the limits are exceeded during a reaction, auto-rxn will set all devices to fallback positions and stop the reaction.

To set limits:

```bash
$ auto-rxn edit-limits
```

To view current limits:

```bash
$ auto-rxn list-devices
```

A copy of the limits as they were at the start of each reaction are stored in the `auto-rxn-data` directory.
It's important to note that this backup occurs immediately before the recipe runs since fallback positions can change over the course of a reaction.

Limits can always be numerical, including `+inf`, `-inf`, and (in some cases) `nan`.
Limits can sometimes be strings, for devices that accept string arguments to set (in a yaq context, daemons following [is-discrete](https://yeps.yaq.fyi/309/) trait).

## fallback

The setting for fallback is probably the most important for a given control point.
If any limit is exceeded for any control point, each control point will be set to its fallback position
A fallback of `nan` tells auto-rxn to leave that control point where it is during a fault.

Fallback can be set directly using `$ auto-rxn edit-limits`, or set during a recipe by appending `fallback_position` to the control point ID. For example, if your control point is furnace you could set the ID `furnace.fallback_position`.
Auto-rxn supports this feature because sometimes the ideal fallback positions are dependent on the step within the recipe.

## lower and upper

These are basic upper and lower limits.
Auto-rxn considers it a fault if these limits are exceeded by the set value or the proccess value.

## atol

Absolute tolerance.
Considered a fault if the difference between the PV and the SV has greater magnitude than atol setting.

## rtol

Relative tolerance.
Considered a fault if the difference between the PV and the SV has greater magnitude than rtol as a percentage of the SV.
Rtol can be useful if you want to allow a wider toleraence margin at higher set values and a tighter and lower set values.

If your device will be set to zero during the reaction, you have to set deadband if you're using rtol.
The ratio of difference to SV is a divide by zero error if SV equals zero.

## deadband

Allows for ignoring limit checks when both PV and SV are near zero.
If both PV and SV are within deadband of zero, all other checks are ignored.

## delay

Setting to allow limit overrides for a period of time.
If nonzero, limit checks must fail consistently several times before auto-rxn considers the device to be in fault.
Units of seconds.
Set delay to zero to trigger fault immediately when out of bounds.

