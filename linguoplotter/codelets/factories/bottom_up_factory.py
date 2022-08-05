from linguoplotter.codelets import Factory
from linguoplotter.errors import MissingStructureError


class BottomUpFactory(Factory):
    def follow_up_urgency(self):
        if self.bubble_chamber.focus.view is None:
            try:
                return max(
                    min(
                        [
                            1 - self.bubble_chamber.satisfaction,
                            self.child_codelets[0].urgency,
                        ]
                    ),
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
            except IndexError:
                return max(
                    1 - self.bubble_chamber.satisfaction,
                    self.coderack.MINIMUM_CODELET_URGENCY,
                )
        return self.coderack.MINIMUM_CODELET_URGENCY

    def _proportion_of_unchunked_raw_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        raw_chunks = input_space.contents.filter(
            lambda x: x.is_chunk and x.is_raw
        ).sample(10)
        return len(raw_chunks.where(unchunkedness=1.0)) / len(raw_chunks)

    def _proportion_of_unlabeled_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            non_raw_chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
            unlabeled_non_raw_chunks = non_raw_chunks.filter(
                lambda x: x.labels.is_empty()
            )
            return len(unlabeled_non_raw_chunks) / len(non_raw_chunks)
        except MissingStructureError:
            return float("-inf")

    def _proportion_of_unrelated_chunks(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            non_raw_chunks = input_space.contents.filter(
                lambda x: x.is_chunk and not x.is_raw
            ).sample(10)
            unrelated_non_raw_chunks = non_raw_chunks.filter(
                lambda x: x.relations.is_empty()
            )
            return len(unrelated_non_raw_chunks) / len(non_raw_chunks)
        except MissingStructureError:
            return float("-inf")

    def _proportion_of_uncorresponded_links(self):
        input_space = self.bubble_chamber.spaces.where(is_main_input=True).get()
        try:
            labels_and_relations = input_space.contents.filter(
                lambda x: x.is_label or x.is_relation
            ).sample(10)
            uncorresponded_links = labels_and_relations.filter(
                lambda x: x.correspondences.is_empty()
            )
            return len(uncorresponded_links) / len(labels_and_relations)
        except MissingStructureError:
            return float("-inf")
