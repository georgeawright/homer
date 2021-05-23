from homer.bubble_chamber import BubbleChamber
from homer.codelets.builders import ViewBuilder
from homer.id import ID
from homer.location import Location
from homer.structure_collection import StructureCollection
from homer.structures.spaces import WorkingSpace
from homer.structures.views import SimplexView


class SimplexViewBuilder(ViewBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from homer.codelets.evaluators.view_evaluators import SimplexViewEvaluator

        return SimplexViewEvaluator

    @classmethod
    def make(cls, parent_id: str, bubble_chamber: BubbleChamber, urgency: float = None):
        target_one = bubble_chamber.spaces["input"]
        target_two = bubble_chamber.frames.where(
            parent_concept=bubble_chamber.concepts["text"]
        ).get_active()
        urgency = urgency if urgency is not None else target_two.activation
        return cls.spawn(
            parent_id,
            bubble_chamber,
            StructureCollection({target_one, target_two}),
            urgency,
        )

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view-simplex"]

    def _process_structure(self):
        view_id = ID.new(SimplexView)
        view_location = Location([], self.bubble_chamber.spaces["top level working"])
        input_spaces = StructureCollection(
            {
                self._instantiate_frame(space) if space.is_frame else space
                for space in self.target_spaces
            }
        )
        view_output = WorkingSpace(
            structure_id=ID.new(WorkingSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=self.frame.parent_concept,
            conceptual_space=self.frame.conceptual_space,
            locations=[view_location],
            contents=StructureCollection(),
            no_of_dimensions=1,
            dimensions=[],
            sub_spaces=[],
        )
        view = SimplexView(
            structure_id=view_id,
            parent_id=self.codelet_id,
            location=view_location,
            members=StructureCollection(),
            input_spaces=input_spaces,
            output_space=view_output,
            quality=0,
        )
        self.bubble_chamber.logger.log(view_output)
        self.bubble_chamber.working_spaces.add(view_output)
        self.bubble_chamber.logger.log(view)
        self.bubble_chamber.views.add(view)
        self.child_structures = StructureCollection({view})
