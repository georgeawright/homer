from linguoplotter.codelets.selectors import ProjectionSelector
from linguoplotter.codelets.suggesters.projection_suggesters import (
    RelationProjectionSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import uncorrespondedness


class RelationProjectionSelector(ProjectionSelector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        return True

    def _engender_follow_up(self):
        try:
            relation = self.winners.where(is_relation=True).get()
            correspondence = self.winners.where(is_correspondence=True).get()
            frame_space = correspondence.start.parent_space
            new_target = (
                frame_space.contents.where(is_relation=True)
                .excluding(relation)
                .get(key=uncorrespondedness)
            )
            targets = self.bubble_chamber.new_dict(
                {"view": correspondence.parent_view, "projectee": new_target},
                name="targets",
            )
            self.child_codelets.append(
                RelationProjectionSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    new_target.unhappiness,
                )
            )
        except MissingStructureError:
            pass
