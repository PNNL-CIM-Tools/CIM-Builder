"""Phase 3: NameIndex - name -> object, scoped per class (design: CIMTBL_DESIGN.md §5.5).

Scoped per-class rather than globally by design: two different CIM classes
can legitimately share a name (e.g. a bus and a switch both named 'sw1' in
different tables) - "arguably sloppy, but matches how power engineers think."
"""

from dataclasses import dataclass, field


@dataclass
class NameIndex:
    by_class: dict[type, dict[str, object]] = field(default_factory=dict)

    def add(self, obj: object) -> None:
        """Bind obj under (type(obj), obj.name). Re-adding the same object is
        a no-op; a different object claiming an already-used name raises -
        that's a real modeling error, not a NameIndex bug."""
        by_name = self.by_class.setdefault(type(obj), {})
        existing = by_name.get(obj.name)
        if existing is not None and existing.identifier != obj.identifier:
            raise ValueError(
                f"duplicate name {obj.name!r} for {type(obj).__name__} "
                f"(already bound to a different object)"
            )
        by_name[obj.name] = obj

    def get(self, cim_cls: type, name: str) -> object | None:
        """O(1) lookup; None if no object of cim_cls is bound to name."""
        return self.by_class.get(cim_cls, {}).get(name)
