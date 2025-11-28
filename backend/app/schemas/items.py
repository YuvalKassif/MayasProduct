from __future__ import annotations

from pydantic import BaseModel, Field


class ItemImageOut(BaseModel):
    id: str
    original_key: str
    thumb_key: str | None = None
    medium_key: str | None = None
    width: int | None = None
    height: int | None = None
    sort_order: int


class ItemCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str | None = None
    category: str
    brand: str | None = None
    size: str | None = None
    condition: str
    price_cents: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    location_city: str | None = None
    location_country: str | None = None


class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None
    category: str | None = None
    brand: str | None = None
    size: str | None = None
    condition: str | None = None
    price_cents: int | None = Field(default=None, ge=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    location_city: str | None = None
    location_country: str | None = None
    status: str | None = None


class ItemOut(BaseModel):
    id: str
    seller_id: str
    title: str
    description: str | None
    category: str
    brand: str | None
    size: str | None
    condition: str
    price_cents: int
    currency: str
    location_city: str | None
    location_country: str | None
    status: str
    images: list[ItemImageOut] = []


class ItemsListOut(BaseModel):
    items: list[ItemOut]
    total: int
