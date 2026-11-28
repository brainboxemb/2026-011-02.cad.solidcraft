This model reproduces the **default SolidCraft Sheet Metal Bracket** through
Forge's native sheet-metal API.

It is deliberately not remodelled as ordinary solid geometry. The useful test
is that the saved design keeps native sheet history:

- one active `Steel 2mm` rule;
- base sheet from the original XY sketch;
- two native edge-flange features;
- one native hem;
- recoverable flat-pattern semantics.

The hem does not pass an explicit `gap=` override. This intentionally tests
that SolidCraft's active sheet rule supplies its default hem clearance.
