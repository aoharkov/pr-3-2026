"""Utilities for tracking and displaying Wikipedia link-chain traversals."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChainResult:
    """Immutable record of a completed chain traversal."""

    visited_titles: tuple[str, ...]
    visited_urls: tuple[str, ...]
    reason: str  # "cycle" | "dead_end" | "cutoff" | "got_to_philosophy"


class VisitTracker:
    """Tracks visited pages during a chain traversal."""

    def __init__(self) -> None:
        self._titles: list[str] = []
        self._urls: list[str] = []
        self._seen: set[str] = set()

    def add(self, title: str, url: str) -> None:
        """Record a page visit."""
        self._titles.append(title)
        self._urls.append(url)
        self._seen.add(title)

    def has_visited(self, title: str) -> bool:
        """Return True if *title* was already visited (O(1))."""
        return title in self._seen

    def __len__(self) -> int:
        return len(self._titles)

    def to_result(self, reason: str) -> ChainResult:
        """Snapshot current state into a frozen :class:`ChainResult`."""
        return ChainResult(
            visited_titles=tuple(self._titles),
            visited_urls=tuple(self._urls),
            reason=reason,
        )


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def print_step(step: int, title: str, url: str) -> None:
    """Print a single numbered step in the chain."""
    print(f"  {step:>3}. {title}  —  {url}")


def print_chain_result(result: ChainResult) -> None:
    """Print the summary block for a completed chain."""
    print("=" * 60)
    print(f"  Pages visited : {len(result.visited_titles)}")
    print(f"  Termination   : {result.reason}")
    print("=" * 60)
    print("\nFull chain:")
    for i, title in enumerate(result.visited_titles, 1):
        print(f"  {i:>3}. {title}")
