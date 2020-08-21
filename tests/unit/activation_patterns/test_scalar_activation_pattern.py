import pytest

from homer.activation_patterns.scalar_activation_pattern import ScalarActivationPattern


FLOAT_COMPARISON_TOLERANCE = 1e-5


@pytest.mark.parametrize(
    "activation_coefficient, amount, prior_activation, expected_activation",
    [(0.5, 0.5, 0, 0.25), (0.5, 0.5, 0.9, 1.0)],
)
def test_boost(
    activation_coefficient, amount, prior_activation, expected_activation,
):
    activation_pattern = ScalarActivationPattern(activation_coefficient)
    activation_pattern.activation = prior_activation
    activation_pattern.boost(amount, None)
    activation_pattern.update()
    assert expected_activation == activation_pattern.activation
