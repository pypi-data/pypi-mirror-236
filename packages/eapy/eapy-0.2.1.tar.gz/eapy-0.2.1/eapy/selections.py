import random
import numpy as np
from . import baseclasses as bc
from .utils import get_rng


class TournamentSelection(bc.Selection):
    def __init__(self, n: int = 1, k: int = 2) -> None:
        self._n = n  # exchange_size
        self._k = k  # tournament size

    def select(
        self, members: list[bc.Member]
    ) -> tuple[list[bc.Member], list[bc.Member]]:
        members_to_reproduce = []
        members_to_delete = []
        for _ in range(self._n):
            competitors = random.sample(members, k=self._k)
            competitors.sort()
            members_to_reproduce.append(competitors[0])
            members_to_delete.append(competitors[-1])

        return members_to_reproduce, members_to_delete


class RankedSelection(bc.Selection):
    def __init__(self, n: int = 1) -> None:
        self._n = n  # exchange size

    def select(
        self, members: list[bc.Member]
    ) -> tuple[list[bc.Member], list[bc.Member]]:
        members.sort()
        return members[: self._n], members[-self._n :]


class ExpRankedSelection(bc.Selection):
    def __init__(self, n: int = 1, factor: float = 0.2) -> None:
        self._rng = get_rng()
        self._n = n  # exchange size
        self._factor = factor
        self._weights = None

    def select(
        self, members: list[bc.Member]
    ) -> tuple[list[bc.Member], list[bc.Member]]:
        # This seems redundant, but saves recalculating weights for the same sized population.
        if self._weights == None:
            self._weights = np.cumprod(1 / self._factor * np.ones(len(members)))
            self._weights /= np.sum(self._weights)
        members.sort()
        return (
            self._rng.choice(members, size=self._n, p=self._weights, replace=False),
            self._rng.choice(
                members, size=self._n, p=self._weights[::-1], replace=False
            ),
        )


class RouletteSelection(bc.Selection):
    def __init__(self, n: int = 1) -> None:
        self._rng = get_rng()
        self._n = n  # exchange size

    def select(
        self, members: list[bc.Member]
    ) -> tuple[list[bc.Member], list[bc.Member]]:
        fitnesses = np.array([member.fitness for member in members])
        fitnesses -= np.min(fitnesses)
        fitnesses /= np.sum(fitnesses)
        inverse_fitnesses = np.max(fitnesses) - fitnesses
        inverse_fitnesses /= np.sum(inverse_fitnesses)
        return (
            self._rng.choice(members, size=self._n, p=inverse_fitnesses),
            self._rng.choice(members, size=self._n, p=fitnesses),
        )


class RandomSelection(bc.Selection):
    def __init__(self, n: int = 1) -> None:
        self._rng = get_rng()
        self._n = n  # exchange size

    def select(
        self, members: list[bc.Member]
    ) -> tuple[list[bc.Member], list[bc.Member]]:
        choice = self._rng.choice(members, size=self._n * 2, replace=False)
        return choice[: self._n], choice[self._n :]


_SELECTIONS = [
    TournamentSelection,
    RankedSelection,
    ExpRankedSelection,
    RouletteSelection,
    RandomSelection,
]
