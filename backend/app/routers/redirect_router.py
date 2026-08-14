from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from app.services.link_service import LinkService

router = APIRouter(tags=["Redirection"])

def get_link_service(request: Request) -> LinkService:
    return request.app.state.link_service

@router.get("/go/{alias:path}")
@router.get("/r/{alias:path}")
async def redirect_alias(
    alias: str,
    service: LinkService = Depends(get_link_service)
):
    target_url = await service.resolve_redirect(alias)
    return RedirectResponse(url=target_url, status_code=302)
