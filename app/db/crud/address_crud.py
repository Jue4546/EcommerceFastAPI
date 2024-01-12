from typing import List

from sqlalchemy import text

from app.db.base import SessionLocal
from app.models.address_model import Address, AddressCreate, AddressUpdate


def create_address_db(address_create: AddressCreate) -> Address:
    db = SessionLocal()
    insert_query = text(
        'INSERT INTO "address" (user_id, province_or_state, city, district, street, detail, postal_code, is_default) '
        'VALUES (:user_id, :province_or_state, :city, :district, :street, :detail, :postal_code, :is_default) RETURNING *'
    )
    db_address = db.execute(
        insert_query,
        {
            'user_id': address_create.user_id,
            'province_or_state': address_create.province_or_state,
            'city': address_create.city,
            'district': address_create.district,
            'street': address_create.street,
            'detail': address_create.detail,
            'postal_code': address_create.postal_code,
            'is_default': address_create.is_default,
        },
    ).fetchone()
    db.commit()
    db.close()
    return Address(
        id=db_address[0],
        user_id=db_address[1],
        province_or_state=db_address[2],
        city=db_address[3],
        street=db_address[4],
        postal_code=db_address[5],
        is_default=db_address[6],
        district=db_address[7],
        detail=db_address[8]
    )


def get_address_db(address_id: int, user_id: int) -> Address:
    db = SessionLocal()
    select_query = text('SELECT id, user_id, province_or_state, city, district, street, detail, postal_code, is_default '
                        'FROM "address" WHERE id = :address_id AND user_id = :user_id')
    db_address = db.execute(select_query, {'address_id': address_id, 'user_id': user_id}).fetchone()
    db.close()
    if db_address:
        return Address(
            id=db_address[0],
            user_id=db_address[1],
            province_or_state=db_address[2],
            city=db_address[3],
            district=db_address[4],
            street=db_address[5],
            detail=db_address[6],
            postal_code=db_address[7],
            is_default=db_address[8]
        )
    else:
        return None


def get_addresses_db(user_id: int, skip: int = 0, limit: int = 10) -> List[Address]:
    db = SessionLocal()
    select_all_query = text('SELECT id, user_id, province_or_state, city, district, street, detail, postal_code, is_default '
                            'FROM "address" WHERE user_id = :user_id LIMIT :limit OFFSET :skip')
    addresses_data = db.execute(select_all_query, {'limit': limit, 'skip': skip, 'user_id': user_id}).fetchall()
    db.close()
    addresses_db = [
        Address(
            id=address_tuple[0],
            user_id=address_tuple[1],
            province_or_state=address_tuple[2],
            city=address_tuple[3],
            district=address_tuple[4],
            street=address_tuple[5],
            detail=address_tuple[6],
            postal_code=address_tuple[7],
            is_default=address_tuple[8],
        )
        for address_tuple in addresses_data
    ]
    return addresses_db


def update_address_db(address_id: int, address_update: AddressUpdate) -> Address:
    db = SessionLocal()
    update_query = text('UPDATE "address" SET province_or_state = :province_or_state, city = :city, '
                        'district = :district, street = :street, detail = :detail, postal_code = :postal_code, '
                        'is_default = :is_default WHERE id = :address_id AND user_id = :user_id RETURNING *')
    db_address = db.execute(
        update_query,
        {
            'province_or_state': address_update.province_or_state,
            'city': address_update.city,
            'district': address_update.district,
            'street': address_update.street,
            'detail': address_update.detail,
            'postal_code': address_update.postal_code,
            'is_default': address_update.is_default,
            'address_id': address_id,
            'user_id': address_update.user_id,
        },
    ).fetchone()
    db.commit()
    db.close()
    if db_address:
        return Address(
            id=db_address[0],
            user_id=db_address[1],
            province_or_state=db_address[2],
            city=db_address[3],
            street=db_address[4],
            postal_code=db_address[5],
            is_default=db_address[6],
            district=db_address[7],
            detail=db_address[8]
        )
    else:
        return None


def delete_address_db(address_id: int) -> Address:
    db = SessionLocal()
    delete_query = text('DELETE FROM "address" WHERE id = :address_id RETURNING *')
    db_address = db.execute(delete_query, {'address_id': address_id}).fetchone()
    db.commit()
    db.close()
    if db_address:
        return Address(
            id=db_address[0],
            user_id=db_address[1],
            province_or_state=db_address[2],
            city=db_address[3],
            street=db_address[4],
            postal_code=db_address[5],
            is_default=db_address[6],
            district=db_address[7],
            detail=db_address[8]
        )
    else:
        return None
