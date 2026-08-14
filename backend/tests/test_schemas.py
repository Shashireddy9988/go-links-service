import pytest
from pydantic import ValidationError
from app.schemas.link import GoLinkCreate

def test_valid_link_schema():
    payload = {
        "alias": "design-system",
        "target_url": "https://storybook.js.org",
        "title": "Design System",
        "tags": ["design", "ui"]
    }
    model = GoLinkCreate(**payload)
    assert model.alias == "design-system"
    assert model.target_url == "https://storybook.js.org"

def test_alias_stripping_go_prefix():
    payload = {
        "alias": "go/oncall",
        "target_url": "https://pagerduty.com",
        "title": "On-Call Rotation"
    }
    model = GoLinkCreate(**payload)
    assert model.alias == "oncall"

def test_invalid_url_protocol_raises():
    payload = {
        "alias": "bad-url",
        "target_url": "ftp://example.com",
        "title": "Bad Protocol"
    }
    with pytest.raises(ValidationError):
        GoLinkCreate(**payload)

def test_invalid_alias_characters_raises():
    payload = {
        "alias": "invalid alias spaces!",
        "target_url": "https://example.com",
        "title": "Bad Alias"
    }
    with pytest.raises(ValidationError):
        GoLinkCreate(**payload)
