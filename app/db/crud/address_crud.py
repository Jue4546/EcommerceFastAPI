from sqlalchemy.orm import Session
from app.models import user_model


def create_address(db: Session, address_data: user_model.AddressCreate, user_id: int):
    db_address = user_model.Address(**address_data.model_dump(), user_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address(db: Session, user_id: int):
    return db.query(user_model.Address).filter(user_model.Address.user_id == user_id).all()


def get_default_address(db: Session, user_id: int):
    return db.query(user_model.Address).filter(user_model.Address.user_id == user_id,
                                               user_model.Address.is_default == True).first()
