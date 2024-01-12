"""收货地址服务逻辑：service/address_service.py"""
from typing import List

from app.models.address_model import Address, AddressCreate, AddressUpdate
from app.db.crud.address_crud import create_address_db, get_address_db, get_addresses_db, update_address_db, \
    delete_address_db


def create_address(address_create: AddressCreate) -> Address:
    return create_address_db(address_create)


def get_address(address_id: int, user_id: int) -> Address:
    return get_address_db(address_id, user_id)


def get_addresses(user_id: int, skip: int = 0, limit: int = 10) -> List[Address]:
    return get_addresses_db(user_id, skip=skip, limit=limit)


def update_address(address_id: int, address_update: AddressUpdate) -> Address:
    return update_address_db(address_id, address_update)


def delete_address_admin(address_id: int) -> Address:
    return delete_address_db(address_id)


def get_default_address_id(user_id: int) -> int:
    addresses = get_addresses(user_id)
    for address in addresses:
        if address.is_default:
            return address.id
    return addresses[0].id


def delete_address(address_id: int, user_id: int) -> Address:
    address = get_address_db(address_id, user_id)
    if address:
        return delete_address_db(address_id)
    else:
        return None
