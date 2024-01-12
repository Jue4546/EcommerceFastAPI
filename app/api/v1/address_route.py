"""收货地址模块路由：api/address_route.py"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.models.address_model import Address, AddressCreate, AddressUpdate
from app.services import address_service, auth_service
from models.user_model import UserInDB

router = APIRouter()


@router.post("/addresses", tags=["地址管理"], response_model=Address)
async def create_address(address_create: AddressCreate, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    if not current_user.is_admin and current_user != address_create.user_id:
        address_create.user_id = current_user.id
    return address_service.create_address(address_create)


@router.get("/addresses/{address_id}", tags=["地址管理"], response_model=Address)
async def read_address(address_id: int, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    address = address_service.get_address(address_id, current_user.id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.get("/addresses", tags=["地址管理"], response_model=List[Address])
async def read_addresses(skip: int = 0, limit: int = 10, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    return address_service.get_addresses(current_user.id, skip=skip, limit=limit)


@router.put("/addresses/{address_id}", tags=["地址管理"], response_model=Address)
async def update_address(
    address_id: int, address_update: AddressUpdate, current_user: UserInDB = Depends(auth_service.get_current_user_db)
):
    if not current_user.is_admin and current_user != address_update.user_id:
        address_update.user_id = current_user.id
    updated_address = address_service.update_address(address_id, address_update)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address


@router.delete("/addresses/{address_id}", tags=["地址管理"], response_model=Address)
async def delete_address(address_id: int, current_user: UserInDB = Depends(auth_service.get_current_user_db)):
    if current_user.is_admin:
        deleted_address = address_service.delete_address_admin(address_id)
    else:
        deleted_address = address_service.delete_address(address_id, current_user.id)
    if not deleted_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return deleted_address
