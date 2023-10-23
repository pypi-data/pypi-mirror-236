"""Use nandai to detect and fix LLM hallucinations.

The most commonly used functions are:
  - nandai.validate — validate one or multiple prompt-response pairs with optional context
"""

__version__ = "0.1.7"

from nandai.validator import NandValidator

_validator = NandValidator()
validate = _validator.validate
display = _validator.display

__all__ = (
    "__version__",
    "validate",
    "display",
)
