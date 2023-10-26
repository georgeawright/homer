from collections import defaultdict

from linguoplotter.codelets.builders import ViewBuilder
from linguoplotter.id import ID
from linguoplotter.location import Location
from linguoplotter.structures import View


class MergedFrameViewBuilder(ViewBuilder):
    def _passes_preliminary_checks(self):
        return True

    def _process_structure(self):
        self._copy_view()
        self._generate_progenitor_frame()
        self._merge_frame()
        self._populate_view_output_space()
        new_view = self.child_structures.get()
        new_view.parent_frame.parent_view = new_view
        new_view.parent_frame.parent_concept.instances.add(new_view)
        new_view.parent_frame.progenitor.instances.add(new_view)
        self.bubble_chamber.loggers["structure"].log(new_view.output_space)
        self.bubble_chamber.loggers["structure"].log(new_view)
        self.bubble_chamber.add(new_view)
        self._structure_concept.instances.add(new_view)
        self._structure_concept.recalculate_salience()

    def _copy_view(self):
        def _copy_space(space, name: str = None):
            return self.bubble_chamber.new_contextual_space(
                name=name if name is not None else space.name,
                parent_concept=space.parent_concept,
                conceptual_spaces=space.conceptual_spaces.copy(),
                parent_id=self.codelet_id,
            )

        old_view = self.targets["view"]
        old_frame = self.targets["view"].parent_frame
        view_id = ID.new(View)
        new_output_space = self._create_view_output(
            view_id,
            old_view.output_space.parent_concept,
            old_view.output_space.conceptual_spaces,
        )
        new_frame, frame_copies = old_frame.instantiate_with_copies_map(
            input_space=old_frame.input_space,
            conceptual_spaces_map={},
            parent_id=self.codelet_id,
            bubble_chamber=self.bubble_chamber,
        )
        new_view = View(
            structure_id=view_id,
            parent_id=self.codelet_id,
            parent_frame=new_frame,
            locations=[Location([], self.bubble_chamber.spaces["views"])],
            members=self.bubble_chamber.new_set(),
            frames=self.bubble_chamber.new_set(new_frame),
            input_spaces=self.bubble_chamber.new_set(self.targets["contextual_space"]),
            output_space=new_output_space,
            quality=0,
            links_in=self.bubble_chamber.new_set(),
            links_out=self.bubble_chamber.new_set(),
            parent_spaces=self.bubble_chamber.new_set(),
            sub_views=old_view.sub_views.copy(),
            super_views=self.bubble_chamber.new_set(),
            cohesion_views=self.bubble_chamber.new_set(),
            champion_labels=self.bubble_chamber.new_set(),
            champion_relations=self.bubble_chamber.new_set(),
            cross_view_links=self.bubble_chamber.new_set(),
            cross_view_relations=defaultdict(self.bubble_chamber.new_set),
        )
        for sub_view in new_view.sub_views:
            sub_view.cohesion_views.add(new_view)
            self.bubble_chamber.loggers["structure"].log(sub_view)
        for k, v in old_view.matched_sub_frames.items():
            if k in frame_copies:
                new_view.matched_sub_frames[frame_copies[k]] = v
            else:
                new_view.matched_sub_frames[k] = v
        for correspondence in old_view.members:
            if correspondence.end in old_view.output_space.contents:
                continue
            if correspondence.parent_view != old_view:
                new_view.add(correspondence)
                continue
            start = correspondence.start
            end = frame_copies[correspondence.end]
            new_correspondence = self.bubble_chamber.new_correspondence(
                start=start,
                end=end,
                parent_concept=correspondence.parent_concept,
                locations=[location.copy() for location in correspondence.locations],
                conceptual_space=correspondence.conceptual_space,
                parent_view=new_view,
                parent_id=self.codelet_id,
                quality=correspondence.quality,
            )
            new_correspondence._activation = correspondence.activation
        self.child_structures.add(new_view)

    def _merge_frame(self):
        view = self.child_structures.get()
        parent_frame = view.parent_frame
        parent_frame.is_merged_frame = True
        parent_frame.name = self.targets["progenitor_frame"].name
        parent_frame_root_sentence = parent_frame.output_space.contents.filter(
            lambda x: x.is_letter_chunk
            and x.super_chunks.is_empty
            and x.members.not_empty
        ).get()
        parent_frame_left_sentence = parent_frame_root_sentence.left_branch.get()
        parent_frame_right_sentence = (
            parent_frame_root_sentence.right_branch.get().right_branch.get()
        )
        parent_frame_conjunction = (
            parent_frame_root_sentence.right_branch.get().left_branch.get()
        )
        parent_frame_left_sub_frame = [
            s
            for s in parent_frame.sub_frames
            if parent_frame_left_sentence in s.output_space.contents
        ][0]
        parent_frame_right_sub_frame = [
            s
            for s in parent_frame.sub_frames
            if parent_frame_right_sentence in s.output_space.contents
        ][0]
        new_frame = self.targets["frame"]
        parent_frame._depth += new_frame.depth
        new_frame_root_sentence = new_frame.output_space.contents.filter(
            lambda x: x.is_letter_chunk
            and x.super_chunks.is_empty
            and x.members.not_empty
        ).get()
        new_frame_left_sentence = new_frame_root_sentence.left_branch.get()
        new_frame_right_sentence = (
            new_frame_root_sentence.right_branch.get().right_branch.get()
        )
        new_frame_conjunction = (
            new_frame_root_sentence.right_branch.get().left_branch.get()
        )
        new_frame_left_sub_frame = [
            s
            for s in new_frame.sub_frames
            if new_frame_left_sentence in s.output_space.contents
        ][0]
        new_frame_right_sub_frame = [
            s
            for s in new_frame.sub_frames
            if new_frame_right_sentence in s.output_space.contents
        ][0]
        spaces_map = {
            new_frame.input_space: parent_frame.input_space,
            new_frame.output_space: parent_frame.output_space,
            new_frame_right_sub_frame.input_space: parent_frame_right_sub_frame.input_space,
            new_frame_right_sub_frame.output_space: parent_frame_right_sub_frame.output_space,
            new_frame_left_sub_frame.input_space: parent_frame_left_sub_frame.input_space,
            new_frame_left_sub_frame.output_space: parent_frame_left_sub_frame.output_space,
        }
        item_copies_map = {}
        # copy across cross_view links and their arguments except for links that recognize interstring repetition
        for link in new_frame.cross_view_links.filter(
            lambda x: not (
                x.is_label
                and x.parent_concept.parent_space
                in (
                    self.bubble_chamber.spaces["grammar"],
                    self.bubble_chamber.spaces["string"],
                )
            )
            and not (
                x.is_relation
                and x.conceptual_space
                in (
                    self.bubble_chamber.spaces["grammar"],
                    self.bubble_chamber.spaces["string"],
                )
            )
        ):
            for arg in link.arguments:
                if arg in item_copies_map:
                    continue
                new_location = Location(
                    arg.location_in_space(arg.parent_space).coordinates,
                    spaces_map[arg.parent_space],
                )
                new_item, item_copies_map = arg.copy_with_contents(
                    copies=item_copies_map,
                    bubble_chamber=self.bubble_chamber,
                    parent_id=self.codelet_id,
                    new_location=new_location,
                )
                for location in arg.locations:
                    if (
                        location.space.is_contextual_space
                        and location.space != arg.parent_space
                    ):
                        new_item.locations.append(
                            Location(
                                arg.location_in_space(location.space).coordinates,
                                spaces_map[location.space],
                            )
                        )
                for location in new_item.locations:
                    location.space.add(new_item)
                item_copies_map[arg] = new_item
                for label in arg.labels:
                    new_label = label.copy(
                        start=new_item,
                        parent_space=spaces_map[label.parent_space],
                        parent_id=self.codelet_id,
                        bubble_chamber=self.bubble_chamber,
                    )
                    new_item.links_out.add(new_label)
                    spaces_map[label.parent_space].add(new_label)
                    item_copies_map[label] = new_label
                    parent_frame.cross_view_links.add(new_label)
                for relation in arg.links_out.where(is_relation=True):
                    if relation.end not in item_copies_map:
                        continue
                    new_end = item_copies_map[relation.end]
                    new_relation = relation.copy(
                        start=new_item,
                        end=new_end,
                        parent_space=spaces_map[relation.parent_space]
                        if relation.parent_space is not None
                        else None,
                        bubble_chamber=self.bubble_chamber,
                        parent_id=self.codelet_id,
                    )
                    new_end.links_in.add(new_relation)
                    new_item.links_out.add(new_relation)
                    item_copies_map[relation] = new_relation
                    parent_frame.cross_view_links.add(relation)
                    if relation.parent_space is not None:
                        spaces_map[relation.parent_space].add(new_relation)
                for relation in arg.links_in.where(is_relation=True):
                    if relation.start not in item_copies_map:
                        continue
                    new_start = item_copies_map[relation.start]
                    new_relation = relation.copy(
                        start=new_start,
                        end=new_item,
                        parent_space=spaces_map[relation.parent_space]
                        if relation.parent_space is not None
                        else None,
                        bubble_chamber=self.bubble_chamber,
                        parent_id=self.codelet_id,
                    )
                    new_item.links_in.add(new_relation)
                    new_start.links_out.add(new_relation)
                    item_copies_map[relation] = new_relation
                    parent_frame.cross_view_links.add(new_relation)
                    if relation.parent_space is not None:
                        spaces_map[relation.parent_space].add(new_relation)
        # merge conjunctions in correct order
        parent_frame_root_sentence.right_branch.get().left_branch.remove(
            parent_frame_conjunction
        )
        new_frame_conjunction_copy = new_frame_conjunction.copy_to_location(
            parent_frame_conjunction.location_in_space(parent_frame.output_space),
            bubble_chamber=self.bubble_chamber,
            parent_id=self.codelet_id,
        )
        (left_branch, right_branch) = (
            (
                self.bubble_chamber.new_set(new_frame_conjunction_copy),
                self.bubble_chamber.new_set(parent_frame_conjunction),
            )
            if new_frame_conjunction_copy.abstract_chunk.relations.where(
                end=parent_frame_conjunction.abstract_chunk,
                parent_concept=self.bubble_chamber.concepts["more"],
                conceptual_space=self.bubble_chamber.spaces["grammar"],
            )
            else (
                self.bubble_chamber.new_set(parent_frame_conjunction),
                self.bubble_chamber.new_set(new_frame_conjunction_copy),
            )
        )
        conjunction_super_chunk = self.bubble_chamber.new_letter_chunk(
            parent_id=self.codelet_id,
            name=None,
            locations=[
                location.copy() for location in parent_frame_conjunction.locations
            ],
            parent_space=parent_frame.output_space,
            left_branch=left_branch,
            right_branch=right_branch,
        )
        parent_frame_root_sentence.right_branch.get().left_branch.add(
            conjunction_super_chunk
        )

    def _generate_progenitor_frame(self):
        frame_1 = self.targets["view"].parent_frame.progenitor
        frame_2 = self.targets["frame"].progenitor
        component_frames = (
            self.bubble_chamber.new_list(frame_1, frame_2)
            if frame_1.relations.where(
                start=frame_1,
                end=frame_2,
                parent_concept=self.bubble_chamber.concepts["more"],
                conceptual_space=self.bubble_chamber.spaces["grammar"],
            ).not_empty
            else self.bubble_chamber.new_list(frame_2, frame_1)
        )
        name = "+".join([f.name for f in component_frames])
        self.targets["progenitor_frame"] = self.bubble_chamber.new_merged_frame(
            name=name,
            parent_concept=frame_1.parent_concept,
            component_frames=component_frames,
            depth=frame_1.depth,
            parent_id=self.codelet_id,
        )
        new_view = self.child_structures.get()
        new_view.parent_frame.parent_frame = self.targets["progenitor_frame"]
