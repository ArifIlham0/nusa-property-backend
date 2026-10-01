from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Property
from ..schemas import (
    PropertyItemSchema,
    PropertyCreateSchema,
    ToggleFavoriteResponse
)
from ..utils import format_rupiah

router = APIRouter(prefix="/api/properties", tags=["Properties"])


@router.get("", response_model=List[PropertyItemSchema])
def get_properties(
    tag_type: Optional[str] = Query(None, description="Filter by tagType: SUBSIDI, PROMO, DISCOUNT"),
    is_favorite: Optional[bool] = Query(None, description="Filter by favorite status"),
    search: Optional[str] = Query(None, description="Search by title or location"),
    db: Session = Depends(get_db)
):
    query = db.query(Property).filter(Property.is_featured == False)
    if tag_type:
        query = query.filter(Property.tag_type == tag_type.upper())
    if is_favorite is not None:
        query = query.filter(Property.is_favorite == is_favorite)
    if search:
        query = query.filter(
            Property.title.ilike(f"%{search}%") | Property.location.ilike(f"%{search}%")
        )
    return query.order_by(Property.price.asc()).all()


@router.get("/featured", response_model=PropertyItemSchema)
def get_featured_property(db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.is_featured == True).first()
    if not prop:
        prop = db.query(Property).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Featured property not found")
    return prop


@router.get("/{property_id}", response_model=PropertyItemSchema)
def get_property_by_id(property_id: str, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")
    return prop


@router.post("", response_model=PropertyItemSchema)
def create_property(payload: PropertyCreateSchema, db: Session = Depends(get_db)):
    prop_id = payload.id
    if not prop_id:
        count = db.query(Property).count()
        prop_id = f"prop_{count + 1}"
        while db.query(Property).filter(Property.id == prop_id).first():
            count += 1
            prop_id = f"prop_{count + 1}"
    else:
        existing = db.query(Property).filter(Property.id == prop_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Property ID already exists")

    price_formatted = format_rupiah(payload.price)
    installment_est = f"Cicilan mulai Rp {payload.price // 150_000_000},5 Jt/bln"

    new_prop = Property(
        id=prop_id,
        title=payload.title,
        location=payload.location,
        price=payload.price,
        price_formatted=price_formatted,
        installment_estimate=installment_est,
        bedrooms=payload.bedrooms,
        bathrooms=payload.bathrooms,
        carports=payload.carports,
        building_area=payload.building_area,
        surface_area=payload.surface_area,
        electricity_va=payload.electricity_va,
        certificate_type=payload.certificate_type,
        tag_text=payload.tag_text,
        tag_type=payload.tag_type.upper(),
        image_url=payload.image_url,
        developer_name=payload.developer_name,
        address_detail=payload.address_detail,
        is_favorite=False,
        is_featured=payload.is_featured
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    return new_prop


@router.patch("/{property_id}/favorite", response_model=ToggleFavoriteResponse)
def toggle_favorite(
    property_id: str,
    favorite: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property {property_id} not found")

    if favorite is not None:
        prop.is_favorite = favorite
    else:
        prop.is_favorite = not prop.is_favorite

    db.commit()
    db.refresh(prop)

    status_msg = (
        f"Disimpan ke favorit: {prop.title}"
        if prop.is_favorite
        else f"Dihapus dari favorit: {prop.title}"
    )
    return ToggleFavoriteResponse(
        id=prop.id,
        isFavorite=prop.is_favorite,
        message=status_msg
    )
