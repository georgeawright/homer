from typing import List

from linguoplotter.classifier import Classifier
from linguoplotter.tools import average_vector


class MagnitudeProximityClassifier(Classifier):
    def __init__(self, main_concepts: List["Concept"]):
        self.main_concept = main_concepts[0] if main_concepts is not None else None

    def classify(self, **kwargs: dict):
        """
        Required: 'concept'; 'start' OR 'collection'
        """
        collection = kwargs.get("collection")
        start = kwargs.get("start")
        concept = kwargs.get("concept")
        magnitude_concept = concept.root

        item = start if start is not None else collection.get()
        item_coordinates = average_vector(
            item.location_in_space(self.main_concept.parent_space).coordinates
        )[0]
        proximity_to_main_concept = self.main_concept.proximity_to(item)
        if magnitude_concept.relatives.where(name="more").not_empty:
            if item_coordinates > self.main_concept.location.coordinates[0][0]:
                magnitude_coordinates = [[1 - proximity_to_main_concept]]
            else:
                magnitude_coordinates = [[proximity_to_main_concept - 1]]
        elif magnitude_concept.relatives.where(name="less").not_empty:
            if item_coordinates > self.main_concept.location.coordinates[0][0]:
                magnitude_coordinates = [[1 - proximity_to_main_concept]]
            else:
                magnitude_coordinates = [[proximity_to_main_concept - 1]]
        else:
            return 0

        distance_from_magnitude_concept = magnitude_concept.distance_function(
            magnitude_concept.prototype, magnitude_coordinates
        )
        proximity_to_magnitude_concept = magnitude_concept._distance_to_proxmity(
            distance_from_magnitude_concept
        )
        return proximity_to_magnitude_concept
