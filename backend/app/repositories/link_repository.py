from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import uuid
import random
from datetime import datetime, timezone
from app.schemas.link import GoLinkResponse, GoLinkCreate, GoLinkUpdate


class BaseLinkRepository(ABC):
    @abstractmethod
    async def find_all(self, search: Optional[str] = None, tag: Optional[str] = None, sort_by: str = "createdAt", sort_order: str = "desc") -> List[GoLinkResponse]:
        pass

    @abstractmethod
    async def find_by_id(self, link_id: str) -> Optional[GoLinkResponse]:
        pass

    @abstractmethod
    async def find_by_alias(self, alias: str) -> Optional[GoLinkResponse]:
        pass

    @abstractmethod
    async def create(self, dto: GoLinkCreate) -> GoLinkResponse:
        pass

    @abstractmethod
    async def update(self, link_id: str, dto: GoLinkUpdate) -> Optional[GoLinkResponse]:
        pass

    @abstractmethod
    async def delete(self, link_id: str) -> bool:
        pass

    @abstractmethod
    async def increment_click(self, link_id: str) -> Optional[GoLinkResponse]:
        pass


class InMemoryLinkRepository(BaseLinkRepository):
    def __init__(self, seed: bool = True):
        self._store: Dict[str, GoLinkResponse] = {}
        if seed:
            self._seed_data()

    def _seed_data(self):
        samples = [
            GoLinkCreate(
                alias="design-system",
                target_url="https://storybook.js.org",
                title="Design System & Component Library",
                description="Official UI components, design tokens, and style guide",
                tags=["design", "frontend", "ui"]
            ),
            GoLinkCreate(
                alias="oncall",
                target_url="https://pagerduty.com",
                title="Engineering On-Call Schedule",
                description="Current primary and secondary on-call engineer rotations",
                tags=["engineering", "ops", "urgent"]
            ),
            GoLinkCreate(
                alias="payroll",
                target_url="https://gusto.com",
                title="Employee Payroll & Benefits Portal",
                description="Access paystubs, tax forms, and health insurance information",
                tags=["hr", "finance", "people"]
            ),
            GoLinkCreate(
                alias="docs",
                target_url="https://notion.so",
                title="Company Engineering Wiki",
                description="Architecture decision records, onboarding docs, and RFCs",
                tags=["docs", "wiki"]
            )
        ]
        for s in samples:
            now = datetime.now(timezone.utc).isoformat()
            link = GoLinkResponse(
                id=str(uuid.uuid4()),
                alias=s.alias.lower(),
                targetUrl=s.target_url,
                title=s.title,
                description=s.description or "",
                tags=s.tags or [],
                clickCount=random.randint(5, 50),
                lastAccessedAt=now,
                createdAt=now,
                updatedAt=now
            )
            self._store[link.id] = link

    async def find_all(self, search: Optional[str] = None, tag: Optional[str] = None, sort_by: str = "createdAt", sort_order: str = "desc") -> List[GoLinkResponse]:
        items = list(self._store.values())

        if search:
            q = search.lower()
            items = [
                i for i in items
                if q in i.alias.lower()
                or q in i.title.lower()
                or q in i.targetUrl.lower()
                or (i.description and q in i.description.lower())
                or any(q in t.lower() for t in i.tags)
            ]

        if tag:
            t_q = tag.lower()
            items = [i for i in items if any(t.lower() == t_q for t in i.tags)]

        reverse = (sort_order.lower() == "desc")
        if sort_by == "alias":
            items.sort(key=lambda x: x.alias.lower(), reverse=reverse)
        elif sort_by == "clickCount":
            items.sort(key=lambda x: x.clickCount, reverse=reverse)
        else: # createdAt
            items.sort(key=lambda x: x.createdAt, reverse=reverse)

        return items

    async def find_by_id(self, link_id: str) -> Optional[GoLinkResponse]:
        return self._store.get(link_id)

    async def find_by_alias(self, alias: str) -> Optional[GoLinkResponse]:
        norm = alias.lower()
        if norm.startswith("go/"):
            norm = norm[3:]
        for link in self._store.values():
            if link.alias.lower() == norm:
                return link
        return None

    async def create(self, dto: GoLinkCreate) -> GoLinkResponse:
        now = datetime.now(timezone.utc).isoformat()
        norm_alias = dto.alias.lower()
        if norm_alias.startswith("go/"):
            norm_alias = norm_alias[3:]

        link = GoLinkResponse(
            id=str(uuid.uuid4()),
            alias=norm_alias,
            targetUrl=dto.target_url,
            title=dto.title,
            description=dto.description or "",
            tags=dto.tags or [],
            clickCount=0,
            lastAccessedAt=None,
            createdAt=now,
            updatedAt=now
        )
        self._store[link.id] = link
        return link

    async def update(self, link_id: str, dto: GoLinkUpdate) -> Optional[GoLinkResponse]:
        existing = self._store.get(link_id)
        if not existing:
            return None

        data = existing.model_dump()
        if dto.alias:
            clean_alias = dto.alias.lower()
            if clean_alias.startswith("go/"):
                clean_alias = clean_alias[3:]
            data["alias"] = clean_alias
        if dto.target_url:
            data["targetUrl"] = dto.target_url
        if dto.title is not None:
            data["title"] = dto.title
        if dto.description is not None:
            data["description"] = dto.description
        if dto.tags is not None:
            data["tags"] = dto.tags

        data["updatedAt"] = datetime.now(timezone.utc).isoformat()
        updated = GoLinkResponse(**data)
        self._store[link_id] = updated
        return updated

    async def delete(self, link_id: str) -> bool:
        if link_id in self._store:
            del self._store[link_id]
            return True
        return False

    async def increment_click(self, link_id: str) -> Optional[GoLinkResponse]:
        existing = self._store.get(link_id)
        if not existing:
            return None

        data = existing.model_dump()
        data["clickCount"] += 1
        data["lastAccessedAt"] = datetime.now(timezone.utc).isoformat()
        data["updatedAt"] = datetime.now(timezone.utc).isoformat()
        updated = GoLinkResponse(**data)
        self._store[link_id] = updated
        return updated
