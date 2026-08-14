from typing import List, Optional, Generic, TypeVar
from datetime import datetime, timezone
import re
from pydantic import BaseModel, Field, HttpUrl, field_validator, AliasChoices

T = TypeVar("T")

ALIAS_REGEX = re.compile(r"^[a-zA-Z0-9_-]+$")

class GoLinkCreate(BaseModel):
    alias: str = Field(..., min_length=2, max_length=60, description="Shortcut alias e.g. design-system")
    target_url: str = Field(..., validation_alias=AliasChoices("targetUrl", "target_url"), description="Target destination URL e.g. https://figma.com")
    title: str = Field(..., min_length=2, max_length=100, description="Human readable title")
    description: Optional[str] = Field(None, max_length=500)
    tags: List[str] = Field(default_factory=list, max_length=10)

    @field_validator("alias", mode="before")
    @classmethod
    def sanitize_alias(cls, v: str) -> str:
        if isinstance(v, str):
            clean = v.strip().lower()
            if clean.startswith("go/"):
                clean = clean[3:]
            return clean
        return v

    @field_validator("alias")
    @classmethod
    def validate_alias_chars(cls, v: str) -> str:
        if not ALIAS_REGEX.match(v):
            raise ValueError("Alias can only contain letters, numbers, hyphens, and underscores")
        return v

    @field_validator("target_url")
    @classmethod
    def validate_url_protocol(cls, v: str) -> str:
        clean = v.strip()
        if not (clean.startswith("http://") or clean.startswith("https://")):
            raise ValueError("Target URL must start with http:// or https://")
        return clean

    @field_validator("tags", mode="before")
    @classmethod
    def clean_tags(cls, v: Optional[List[str]]) -> List[str]:
        if not v:
            return []
        return [t.strip().lower() for t in v if t and t.strip()]


class GoLinkUpdate(BaseModel):
    alias: Optional[str] = Field(None, min_length=2, max_length=60)
    target_url: Optional[str] = Field(None, validation_alias=AliasChoices("targetUrl", "target_url"))
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None

    @field_validator("alias", mode="before")
    @classmethod
    def sanitize_alias(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            clean = v.strip().lower()
            if clean.startswith("go/"):
                clean = clean[3:]
            return clean
        return v

    @field_validator("target_url")
    @classmethod
    def validate_url_protocol(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        clean = v.strip()
        if not (clean.startswith("http://") or clean.startswith("https://")):
            raise ValueError("Target URL must start with http:// or https://")
        return clean


class GoLinkResponse(BaseModel):
    id: str
    alias: str
    targetUrl: str
    title: str
    description: Optional[str] = ""
    tags: List[str] = Field(default_factory=list)
    clickCount: int = 0
    lastAccessedAt: Optional[str] = None
    createdAt: str
    updatedAt: str


class MetaResponse(BaseModel):
    requestId: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    totalCount: Optional[int] = None


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[dict] = None
    meta: Optional[MetaResponse] = None
