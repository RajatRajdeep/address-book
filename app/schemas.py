from typing import Union

from pydantic import BaseModel, confloat, root_validator


def round_off_locations(_, values):
    """
    This function rounds off latitude and longitudes present in Address Model.
    """
    if values.get("latitude") is not None:
        values["latitude"] = round(values["latitude"], 4)
    if values.get("longitude", None) is not None:
        values["longitude"] = round(values["longitude"], 4)
    return values


class AddressBase(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class AddressCreate(AddressBase):
    pass

    _round_off_locations = root_validator(allow_reuse=True, skip_on_failure=True)(
        round_off_locations
    )


class AddressUpdate(BaseModel):
    latitude: Union[confloat(ge=-90, le=90), None]
    longitude: Union[confloat(ge=-180, le=180), None]

    _round_off_locations = root_validator(allow_reuse=True, skip_on_failure=True)(
        round_off_locations
    )


class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True
