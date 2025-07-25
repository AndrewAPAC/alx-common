__author__ = "Andrew Lister"
__author_email__ = "andrew.lister@outlook.co.id"

import os
from pathlib import Path

# Read README content
_readme_path = Path(__file__).parent.parent / "README.md"
if _readme_path.exists():
    __doc__ = _readme_path.read_text()
