from typing import List
from linguoplotter.structure_collections import StructureSet
from linguoplotter.structures.nodes import Concept


class CompoundConcept(Concept):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        root: Concept,
        args: List[Concept],
        child_spaces: StructureSet,
        possible_instances: StructureSet,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        is_slot: bool = False,
        reverse: Concept = None,
    ):
        Concept.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=root.name + "(" + ", ".join([arg.name for arg in args]) + ")",
            locations=[location for arg in args for location in arg.locations],
            classifier=type(root.classifier)(args),
            instance_type=args[0].instance_type,
            structure_type=args[0].structure_type,
            parent_space=args[0].parent_space,
            child_spaces=child_spaces,
            distance_function=root.distance_function,
            chunking_distance_function=root.chunking_distance_function,
            possible_instances=possible_instances,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            instances=instances,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
            depth=root.depth * sum(arg.depth for arg in args),
            distance_to_proximity_weight=root.distance_to_proximity_weight,
            is_slot=is_slot,
            reverse=reverse,
        )
        self.root = root
        self.args = args
        self.is_compound_concept = True

    @property
    def number_of_components(self):
        return (
            sum(arg.number_of_components for arg in self.args)
            + self.root.number_of_components
        )
