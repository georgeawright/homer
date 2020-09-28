from __future__ import annotations
import random
from typing import List, Optional

from homer.errors import MissingPerceptletError
from homer.perceptlet_collection import PerceptletCollection


class NeighbourCollection(PerceptletCollection):
    def __init__(self, perceptlets: Optional[List] = None):
        if perceptlets is not None:
            PerceptletCollection.__init__(self, set(perceptlets))
        else:
            PerceptletCollection.__init__(self)
        self.perceptlets_list = perceptlets if perceptlets is not None else []

    def __eq__(self, other: NeighbourCollection) -> bool:
        return self.perceptlets_list == other.perceptlets_list

    def copy(self) -> NeighbourCollection:
        return NeighbourCollection([perceptlet for perceptlet in self.perceptlets_list])

    def at(self, location):
        raise NotImplementedError

    def add(self, perceptlet):
        self.perceptlets.add(perceptlet)
        self.perceptlets_list.append(perceptlet)

    def remove(self, perceptlet):
        self.perceptlets.remove(perceptlet)
        if perceptlet in self.perceptlets_list:
            self.perceptlets_list = [
                p for p in self.perceptlets_list if p != perceptlet
            ]

    @staticmethod
    def union(*collections: List[NeighbourCollection]) -> NeighbourCollection:
        return NeighbourCollection(
            [
                perceptlet
                for perceptlets_list in collections
                for perceptlet in perceptlets_list
            ]
        )

    @staticmethod
    def intersection(*collections: List[NeighbourCollection]):
        raise NotImplementedError

    def get_random(self):
        if len(self.perceptlets) < 1:
            raise MissingPerceptletError
        return random.sample(self.perceptlets_list, 1)[0]

    def _get_perceptlet_according_to(self, attribute: str):
        """Returns a perceptlet probabilistically according to attribute."""
        if len(self.perceptlets) < 1:
            raise MissingPerceptletError
        if len(self.perceptlets) == 1:
            return self.perceptlets_list[0]
        perceptlets = random.sample(
            self.perceptlets_list, len(self.perceptlets_list) // 2
        )
        perceptlet_choice = perceptlets[0]
        for perceptlet in perceptlets[1:]:
            if getattr(perceptlet, attribute) > getattr(perceptlet_choice, attribute):
                perceptlet_choice = perceptlet
        return perceptlet_choice
