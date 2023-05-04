from __future__ import annotations

from linguoplotter.bubble_chamber import BubbleChamber
from linguoplotter.codelets.builder import Builder
from linguoplotter.float_between_one_and_zero import FloatBetweenOneAndZero
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structure_collections import StructureDict
from linguoplotter.structures import View
from linguoplotter.structures.spaces import ContextualSpace


class ViewBuilder(Builder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators import ViewEvaluator

        return ViewEvaluator

    @classmethod
    def spawn(
        cls,
        parent_id: str,
        bubble_chamber: BubbleChamber,
        targets: StructureDict,
        urgency: FloatBetweenOneAndZero,
    ):
        codelet_id = ID.new(cls)
        return cls(codelet_id, parent_id, bubble_chamber, targets, urgency)

    @property
    def _structure_concept(self):
        return self.bubble_chamber.concepts["view"]

    def _passes_preliminary_checks(self):
        return True

    def _process_structure(self):
        view_id = ID.new(View)
        input_space_concept = self.targets["contextual_space"].parent_concept
        frame_input_space = (
            self.targets["frame"].input_space
            if self.targets["frame"].input_space.parent_concept == input_space_concept
            else self.targets["frame"].output_space
        )
        space_map = (
            {} if self.targets["space_map"] is None else self.targets["space_map"]
        )
        frame_instance = self.targets["frame"].instantiate(
            input_space=frame_input_space,
            conceptual_spaces_map=space_map,
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Created frame instance: {frame_instance}"
        )
        view_output = ContextualSpace(
            structure_id=ID.new(ContextualSpace),
            parent_id=self.codelet_id,
            name=f"output for {view_id}",
            parent_concept=frame_instance.output_space.parent_concept,
            contents=self.bubble_chamber.new_set(),
            conceptual_spaces=frame_instance.output_space.conceptual_spaces,
            links_in=self.bubble_chamber.new_set(),
            links_out=self.bubble_chamber.new_set(),
            parent_spaces=self.bubble_chamber.new_set(),
            champion_labels=self.bubble_chamber.new_set(),
            champion_relations=self.bubble_chamber.new_set(),
        )
        self.bubble_chamber.loggers["activity"].log(
            f"Created output space: {view_output}"
        )
        view = View(
            structure_id=view_id,
            parent_id=self.codelet_id,
            parent_frame=frame_instance,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=self.bubble_chamber.new_set(),
            frames=self.bubble_chamber.new_set(frame_instance),
            input_spaces=self.bubble_chamber.new_set(self.targets["contextual_space"]),
            output_space=view_output,
            quality=0,
            links_in=self.bubble_chamber.new_set(),
            links_out=self.bubble_chamber.new_set(),
            parent_spaces=self.bubble_chamber.new_set(),
            sub_views=self.bubble_chamber.new_set(),
            super_views=self.bubble_chamber.new_set(),
            cohesion_views=self.bubble_chamber.new_set(),
            champion_labels=self.bubble_chamber.new_set(),
            champion_relations=self.bubble_chamber.new_set(),
        )
        frame_instance.parent_view = view
        frame_instance.progenitor.instances.add(view)
        frame_instance.parent_concept.instances.add(view)
        self.bubble_chamber.loggers["structure"].log(view_output)
        self.bubble_chamber.contextual_spaces.add(view_output)
        self.bubble_chamber.loggers["structure"].log(view)
        self.bubble_chamber.views.add(view)
        self._structure_concept.instances.add(view)
        self._structure_concept.recalculate_exigency()
        self.child_structures.add(view)
        self._populate_view_output_space()

    def _populate_view_output_space(self):
        view = self.child_structures.get()
        for chunk in view.parent_frame.output_space.contents.where(
            is_chunk=True, is_slot=False
        ):
            abstract_chunk = chunk.abstract_chunk
            output_location = Location(chunk.location.coordinates, view.output_space)
            if abstract_chunk.members.is_empty:
                new_chunk = abstract_chunk.copy_to_location(
                    output_location,
                    parent_id=self.codelet_id,
                    bubble_chamber=self.bubble_chamber,
                )
            else:
                locations = [
                    location.copy()
                    for location in abstract_chunk.locations
                    if location.space.is_conceptual_space
                ] + [output_location]
                new_chunk = self.bubble_chamber.new_letter_chunk(
                    name=None,
                    locations=locations,
                    parent_space=view.output_space,
                    abstract_chunk=abstract_chunk,
                    parent_id=self.codelet_id,
                )
            for member in chunk.left_branch:
                if member.has_correspondence_to_space(view.output_space):
                    correspondence = member.correspondences_to_space(
                        view.output_space
                    ).get()
                    correspondee = correspondence.end
                    new_chunk.left_branch.add(correspondee)
                    new_chunk.members.add(correspondee)
                    new_chunk.sub_chunks.add(correspondee)
                    correspondee.super_chunks.add(new_chunk)
                    new_chunk.update_string_location()
            for member in chunk.right_branch:
                if member.has_correspondence_to_space(view.output_space):
                    correspondence = member.correspondences_to_space(
                        view.output_space
                    ).get()
                    correspondee = correspondence.end
                    new_chunk.right_branch.add(correspondee)
                    new_chunk.members.add(correspondee)
                    new_chunk.sub_chunks.add(correspondee)
                    correspondee.super_chunks.add(new_chunk)
                    new_chunk.update_string_location()
            for super_chunk in chunk.super_chunks:
                if super_chunk.has_correspondence_to_space(view.output_space):
                    correspondence = super_chunk.correspondences_to_space(
                        view.output_space
                    ).get()
                    correspondee = correspondence.end
                    if chunk in super_chunk.left_branch:
                        correspondee.left_branch.add(new_chunk)
                    elif chunk in super_chunk.right_branch:
                        correspondee.right_branch.add(new_chunk)
                    correspondee.members.add(new_chunk)
                    correspondee.sub_chunks.add(new_chunk)
                    new_chunk.super_chunks.add(correspondee)
                    correspondee.update_string_location()
            self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=chunk,
                end=new_chunk,
                locations=[chunk.location, new_chunk.location],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
                parent_view=view,
                quality=1.0,
                is_projection=True,
            )
        for label in view.parent_frame.output_space.contents.filter(
            lambda x: x.is_label and not x.parent_concept.is_slot
        ):
            if not label.start.has_correspondence_to_space(view.output_space):
                continue
            start_correspondence = label.start.correspondences_to_space(
                view.output_space
            ).get()
            corresponding_start = start_correspondence.end
            conceptual_location = label.location_in_space(
                label.parent_concept.parent_space
            )
            output_location = corresponding_start.location_in_space(view.output_space)
            locations = [conceptual_location, output_location]
            new_label = self.bubble_chamber.new_label(
                parent_id=self.codelet_id,
                start=corresponding_start,
                parent_concept=label.parent_concept,
                locations=locations,
                quality=1.0,
            )
            self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=label,
                end=new_label,
                locations=[label.location, new_label.location],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
                parent_view=view,
                quality=1.0,
                is_projection=True,
            )
        for relation in view.parent_frame.output_space.contents.filter(
            lambda x: x.is_relation and not x.parent_concept.is_slot
        ):
            if not relation.start.has_correspondence_to_space(
                view.output_space
            ) and not relation.end.has_correspondence_to_space(view.output_space):
                continue
            start_correspondence = relation.start.correspondences_to_space(
                view.output_space
            ).get()
            corresponding_start = start_correspondence.end
            end_correspondence = relation.end.correspondences_to_space(
                view.output_space
            ).get()
            corresponding_end = end_correspondence.end
            conceptual_location = relation.location_in_space(
                relation.parent_concept.parent_space
            )
            output_location = corresponding_start.location_in_space(view.output_space)
            locations = [conceptual_location, output_location]
            new_relation = self.bubble_chamber.new_relation(
                parent_id=self.codelet_id,
                start=corresponding_start,
                end=corresponding_end,
                parent_concept=relation.parent_concept,
                locations=locations,
                quality=1.0,
            )
            self.bubble_chamber.new_correspondence(
                parent_id=self.codelet_id,
                start=relation,
                end=new_relation,
                locations=[relation.location, new_relation.location],
                parent_concept=self.bubble_chamber.concepts["same"],
                conceptual_space=self.bubble_chamber.conceptual_spaces["grammar"],
                parent_view=view,
                quality=1.0,
                is_projection=True,
            )
        for item in view.output_space.contents:
            item.quality = 1.0
            item._activation = 1.0

    def _fizzle(self):
        pass
