# Bug: CIMTool export flattens ~34 unrelated `.value` attributes onto an unrelated class

> **Status:** CIM-Builder no longer consumes the LinkML export, so this repo is not
> affected (validation reflects on the installed profile - `PROFILE_RESOLUTION.md`).
> Kept as the record of the upstream CIMTool bug.

**Where:** upstream CIMTool XSLT (OWL → LinkML export pipeline that produces
`cimbuilder/dsl/schema/cimhub_2026.linkml.yaml`). Not fixable in the generated
YAML itself — every regeneration reproduces it.

## Symptom

The generated LinkML schema contains one class with ~34-37 attributes, every
one of them literally named `value`, differing only by `slot_uri` /
`annotations.ea_guid` / `range`:

```yaml
attributes:
  ...
  value:
    annotations:
      ea_guid: "EAID_133597D7_9050_4335_B968_86AF7E16558C"
    slot_uri: cim:ActivePower.value
    range: float
    minimum_cardinality: 0
    maximum_cardinality: 1
  value:
    annotations:
      ea_guid: "EAID_9AC71195_FE05_4022_805D_524DFF496593"
    slot_uri: cim:ActivePowerChangeRate.value
    range: float
    minimum_cardinality: 0
    maximum_cardinality: 1
  # ...and ~32-35 more, one per CIM primitive-quantity type
  # (Resistance, Reactance, Voltage, Money, PU, PerCent, Length, ...)
```

Each entry's `slot_uri` is `cim:<SomeUnrelatedPrimitiveType>.value` — i.e. the
export is pulling in the `.value` slot from ~35 unrelated CIM primitive
wrapper types (`ActivePower`, `Resistance`, `Voltage`, `Money`, `PU`, ...) and
attaching all of them, under the same literal YAML key `value`, onto whatever
class happens to occupy that position in the source model.

Plain PyYAML silently keeps the last one and hides the bug. LinkML's loader
(`DupCheckYamlLoader`) correctly rejects it:

```
ValueError: Duplicate key: "value"
```

This is a hard failure that blocks loading the **entire** schema file (all
~450 classes), not just the offending class.

## It moves, it doesn't go away

Deleting the affected class from the OWL source does **not** fix the bug — it
relocates to whichever class ends up adjacent in that part of the model:

1. First regeneration: bug on `WireTemplate`.
2. `WireTemplate` deleted from OWL source, regenerated: bug reappeared
   identically (same 34 `ea_guid`s, same `slot_uri`s) on `WireSpacingInfo`.

This means the root cause is **not** "this one class has bad attributes" —
it's an incomplete or unnamed association/relationship in the source OWL that
the XSLT mis-resolves as "attach every primitive type's `.value` slot here,"
and whatever class sits in that structural position in the model inherits the
bug. Deleting the current victim class just moves the association's landing
site to its neighbor.

## Likely root cause (for whoever fixes the XSLT)

Look for an association in the OWL/UML source, near wire-info/wire-template
classes, that:
- has no distinct role name at one or both ends (or an ambiguous/inherited
  one), and
- is (or resembles) a generic "value holder" / datatype-wrapper association
  meant to express "this class can carry a value of any one of these CIM
  primitive quantity types."

The XSLT is likely iterating all CIM types that match some pattern (e.g. every
type with `cim_data_type: true`, i.e. every `<Foo>.value`-bearing primitive
wrapper) and emitting one `value:` attribute per match onto the class at the
association's un-role-named end, instead of either (a) skipping association
ends without a distinct role name, or (b) qualifying each generated attribute
name (e.g. `value_ActivePower`, `value_Resistance`, ...).

## Local workaround (applied, not a real fix)

Since this is regenerated wholesale from the OWL and any local patch to
`cimhub_2026.linkml.yaml` is wiped on the next export, the working pattern for
now is: after each regeneration, delete the entire stray `value:` block
(currently landing on `WireSpacingInfo`) plus its dangling reciprocal
reference (`PerLengthImpedance.WireAssemblyInfo`, which points at whatever
class most recently hosted the bug, e.g. `range: WireTemplate` after that
class was deleted — `SchemaView` tolerates a dangling range, `gen-python`
does not and needs it removed too).

This is a stopgap. It does not survive a regeneration and should be dropped
once the XSLT is fixed at the source.

## Real fix (for the agent working the XSLT)

Fix the export so the offending association either:
- is skipped (if it has no valid/distinct role name at the relevant end), or
- generates uniquely-named attributes (e.g. `value_<TypeName>`) if the
  one-value-per-primitive-type behavior is actually intentional somewhere in
  CIM, or
- is corrected in the OWL source if it's simply a modeling mistake (most
  likely, given it produces ~34 meaningless attributes with no real semantic
  role name).

Confirm the fix by checking that a regenerated `cimhub_2026.linkml.yaml`
loads via `linkml_runtime.utils.schemaview.SchemaView(...)` with no
"Duplicate key" error, and that `uv run gen-python cimhub_2026.linkml.yaml`
completes with no "unrecognized range" error.
