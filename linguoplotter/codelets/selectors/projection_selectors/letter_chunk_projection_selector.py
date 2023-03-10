from linguoplotter.codelets.selectors import ProjectionSelector
from linguoplotter.codelets.suggesters.projection_suggesters import (
    LetterChunkProjectionSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import uncorrespondedness


class LetterChunkProjectionSelector(ProjectionSelector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["letter-chunk"]

    def _passes_preliminary_checks(self):
        return True

    def _engender_follow_up(self):
        try:
            letter_chunk = self.winners.where(is_letter_chunk=True).get()
            correspondence = self.winners.where(is_correspondence=True).get()
            view = correspondence.parent_view
            frame = view.frames.filter(lambda x: letter_chunk in x.items).get()
            frame_space = correspondence.start.parent_space
            new_target = (
                frame_space.contents.where(is_chunk=True)
                .excluding(letter_chunk)
                .get(key=uncorrespondedness)
            )
            targets = self.bubble_chamber.new_dict(
                {"view": view, "frame": frame, "projectee": new_target},
                name="targets",
            )
            self.child_codelets.append(
                LetterChunkProjectionSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    new_target.unhappiness,
                )
            )
        except MissingStructureError:
            pass
