import math

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


def distance_in_km(latitude1, longitude1, latitude2, longitude2):
    # Earth's radius in kilometers
    R = 6371

    # Convert latitude and longitude to radians
    latitude1_rad, longitude1_rad = math.radians(latitude1), math.radians(longitude1)
    latitude2_rad, longitude2_rad = math.radians(latitude2), math.radians(longitude2)

    # Calculate the differences in latitude and longitude
    delta_latitude = latitude2_rad - latitude1_rad
    delta_longitude = longitude2_rad - longitude1_rad

    # Apply the Haversine formula
    a = (
        math.sin(delta_latitude / 2) ** 2
        + math.cos(latitude1_rad)
        * math.cos(latitude2_rad)
        * math.sin(delta_longitude / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def get_nearby_addresses(db: Session, latitude: float, longitude: float, distance: int):
    total_addresses = (
        db.query(models.Address).filter(models.Address.is_deleted == False).all()
    )
    res_addresses = []
    for address in total_addresses:
        if (
            distance_in_km(latitude, longitude, address.latitude, address.longitude)
            <= distance
        ):
            res_addresses.append(address)
    return res_addresses
