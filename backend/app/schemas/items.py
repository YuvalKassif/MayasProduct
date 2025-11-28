from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class ItemImageOut(BaseModel):
    id: str
    original_key: str
    thumb_key: Optional[str] = None
    medium_key: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int


class ItemCreate(BaseModel):
    title: str = Field(max_length=200)
    description: Optional[str] = None
    category: str
    brand: Optional[str] = None
    size: Optional[str] = None
    condition: str
    price_cents: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    location_city: Optional[str] = None
    location_country: Optional[str] = None


class ItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    condition: Optional[str] = None
    price_cents: Optional[int] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    status: Optional[str] = None


class ItemOut(BaseModel):
    id: str
    seller_id: str
    title: str
    description: Optional[str]
    category: str
    brand: Optional[str]
    size: Optional[str]
    condition: str
    price_cents: int
    currency: str
    location_city: Optional[str]
    location_country: Optional[str]
    status: str
    images: list[ItemImageOut] = []


class ItemsListOut(BaseModel):
    items: list[ItemOut]
    total: int

