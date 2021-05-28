from homer.codelets.selector import Selector
from homer.codelets.suggesters import CorrespondenceSuggester
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection
from homer.structure_collection_keys import activation, corresponding_exigency
from homer.structures import Node
from homer.structures.links import Correspondence
from homer.structures.spaces import WorkingSpace


class CorrespondenceSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["correspondence"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        champion_correspondence = self.champions.get()
        candidates = champion_correspondence.start.correspondences_to_space(
            champion_correspondence.end_space
        )
        if len(candidates) > 1:
            challenger_correspondence = candidates.get(
                key=activation, exclude=[champion_correspondence]
            )
            self.challengers = StructureCollection({challenger_correspondence})
        return True

    def _fizzle(self):
        pass

    def _engender_follow_up(self):
        winner_correspondence = self.winners.get()
        target_view = winner_correspondence.parent_view
        try:
            if isinstance(winner_correspondence.start, Node):
                target_structure_one = winner_correspondence.start.links.not_of_type(
                    Correspondence
                ).get(key=corresponding_exigency)
            else:
                target_structure_one = (
                    winner_correspondence.start.arguments.get()
                    .links.not_of_type(Correspondence)
                    .get(key=corresponding_exigency)
                )
            target_space_one = target_structure_one.parent_space
            target_conceptual_space = target_space_one.conceptual_space
            target_space_two = (
                target_view.input_spaces.get(
                    exclude=list(target_space_one.parent_spaces)
                )
                .contents.of_type(WorkingSpace)
                .where(is_basic_level=True)
                .where(conceptual_space=target_conceptual_space)
                .get()
            )
            if isinstance(winner_correspondence.end, Node):
                target_structure_two = (
                    winner_correspondence.end.links.of_type(type(target_structure_one))
                    .where(parent_space=target_space_two)
                    .get()
                )
            else:
                target_structure_two = (
                    winner_correspondence.end.arguments.get()
                    .links.of_type(type(target_structure_one))
                    .where(parent_space=target_space_two)
                    .get(key=corresponding_exigency)
                )
            target_concept = winner_correspondence.parent_concept.friends().get()
        except MissingStructureError:
            return
        self.child_codelets.append(
            CorrespondenceSuggester.spawn(
                self.codelet_id,
                self.bubble_chamber,
                {
                    "target_view": winner_correspondence.parent_view,
                    "target_space_one": target_space_one,
                    "target_structure_one": target_structure_one,
                    "target_space_two": target_space_two,
                    "target_structure_two": target_structure_two,
                    "target_conceptual_space": target_conceptual_space,
                    "parent_concept": target_concept,
                },
                target_structure_one.uncorrespondedness,
            )
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.losers,
            )
        )
