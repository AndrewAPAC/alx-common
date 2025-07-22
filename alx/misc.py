
def normalize(s: str) -> str:
    """
    Normalize a string: trim, lowercase, collapse internal whitespace.

    Args:
        s (str): The input string.

    Returns:
        str: Normalized string.
    """
    return " ".join(s.strip().lower().split())


def spaces_to_underscores(s: str) -> str:
    """
    Replace spaces in a string with underscores.

    Args:
        s (str): The input string.

    Returns:
        str: String with spaces replaced by underscores.
    """
    return s.replace(" ", "_")
