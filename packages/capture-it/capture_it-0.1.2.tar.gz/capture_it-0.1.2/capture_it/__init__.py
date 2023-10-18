__doc__ = '''Device Output Capture Utility'''

__version__ = "0.1.2"

from .executions import Execute_By_Login as capture
from .executions import Execute_By_Individual_Commands as capture_individual
from ._detection import quick_display
from ._cap_summary import LogSummary
from .gui import CaptureIT
