"""NetworkSession — thin holder for multi-substation network models."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cimbuilder.session.substation_session import SubstationSession

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim


@dataclass
class NetworkSession:
    """Holds a collection of SubstationSessions forming a multi-substation network.

    Attributes:
        substations: Ordered list of SubstationSessions added to this network.
    """
    substations: list[SubstationSession] = field(default_factory=list)

    def add_substation(self, session: SubstationSession) -> SubstationSession:
        """Register a SubstationSession with this network.

        Args:
            session: An already-constructed SubstationSession.

        Returns:
            The same session (for chaining).
        """
        self.substations.append(session)
        return session

    def get_substation(self, name: str) -> SubstationSession | None:
        """Return the SubstationSession whose substation.name matches ``name``."""
        for s in self.substations:
            if s.substation.name == name:
                return s
        return None

    def upload_all(self) -> None:
        """Upload every substation network."""
        for s in self.substations:
            s.upload()
