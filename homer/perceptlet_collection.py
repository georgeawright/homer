from __future__ import annotations
import random
from typing import List, Set, Union

from .errors import MissingPerceptletError
from .perceptlet import Perceptlet
from .workspace_location import WorkspaceLocation


class PerceptletCollection:
    def __init__(self, perceptlets: Set[Perceptlet]):
        self.perceptlets = perceptlets
        self.perceptlets_by_location = None

    def at(self, location: WorkspaceLocation) -> PerceptletCollection:
        if self.perceptlets_by_location is None:
            self._arrange_perceptlets_by_location()
        return PerceptletCollection(
            self.perceptlets_by_location[location.i][location.j][location.k]
        )

    def add(self, perceptlet: Perceptlet):
        self.perceptlets.add(perceptlet)
        if self.perceptlets_by_location is not None:
            self._add_at_location(perceptlet, perceptlet.location)
            try:
                for member in perceptlet.member:
                    self._add_at_location(perceptlet, member.location)
            except AttributeError:
                pass

    def remove(self, perceptlet: Perceptlet):
        self.perceptlets.remove(perceptlet)
        if self.perceptlets_by_location is None:
            return
        for i, layer in enumerate(self.perceptlets_by_location):
            for j, row in enumerate(layer):
                for k, cell in enumerate(layer):
                    if perceptlet in cell:
                        self.perceptlets_by_location[i][j][k].remove(perceptlet)

    @staticmethod
    def union(*collections: List[PerceptletCollection]) -> PerceptletCollection:
        return PerceptletCollection(
            set.union(*[collection.perceptlets for collection in collections])
        )

    @staticmethod
    def intersection(*collections: List[PerceptletCollection]) -> PerceptletCollection:
        return PerceptletCollection(
            set.intersection(*[collection.perceptlets for collection in collections])
        )

    def get_random(self) -> Perceptlet:
        """Returns a random perceptlet"""
        return random.sample(self.perceptlets, 1)[0]

    def get_exigent(self) -> Perceptlet:
        """Returns a perceptlet probabilistically according to exigency."""
        return self._get_perceptlet_according_to("exigency")

    def get_important(self) -> Perceptlet:
        """Returns a perceptlet probabilistically according to importance."""
        return self._get_perceptlet_according_to("importance")

    def get_unhappy(self) -> Perceptlet:
        """Returns a perceptlet probabilistically according to unhappiness."""
        return self._get_perceptlet_according_to("unhappiness")

    def _add_at_location(
        self, perceptlet: Perceptlet, coordinates: List[Union[float, int]]
    ):

        loc = WorkspaceLocation.from_workspace_coordinates(coordinates)
        self.perceptlets_by_location[loc.i][loc.j][loc.k]

    def _get_perceptlet_according_to(self, attribute: str) -> Perceptlet:
        """Returns a perceptlet probabilistically according to attribute."""
        if len(self.perceptlets) < 1:
            raise MissingPerceptletError
        perceptlets = random.sample(self.perceptlets, len(self.perceptlets) // 2)
        perceptlet_choice = perceptlets[0]
        for perceptlet in perceptlets[1:]:
            if getattr(perceptlet, attribute) > getattr(perceptlet_choice, attribute):
                perceptlet_choice = perceptlet
        return perceptlet_choice

    def _arrange_perceptlets_by_location(self):
        self.perceptlets_by_location = [
            [
                [set() for _ in range(WorkspaceLocation.WIDTH)]
                for _ in range(WorkspaceLocation.HEIGHT)
            ]
            for _ in range(WorkspaceLocation.DEPTH)
        ]
        for perceptlet in self.perceptlets:
            loc = WorkspaceLocation.from_workspace_coordinates(perceptlet.location)
            self.perceptlets_by_location[loc.i][loc.j][loc.k].add(perceptlet)
