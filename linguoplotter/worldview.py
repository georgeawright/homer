from .structure_collection import StructureCollection


class Worldview:
    def __init__(self, views: StructureCollection):
        self.views = views
        self.satisfaction = 0

    @property
    def output(self):
        return ". ".join(
            [
                view.output_space.contents.filter(
                    lambda x: x.is_letter_chunk and x.super_chunks.is_empty()
                )
                .get()
                .name
                for view in self.views
            ]
        )
