import pytest
import random
from unittest.mock import Mock, patch

from linguoplotter.codelet_result import CodeletResult
from linguoplotter.codelets.selectors.view_selectors import MonitoringViewSelector
from linguoplotter.codelets.suggesters.view_suggesters import MonitoringViewSuggester
from linguoplotter.structure_collection import StructureCollection
from linguoplotter.tools import hasinstance


# TODO or not TODO
