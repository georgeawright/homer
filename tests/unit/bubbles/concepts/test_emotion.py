from homer.bubbles.concepts.emotion import Emotion


def test_constructor():
    satisfaction = Emotion("satisfaction", depth=10)
    assert satisfaction.activation.as_scalar() == 0
