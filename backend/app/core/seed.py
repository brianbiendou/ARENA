"""Deterministic seed system for reproducible runs."""

from __future__ import annotations

import random
import time


class SeedManager:
    """Manages a seeded RNG for reproducible experiment runs."""

    def __init__(self, seed: int | None = None):
        self.seed = seed if seed is not None else int(time.time() * 1000) % (2**31)
        self._rng = random.Random(self.seed)

    def shuffle(self, items: list) -> list:
        """Return a shuffled copy of items."""
        copy = list(items)
        self._rng.shuffle(copy)
        return copy

    def choice(self, items: list):
        """Pick a random item."""
        return self._rng.choice(items)

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

    def random(self) -> float:
        return self._rng.random()

    def variation(self, value: int | float, pct: float = 0.05) -> float:
        """Apply ±pct% random variation to a value."""
        delta = value * pct
        return value + self._rng.uniform(-delta, delta)

    def next_seed(self) -> int:
        """Generate a derived seed (for batch runs)."""
        return self._rng.randint(0, 2**31 - 1)
