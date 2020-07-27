from typing import Callable, List, Optional, Union

from homer.concept import Concept


class CorrespondenceConcept(Concept):
    def __init__(
        self,
        name: str,
        affinity_calculation: Callable,
        depth: int = 1,
        activation: float = 0.0,
        space: Optional[Concept] = None,
        prototype: Optional[Union[List[int], List[float], str]] = None,
        boundary: Optional[Union[List[int], List[float]]] = None,
        distance_metric: Optional[Callable] = None,
    ):
        Concept.__init__(
            self,
            name,
            depth=depth,
            activation=activation,
            space=space,
            prototype=prototype,
            boundary=boundary,
            distance_metric=distance_metric,
        )
        self.affinity_calculation = affinity_calculation

    def calculate_affinity(self, number_of_same_labels: int, proximity: float):
        self.affinity_calculation(number_of_same_labels, proximity)
