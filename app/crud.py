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


def get_range_of_coordinates(latitude: float, longitude: float, distance: int):
    # Earth's radius in kilometers
    R = 6371

    # Convert latitude and longitude to radians
    latitude_rad = math.radians(latitude)
    longitude_rad = math.radians(longitude)

    # Convert distance from kilometers to radians
    dist_rad = distance / R

    # Calculate minimum and maximum latitude values
    min_latitude = math.degrees(latitude_rad - dist_rad)
    max_latitude = math.degrees(latitude_rad + dist_rad)

    # Calculate minimum and maximum longitude values
    delta_longitude = math.asin(math.sin(dist_rad) / math.cos(latitude_rad))
    min_longitude = math.degrees(longitude_rad - delta_longitude)
    max_longitude = math.degrees(longitude_rad + delta_longitude)

    return (
        min_latitude,
        max_latitude,
        min_longitude,
        max_longitude,
    )


def get_nearby_addresses(db: Session, latitude: float, longitude: float, distance: int):
    min_latitude, max_latitude, min_longitude, max_longitude = get_range_of_coordinates(
        latitude, longitude, distance
    )
    return (
        db.query(models.Address)
        .filter(
            models.Address.is_deleted == False,
            min_latitude <= models.Address.latitude,
            models.Address.latitude <= max_latitude,
            min_longitude <= models.Address.longitude,
            models.Address.longitude <= max_longitude,
        )
        .all()
    )
