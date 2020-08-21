from __future__ import annotations
import random
from typing import List, Optional, Set, Union

from .errors import MissingPerceptletError
from .workspace_location import WorkspaceLocation


class PerceptletCollection:
    def __init__(self, perceptlets: Optional[Set] = None):
        self.perceptlets = set() if perceptlets is None else perceptlets
        self.perceptlets_by_location = None

    def __len__(self):
        return len(self.perceptlets)

    def __eq__(self, other: PerceptletCollection) -> bool:
        if len(self) != len(other):
            return False
        for perceptlet in self:
            if perceptlet not in other:
                return False
        return True

    def __ne__(self, other: PerceptletCollection) -> bool:
        return not self == other

    def __iter__(self):
        return (perceptlet for perceptlet in self.perceptlets)

    def copy(self) -> PerceptletCollection:
        return PerceptletCollection({perceptlet for perceptlet in self.perceptlets})

    def at(self, location: WorkspaceLocation) -> PerceptletCollection:
        if self.perceptlets_by_location is None:
            self._arrange_perceptlets_by_location()
        return PerceptletCollection(
            self.perceptlets_by_location[location.i][location.j][location.k]
        )

    def add(self, perceptlet):
        self.perceptlets.add(perceptlet)
        if self.perceptlets_by_location is not None:
            self._add_at_location(perceptlet, perceptlet.location)
            if hasattr(perceptlet, "members"):
                for member in perceptlet.members:
                    self._add_at_location(perceptlet, member.location)

    def remove(self, perceptlet):
        self.perceptlets.remove(perceptlet)
        if self.perceptlets_by_location is None:
            return
        for i, layer in enumerate(self.perceptlets_by_location):
            for j, row in enumerate(layer):
                for k, cell in enumerate(row):
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

    def get_random(self):
        """Returns a random perceptlet"""
        if len(self.perceptlets) < 1:
            raise MissingPerceptletError
        return random.sample(self.perceptlets, 1)[0]

    def get_exigent(self):
        """Returns a perceptlet probabilistically according to exigency."""
        return self._get_perceptlet_according_to("exigency")

    def get_active(self):
        """Returns a perceptlet probabilistically according to activation."""
        return self._get_perceptlet_according_to("activation")

    def get_unhappy(self):
        """Returns a perceptlet probabilistically according to unhappiness."""
        return self._get_perceptlet_according_to("unhappiness")

    def _add_at_location(self, perceptlet, coordinates: List[Union[float, int]]):
        loc = WorkspaceLocation.from_workspace_coordinates(coordinates)
        self.perceptlets_by_location[loc.i][loc.j][loc.k].add(perceptlet)

    def _get_perceptlet_according_to(self, attribute: str):
        """Returns a perceptlet probabilistically according to attribute."""
        if len(self.perceptlets) < 1:
            raise MissingPerceptletError
        if len(self.perceptlets) == 1:
            return list(self.perceptlets)[0]
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
