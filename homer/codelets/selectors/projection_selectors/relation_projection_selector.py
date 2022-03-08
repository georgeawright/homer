from homer.codelets.selectors import ProjectionSelector
from homer.codelets.evaluators.projection_evaluators import RelationProjectionEvaluator
from homer.codelets.suggesters.projection_suggesters import RelationProjectionSuggester
from homer.errors import MissingStructureError
from homer.structure_collection_keys import uncorrespondedness


class RelationProjectionSelector(ProjectionSelector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["relation"]

    def _passes_preliminary_checks(self):
        return True

    def _engender_follow_up(self):
        correspondence_from_frame = self.bubble_chamber.new_structure_collection(
            *[
                correspondence
                for correspondence in self.winners.where(is_correspondence=True)
                if correspondence.start.parent_space.parent_concept
                == correspondence.end.parent_space.parent_concept
            ]
        ).get()
        frame = correspondence_from_frame.start.parent_space
        try:
            new_target = frame.contents.where(is_relation=True).get(
                key=uncorrespondedness, exclude=[correspondence_from_frame.start]
            )
            self.child_codelets.append(
                RelationProjectionSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    {
                        "target_view": correspondence_from_frame.parent_view,
                        "target_projectee": new_target,
                    },
                    new_target.unhappiness,
                )
            )
        except MissingStructureError:
            pass
        self.child_codelets.append(
            RelationProjectionEvaluator.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
            )
        )
