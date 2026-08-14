from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.link_repository import BaseLinkRepository
from app.schemas.link import GoLinkResponse, GoLinkCreate, GoLinkUpdate


class LinkService:
    def __init__(self, repo: BaseLinkRepository):
        self.repo = repo

    async def get_all_links(self, search: Optional[str] = None, tag: Optional[str] = None, sort_by: str = "createdAt", sort_order: str = "desc") -> List[GoLinkResponse]:
        return await self.repo.find_all(search=search, tag=tag, sort_by=sort_by, sort_order=sort_order)

    async def get_link_by_id(self, link_id: str) -> GoLinkResponse:
        link = await self.repo.find_by_id(link_id)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "NOT_FOUND", "message": f"GoLink with ID '{link_id}' not found"}
            )
        return link

    async def get_link_by_alias(self, alias: str) -> GoLinkResponse:
        norm = alias.lower()
        if norm.startswith("go/"):
            norm = norm[3:]
        link = await self.repo.find_by_alias(norm)
        if not link:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "NOT_FOUND", "message": f"GoLink shortcut 'go/{norm}' not found"}
            )
        return link

    async def resolve_redirect(self, alias: str) -> str:
        link = await self.get_link_by_alias(alias)
        await self.repo.increment_click(link.id)
        return link.targetUrl

    async def create_link(self, dto: GoLinkCreate) -> GoLinkResponse:
        norm_alias = dto.alias.lower()
        if norm_alias.startswith("go/"):
            norm_alias = norm_alias[3:]

        existing = await self.repo.find_by_alias(norm_alias)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"code": "ALREADY_EXISTS", "message": f"Shortcut 'go/{norm_alias}' already exists"}
            )

        return await self.repo.create(dto)

    async def update_link(self, link_id: str, dto: GoLinkUpdate) -> GoLinkResponse:
        existing = await self.get_link_by_id(link_id)

        if dto.alias:
            norm_alias = dto.alias.lower()
            if norm_alias.startswith("go/"):
                norm_alias = norm_alias[3:]
            if norm_alias != existing.alias:
                alias_conflict = await self.repo.find_by_alias(norm_alias)
                if alias_conflict and alias_conflict.id != link_id:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail={"code": "ALREADY_EXISTS", "message": f"Shortcut 'go/{norm_alias}' is already in use"}
                    )

        updated = await self.repo.update(link_id, dto)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "NOT_FOUND", "message": f"GoLink with ID '{link_id}' not found"}
            )
        return updated

    async def delete_link(self, link_id: str) -> None:
        await self.get_link_by_id(link_id)  # Raises 404 if not found
        await self.repo.delete(link_id)
