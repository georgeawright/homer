import pytest
import random
from unittest.mock import Mock, patch

from linguoplotter.codelets import CoderackCleaner
from linguoplotter.coderack import Coderack


@pytest.mark.parametrize(
    "last_satisfaction_score, current_satisfaction_score, "
    + "expected_no_of_codelets, minimum_urgency",
    [(0, 1, 6, 0), (0.5, 0.5, 4, 0.5), (1, 0, 1, 0)],
)
def test_coderack_cleaner_removes_low_urgency_offending_codelets(
    last_satisfaction_score,
    current_satisfaction_score,
    expected_no_of_codelets,
    minimum_urgency,
):
    class OffendingCodelet:
        def __init__(self, urgency):
            self.urgency = urgency

    class NonOffendingCodelet:
        pass

    with patch.object(random, "random", return_value=0.5):
        bubble_chamber = Mock()
        bubble_chamber.loggers = {"activity": Mock()}
        bubble_chamber.satisfaction = current_satisfaction_score
        coderack = Coderack(Mock(), Mock())
        coderack._codelets = [
            OffendingCodelet(0.9),
            OffendingCodelet(0.7),
            OffendingCodelet(0.5),
            OffendingCodelet(0.3),
            OffendingCodelet(0.1),
            NonOffendingCodelet(),
        ]
        coderack.recently_run = {OffendingCodelet}
        coderack_cleaner = CoderackCleaner(
            "", "", bubble_chamber, coderack, last_satisfaction_score, Mock()
        )
        coderack_cleaner.run()
        assert len(coderack._codelets) == expected_no_of_codelets
        assert coderack.recently_run == set()
        for codelet in coderack._codelets:
            assert (
                not isinstance(codelet, OffendingCodelet)
                or codelet.urgency >= minimum_urgency
            )
