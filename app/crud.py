from sqlalchemy.orm import Session

from . import models, schemas


def get_address(db: Session, address_id: int):
    return (
        db.query(models.Address)
        .filter(models.Address.id == address_id, models.Address.is_deleted == False)
        .first()
    )


def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Address)
        .filter(models.Address.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = get_address(db, address_id)
    address_data = address.dict(exclude_unset=True)
    for key, value in address_data.items():
        setattr(db_address, key, value)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    setattr(db_address, "is_deleted", True)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return None
