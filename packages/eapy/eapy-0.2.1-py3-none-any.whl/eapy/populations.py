import math
from . import baseclasses as bc


class FlatPopulation(bc.Population):
    def populate(
        self, population_size: int, operator: bc.Operator, problem: bc.Problem
    ) -> None:
        self._populace = []
        for _ in range(population_size):
            new_member = operator.new_member(problem)
            new_member.fitness = problem.evaluate(new_member)
            self._populace.append(new_member)

    def advance(
        self, selection: bc.Selection, operator: bc.Operator, problem: bc.Problem
    ) -> int:
        members_to_reproduce, members_to_delete = selection.select(self._populace)

        # if callable(getattr(operator, "crossover", None)):
        #     partners_to_reproduce, _ = selection.select(self._populace)
        #     members_to_reproduce = [
        #         operator.crossover(member1, member2)
        #         for member1, member2 in zip(members_to_reproduce, partners_to_reproduce)
        #     ]

        for member in members_to_delete:
            self._populace.remove(member)

        for member in members_to_reproduce:
            new_member = operator.mutate(member, problem)
            new_member.fitness = problem.evaluate(new_member)
            self._populace.append(new_member)

        return len(members_to_reproduce)

    def insert_migrants(self, members: list[bc.Member]) -> None:
        insert_index = len(self._populace) - len(members)
        self._populace[insert_index:] = members[:]

    def get_migrants(self, emigrants_requested: int) -> list[bc.Member]:
        self._populace.sort()
        return self._populace[:emigrants_requested]

    @property
    def populace(self) -> list[bc.Member]:
        return self._populace


class SubDemePopulation(bc.Population):
    def populate(
        self,
        population_size: int,
        operator: bc.Operator,
        problem: bc.Problem,
        num_demes: int = 10,
    ) -> None:
        def check_is_power(value, base):
            return value == 1 if value < base else check_is_power(value // base, base)

        assert check_is_power(
            population_size, num_demes
        ), "size must be a power of the number of demes"

        if population_size == num_demes**2:
            self._demes = [FlatPopulation() for _ in range(num_demes)]
            for population in self._demes:
                population.populate(population_size // num_demes, operator, problem)
        else:
            self._demes = [SubDemePopulation() for _ in range(num_demes)]
            for population in self._demes:
                population.populate(
                    population_size // num_demes, operator, problem, num_demes
                )

    def advance(
        self, selection: bc.Selection, operator: bc.Operator, problem: bc.Problem
    ) -> int:
        return sum(
            [
                population.advance(selection, operator, problem)
                for population in self._demes
            ]
        )

    def insert_migrants(self, members: list[bc.Member]) -> None:
        for population in self._demes:
            next_migrants = population.get_migrants(len(members))
            population.insert_migrants(members)
            members = next_migrants

    def get_migrants(self, emigrants_requested: int) -> list[bc.Member]:
        return self._demes[-1].get_migrants(emigrants_requested)

    @property
    def populace(self) -> list[bc.Member]:
        return [member for population in self._demes for member in population.populace]


_POPULATIONS = [
    FlatPopulation,
    SubDemePopulation,
]
