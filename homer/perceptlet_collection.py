from __future__ import annotations
import random
from typing import Iterable

from .errors import MissingPerceptletError
from .perceptlet import Perceptlet
from .workspace_location import WorkspaceLocation


class PerceptletCollection:
    def __init__(self, perceptlets: Iterable[Perceptlet]):
        self.perceptlets = perceptlets
        self.perceptlets_by_location = None

    def at(self, location: WorkspaceLocation) -> PerceptletCollection:
        if self.perceptlets_by_location is None:
            self._arrange_perceptlets_by_location()
        return PerceptletCollection(
            self.perceptlets_by_location[location.i][location.j][location.k]
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
