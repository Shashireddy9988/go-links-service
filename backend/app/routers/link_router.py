from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from app.schemas.link import GoLinkResponse, GoLinkCreate, GoLinkUpdate, ApiResponse, MetaResponse
from app.services.link_service import LinkService

router = APIRouter(prefix="/api/v1/links", tags=["Links API"])

def get_link_service(request: Request) -> LinkService:
    return request.app.state.link_service

@router.get("", response_model=ApiResponse[List[GoLinkResponse]])
async def get_all_links(
    request: Request,
    search: Optional[str] = Query(None, description="Search term for alias, title, url, or tag"),
    tag: Optional[str] = Query(None, description="Filter by exact tag"),
    sortBy: str = Query("createdAt", alias="sortBy", description="Sort by alias, clickCount, or createdAt"),
    sortOrder: str = Query("desc", alias="sortOrder", description="Sort order: asc or desc"),
    service: LinkService = Depends(get_link_service)
):
    links = await service.get_all_links(search=search, tag=tag, sort_by=sortBy, sort_order=sortOrder)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        data=links,
        meta=MetaResponse(requestId=req_id, totalCount=len(links))
    )

@router.post("", response_model=ApiResponse[GoLinkResponse], status_code=status.HTTP_201_CREATED)
async def create_link(
    request: Request,
    dto: GoLinkCreate,
    service: LinkService = Depends(get_link_service)
):
    created = await service.create_link(dto)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        data=created,
        meta=MetaResponse(requestId=req_id)
    )

@router.get("/alias/{alias}", response_model=ApiResponse[GoLinkResponse])
async def get_by_alias(
    request: Request,
    alias: str,
    service: LinkService = Depends(get_link_service)
):
    link = await service.get_link_by_alias(alias)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        data=link,
        meta=MetaResponse(requestId=req_id)
    )

@router.get("/{id}", response_model=ApiResponse[GoLinkResponse])
async def get_by_id(
    request: Request,
    id: str,
    service: LinkService = Depends(get_link_service)
):
    link = await service.get_link_by_id(id)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        data=link,
        meta=MetaResponse(requestId=req_id)
    )

@router.put("/{id}", response_model=ApiResponse[GoLinkResponse])
async def update_link(
    request: Request,
    id: str,
    dto: GoLinkUpdate,
    service: LinkService = Depends(get_link_service)
):
    updated = await service.update_link(id, dto)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        data=updated,
        meta=MetaResponse(requestId=req_id)
    )

@router.delete("/{id}", response_model=ApiResponse[None])
async def delete_link(
    request: Request,
    id: str,
    service: LinkService = Depends(get_link_service)
):
    await service.delete_link(id)
    req_id = getattr(request.state, "request_id", "")
    return ApiResponse(
        success=True,
        meta=MetaResponse(requestId=req_id)
    )
