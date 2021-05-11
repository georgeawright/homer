from homer.bubble_chamber import BubbleChamber
from homer.codelets.selector import Selector
from homer.errors import MissingStructureError
from homer.structure_collection import StructureCollection


class ViewSelector(Selector):
    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        if self.challengers is not None:
            return True
        try:
            champion_view = self.champions.get_random()
            challenger_view = champion_view.nearby().get_random()
            self.challengers = StructureCollection({challenger_view})
        except MissingStructureError:
            return True
        return True

    def _fizzle(self):
        new_target = self.bubble_chamber.views.get_unhappy()
        builder_class = self.get_target_class().get_builder_class()
        self.child_codelets.append(
            builder_class.spawn(
                self.codelet_id,
                self.bubble_chamber,
                new_target,
                new_target.unhappiness,
            )
        )

    def _engender_follow_up(self):
        builder_class = self.get_target_class().get_builder_class()
        self.child_codelets.append(
            builder_class.make(self.codelet_id, self.bubble_chamber)
        )
        self.child_codelets.append(
            self.spawn(
                self.codelet_id,
                self.bubble_chamber,
                self.winners,
                self.follow_up_urgency,
                challengers=self.challengers,
            )
        )
