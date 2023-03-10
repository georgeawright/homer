from linguoplotter import fuzzy
from linguoplotter.codelets.selectors import LabelSelector
from linguoplotter.codelets.suggesters.label_suggesters import (
    InterspatialLabelSuggester,
)
from linguoplotter.errors import MissingStructureError
from linguoplotter.structure_collection_keys import activation, labeling_exigency
from linguoplotter.structure_collections import StructureSet


class InterspatialLabelSelector(LabelSelector):
    def _passes_preliminary_checks(self):
        if self.challengers.not_empty:
            return True
        champion = self.champions.get()
        try:
            self.challengers.add(
                StructureSet.union(
                    *[
                        node.labels
                        for node in champion.parent_space.contents.where(is_chunk=True)
                    ]
                )
                .filter(
                    lambda x: x.start != champion.start
                    and x.parent_concept == champion.parent_concept
                    and x.parent_spaces == champion.parent_spaces
                )
                .get()
            )
        except MissingStructureError:
            return True
        return True

    def _engender_follow_up(self):
        try:
            winning_label = self.winners.get()
            view = self.bubble_chamber.views.filter(
                lambda x: x.unhappiness < self.FLOATING_POINT_TOLERANCE
                and x.parent_frame.parent_concept.location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
                == self.bubble_chamber.concepts["sentence"].location_in_space(
                    self.bubble_chamber.spaces["grammar"]
                )
            ).get(
                key=lambda x: fuzzy.OR(
                    self.bubble_chamber.worldview.view is not None
                    and x in self.bubble_chamber.worldview.view.all_sub_views,
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
                and x in start.parent_space.conceptual_spaces
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
