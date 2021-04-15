from homer.codelets import Builder


# TODO
class RelationProjectionBuilder(Builder):
    """Builds a relation in a new space with a correspondence to a node in another space.
    Sets or alters the value or coordinates of its arguments
    according to the parent concept's prototype."""

    # target is a word with an adverb label in one space and the chunks in the target space
