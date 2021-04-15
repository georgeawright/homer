from homer.codelets import Builder


# TODO
class LabelProjectionBuilder(Builder):
    """Builds a label in a new space with a correspondence to a node in another space.
    Sets the value or coordinates of the chunk according to the parent concept's prototyp."""

    # target is a word with an adjective label in one space and the chunk in the target space
