from sqlalchemy.orm import Session
from app.db.crud import address_crud
from app.models import user_model


def create_address(db: Session, address_data: user_model.AddressCreate, user_id: int):
    return address_crud.create_address(db, address_data, user_id)


def get_address(db: Session, address_id: int):
    return address_crud.get_address(db, address_id)


def get_default_address(db: Session, user_id: int, address_curd=None):
    return address_curd.get_default_address(db, user_id)
