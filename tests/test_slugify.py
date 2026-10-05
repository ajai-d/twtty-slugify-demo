import pytest

from src.app.slugify import slugify


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Hello, World!", "hello-world"),          # AC-1
        ("  Café del Mar  ", "cafe-del-mar"),       # AC-2
        ("multiple   ---  separators", "multiple-separators"),  # AC-3
        ("", ""),                                    # AC-4
        ("!!!", ""),                                 # AC-4
    ],
)
def test_slugify_rules(text, expected):
    """AC-1..AC-4: slug casing, unicode, separator collapse, empty input."""
    assert slugify(text) == expected
