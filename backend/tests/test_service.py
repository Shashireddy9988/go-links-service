import pytest
from fastapi import HTTPException
from app.repositories.link_repository import InMemoryLinkRepository
from app.services.link_service import LinkService
from app.schemas.link import GoLinkCreate, GoLinkUpdate

@pytest.mark.asyncio
async def test_create_and_get_link():
    repo = InMemoryLinkRepository(seed=False)
    service = LinkService(repo)

    created = await service.create_link(GoLinkCreate(
        alias="wiki",
        target_url="https://notion.so",
        title="Company Wiki",
        tags=["docs"]
    ))

    assert created.id is not None
    assert created.alias == "wiki"
    assert created.clickCount == 0

    fetched = await service.get_link_by_alias("wiki")
    assert fetched.id == created.id

@pytest.mark.asyncio
async def test_duplicate_alias_raises_conflict():
    repo = InMemoryLinkRepository(seed=False)
    service = LinkService(repo)

    await service.create_link(GoLinkCreate(
        alias="oncall",
        target_url="https://pagerduty.com",
        title="On Call"
    ))

    with pytest.raises(HTTPException) as exc_info:
        await service.create_link(GoLinkCreate(
            alias="go/oncall",
            target_url="https://opsgenie.com",
            title="Duplicate On Call"
        ))

    assert exc_info.value.status_code == 409

@pytest.mark.asyncio
async def test_resolve_redirect_increments_click():
    repo = InMemoryLinkRepository(seed=False)
    service = LinkService(repo)

    created = await service.create_link(GoLinkCreate(
        alias="github",
        target_url="https://github.com/my-org",
        title="GitHub Org"
    ))

    target = await service.resolve_redirect("github")
    assert target == "https://github.com/my-org"

    updated = await service.get_link_by_id(created.id)
    assert updated.clickCount == 1

@pytest.mark.asyncio
async def test_delete_link():
    repo = InMemoryLinkRepository(seed=False)
    service = LinkService(repo)

    created = await service.create_link(GoLinkCreate(
        alias="temp",
        target_url="https://temp.com",
        title="Temp Link"
    ))

    await service.delete_link(created.id)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_link_by_id(created.id)
    assert exc_info.value.status_code == 404
