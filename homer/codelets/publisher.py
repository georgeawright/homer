from homer.codelet import Codelet


# TODO
class Publisher(Codelet):
    """Takes Output View of a CheckingView as target.
    The more of the input space that is contained in the ouptut space,
    and the higher the quality of the output space,
    the more likely publisher is to succeed.
    If successful, output is sent to bubble_chamber.result as string"""
