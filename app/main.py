import logging

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import confloat, conint
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine
from .messages import ERRORS, SUCCESS_MESSAGE

models.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Address", "description": "This contains all the Address APIs"},
]


app = FastAPI(
    title="Address Book APIs",
    description="This contains the documentation of all the Address Book APIs.",
    version="0.0.1",
    openapi_tags=tags_metadata,
)


def get_db():
    """
    Dependency function to retrieve db session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/addresses/",
    response_model=list[schemas.Address],
    summary="To retrieve all addresses present in the system.",
    status_code=status.HTTP_200_OK,
    tags=["Address"],
)
def fetch_addresses(
    skip: conint(ge=0) = 0, limit: conint(ge=1) = 100, db: Session = Depends(get_db)
):
    """
    This api returns all the addresses present in the system.
    ---
    Args:

        skip: Number of rows to skip.
        limit: Number of rows to return.

    Returns:

        Json object: List of addresses.
    """
    try:
        logging.info("fetch_addresses method initialized.")
        return crud.get_addresses(db, skip, limit)
    except Exception:
        logging.exception("Exception occurred while fetching the addresses.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


@app.get(
    "/addresses/{address_id}",
    response_model=schemas.Address,
    summary="To retrieve specific address present in the system.",
    status_code=status.HTTP_200_OK,
    tags=["Address"],
)
def fetch_address(address_id: int, db: Session = Depends(get_db)):
    """
    This api retrieves an address entity present in the system by address id.
    ---
    Args:

        address_id: Address unique id.

    Returns:

        Json object: Address entity.
    """
    try:
        logging.info(
            "fetch_address method initialized for following address #{}.".format(
                address_id
            )
        )
        address = crud.get_address(db, address_id)
        if not address:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": ERRORS["ADDRESS_NOT_PRESENT_ERROR"]},
            )
        return address
    except Exception:
        logging.exception(
            "Exception occurred while fetching the following address #{}".format(
                address_id
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


@app.post(
    "/addresses/",
    response_model=schemas.Address,
    summary="To create address entity in the system.",
    status_code=status.HTTP_201_CREATED,
    tags=["Address"],
)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    This api create address entity in the system and returns it.
    ---

    Args:
        address: Address entity data.

    Returns:

        Json object: Created address entity.
    """
    try:
        logging.info("create_address method initialized.")
        return crud.create_address(db, address)
    except Exception:
        logging.exception("Exception occurred while creating the address entity.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


@app.put(
    "/addresses/{address_id}",
    response_model=schemas.Address,
    summary="To update specific address entity present in the system.",
    status_code=status.HTTP_200_OK,
    tags=["Address"],
)
def update_address(
    address_id: int, address_out: schemas.AddressUpdate, db: Session = Depends(get_db)
):
    """
    This api allows user to update an address entity present in the system.
    ---
    Args:

        address_id: Address unique id.
        address: Address entity data.

    Returns:

        Json object: Returns updated address entity.
    """
    try:
        logging.info(
            "update_address method initialized for following address #{}.".format(
                address_id
            )
        )
        address = crud.get_address(db, address_id)
        if not address:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": ERRORS["ADDRESS_NOT_PRESENT_ERROR"]},
            )
        return crud.update_address(db, address_id, address_out)
    except Exception:
        logging.exception(
            "Exception occurred while updating the following address entity #{}".format(
                address_id
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


@app.delete(
    "/addresses/{address_id}",
    summary="To delete specific address entity present in the system.",
    status_code=status.HTTP_200_OK,
    tags=["Address"],
)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    This api allows user to delete an address entity present in the system.
    ---
    Args:

        address_id: Address unique id.

    """
    try:
        logging.info(
            "delete_address method initialized for following address #{}.".format(
                address_id
            )
        )
        address = crud.get_address(db, address_id)
        if not address:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": ERRORS["ADDRESS_NOT_PRESENT_ERROR"]},
            )
        crud.delete_address(db, address_id)
        return {
            "address_id": address_id,
            "detail": SUCCESS_MESSAGE["ADDRESS_DELETED_SUCCESS"],
        }
    except Exception:
        logging.exception(
            "Exception occurred while deleting the following address entity #{}".format(
                address_id
            )
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


@app.get(
    "/addresses/nearby/",
    response_model=list[schemas.Address],
    summary="To retrieve the addresses that are within a given distance of provided location coordinates.",
    status_code=status.HTTP_200_OK,
    tags=["Address"],
)
def fetch_nearby_addresses(
    latitude: confloat(ge=-90, le=90),
    longitude: confloat(ge=-180, le=180),
    distance: conint(ge=0),
    db: Session = Depends(get_db),
):
    """
    This api returns all the addresses that are within a given distance of provided location coordinates.
    ---
    Args:

        latitude: geographic coordinate.
        longitude: geographic coordinate.
        distance: length from coordinate (in km).

    Returns:

        Json object: Returns list of addresses.
    """
    try:
        logging.info("fetch_nearby_addresses method initialized.")
        return crud.get_addresses(db, skip=0, limit=100)
    except Exception:
        logging.exception("Exception occurred while fetching the nearby addresses.")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ERRORS["INTERNAL_SERVER_ERROR"]},
        )


#
