from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import base
from app.services import address_service
from app.models import user_model

router = APIRouter()


@router.post("/address")
def create_address(
        address_data: user_model.AddressCreate,
        db: Session = Depends(base.get_db),
        # current_user: User = Depends(get_current_user),
):
    return address_service.create_address(db, address_data)


@router.get("/address", response_model=list[user_model.Address])
def get_addresses(
        db: Session = Depends(base.get_db),
        current_user: user_model.User = Depends(base.get_current_user),
):
    return address_service.get_addresses(db, current_user.id)


@router.get("/address/default", response_model=user_model.Address)
def get_default_address(
        db: Session = Depends(base.get_db),
        current_user: user_model.User = Depends(base.get_current_user),
):
    return address_service.get_default_address(db, current_user.id)
