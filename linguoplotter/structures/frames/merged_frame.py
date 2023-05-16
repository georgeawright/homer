from linguoplotter.structures import Frame
from linguoplotter.structure_collections import StructureList, StructureSet


class MergedFrame(Frame):
    def __init__(
        self,
        structure_id: str,
        parent_id: str,
        name: str,
        parent_concept: "Concept",
        component_frames: StructureList,
        links_in: StructureSet,
        links_out: StructureSet,
        parent_spaces: StructureSet,
        instances: StructureSet,
        champion_labels: StructureSet,
        champion_relations: StructureSet,
        depth: int = None,
    ):
        Frame.__init__(
            self,
            structure_id=structure_id,
            parent_id=parent_id,
            name=name,
            parent_concept=parent_concept,
            parent_frame=None,
            sub_frames=None,
            concepts=None,
            interspatial_links=None,
            input_space=None,
            output_space=None,
            links_in=links_in,
            links_out=links_out,
            parent_spaces=parent_spaces,
            instances=instances,
            champion_labels=champion_labels,
            champion_relations=champion_relations,
            is_sub_frame=False,
            depth=depth,
        )
        self.component_frames = component_frames
        self.is_merged_frame = True

    def __dict__(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "name": self.name,
            "component_frames": [frame.structure_id for frame in self.component_frames],
            "activation": self.activation,
        }
