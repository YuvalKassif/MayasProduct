from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_session
from ..models.item import Item
from ..schemas.items import ItemCreate, ItemOut, ItemUpdate, ItemsListOut
from ..security.deps import get_current_user_id


router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: ItemCreate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    item = Item(
        seller_id=user_id,
        title=payload.title,
        description=payload.description,
        category=payload.category,
        brand=payload.brand,
        size=payload.size,
        condition=payload.condition,
        price_cents=payload.price_cents,
        currency=payload.currency,
        location_city=payload.location_city,
        location_country=payload.location_country,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return await _to_item_out(item, session)


@router.get("/{item_id}", response_model=ItemOut)
async def get_item(item_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await _to_item_out(item, session)


@router.get("", response_model=ItemsListOut)
async def list_items(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    seller_id: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    q = select(Item)
    if seller_id:
        q = q.where(Item.seller_id == seller_id)
    q = q.order_by(Item.created_at.desc()).limit(limit).offset(offset)
    rows = (await session.execute(q)).scalars().all()

    total_q = select(func.count()).select_from(Item)
    if seller_id:
        total_q = total_q.where(Item.seller_id == seller_id)
    total = (await session.execute(total_q)).scalar_one()

    items = [await _to_item_out(i, session) for i in rows]
    return {"items": items, "total": total}


@router.patch("/{item_id}", response_model=ItemOut)
async def update_item(
    item_id: str,
    payload: ItemUpdate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.seller_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    await session.commit()
    await session.refresh(item)
    return await _to_item_out(item, session)


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.seller_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await session.delete(item)
    await session.commit()
    return None


async def _to_item_out(item: Item, session: AsyncSession) -> ItemOut:
    # images stub (none yet). In future, eager load relationships for performance.
    return ItemOut(
        id=item.id,
        seller_id=item.seller_id,
        title=item.title,
        description=item.description,
        category=item.category,
        brand=item.brand,
        size=item.size,
        condition=item.condition,
        price_cents=item.price_cents,
        currency=item.currency,
        location_city=item.location_city,
        location_country=item.location_country,
        status=item.status,
        images=[],
    )

