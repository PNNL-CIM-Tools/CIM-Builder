# (superseded scratch note)

This file was an early, unstructured sketch of a matrix-based line-impedance
API (`PerLengthSequenceImpedanceBuilder.new_object()` /
`new_phase_impedance_data()`). It predates the real `ObjectBuilder` shape
(`cimbuilder/builders/base.py`, `BUILDER_API.md`) and used a different,
never-implemented API (methods called on the constructed object itself, string
values with embedded units).

The real use case — building an `ACLineSegment`'s per-phase impedance matrix —
is tracked as the Line/ACLineSegment phase in `OBJECT_BUILDER_MIGRATION.md`,
which is where a `LineBuilder.add_electrical(line, ...)` design should live
once written.
