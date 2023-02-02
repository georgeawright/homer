from linguoplotter import fuzzy
from linguoplotter.codelets.selectors import LabelSelector
from linguoplotter.codelets.suggesters.label_suggesters import (
    InterspatialLabelSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation, labeling_exigency


class InterspatialLabelSelector(LabelSelector):
    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        champion = self.champions.get()
        try:
            self.challengers.add(
                champion.start.champion_labels.filter(
                    lambda x: x.parent_spaces == champion.parent_spaces
                )
                .excluding(champion)
                .get()
            )
        except MissingStructureError:
            try:
                self.challengers.add(
                    champion.start.labels.filter(
                        lambda x: x.parent_spaces == champion.parent_spaces
                    )
                    .excluding(champion)
                    .get(key=activation)
                )
            except MissingStructureError:
                return True
        return True

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get()
            view = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept
                == self.bubble_chamber.concepts["sentence"]
            ).get(
                key=lambda x: fuzzy.OR(
                    x in self.bubble_chamber.worldview.views,
                    x.super_views.not_empty,
                    x.activation,
                )
            )
            start = view.output_space.contents.filter(
                lambda x: x.is_letter_chunk
                and x.members.is_empty
                and len(x.parent_spaces.where(is_conceptual_space=True)) > 1
            ).get(key=labeling_exigency)
            space = start.parent_spaces.filter(
                lambda x: x.is_conceptual_space
                and x.no_of_dimensions == 1
                and not x.is_symbolic
            ).get(key=activation)
            targets = self.bubble_chamber.new_dict(
                {
                    "start": start,
                    "concept": winning_label.parent_concept,
                    "space": space,
                },
                name="targets",
            )
            self.child_codelets.append(
                InterspatialLabelSuggester.spawn(
                    self.codelet_id,
                    self.bubble_chamber,
                    targets,
                    start.unlabeledness,
                )
            )
        except MissingStructureError:
            pass
