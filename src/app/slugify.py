import re
import unicodedata

_non_alnum = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug (see spec Iteration-YVIVBU §4).

    Rules: NFKD-normalize and drop non-ASCII marks, lowercase, collapse any run
    of non-alphanumeric characters to a single hyphen, trim leading/trailing
    hyphens. Empty or all-separator input yields an empty string.
    """
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    hyphenated = _non_alnum.sub("-", ascii_text.lower())
    return hyphenated.strip("-")
