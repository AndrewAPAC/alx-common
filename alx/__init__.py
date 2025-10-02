"""alx-common: An application framework promoting consistency and centralising common tasks."""

__author__ = "Andrew Lister"
__author_email__ = "andrew.lister@outlook.co.id"

import os
from pathlib import Path

# Set __doc__ based on context
_readme_path = Path(__file__).resolve().parent.parent / "README.md"
if _readme_path.exists():
    with _readme_path.open(encoding="utf-8") as f:
        content = f.read()

    # If pdoc is generating docs, use full README
    if os.getenv('PDOC'):
        __doc__ = content
    else:
        # For help(), use just the first paragraph
        lines = content.splitlines()
        first_paragraph = []
        for line in lines:
            if not line.strip():
                break
            first_paragraph.append(line)

        if first_paragraph:
            __doc__ = "\n".join(first_paragraph)
