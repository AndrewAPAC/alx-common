__author__ = "Andrew Lister"
__author_email__ = "andrew.lister@outlook.co.id"

import os
from pathlib import Path

# Set __doc__ to the first paragraph of README.md
_readme_path = Path(__file__).resolve().parent.parent / "README.md"
if _readme_path.exists():
    with _readme_path.open(encoding="utf-8") as f:
        lines = f.read().splitlines()

    first_paragraph = []
    for line in lines:
        if not line.strip():
            break
        first_paragraph.append(line)

    if first_paragraph:
        __doc__ = "\n".join(first_paragraph)