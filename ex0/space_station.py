from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional
import sys


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def create_instance() -> SpaceStation:
    try:
        spacestation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-09-09",
            is_operational=False,
            notes="hello"
        )

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
        sys.exit(1)
    return spacestation


def create_invalid_instance() -> SpaceStation:
    try:
        spacestation = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-09-09",
            is_operational=False,
            notes=None
        )
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
        sys.exit(1)

    return spacestation


def show_info(spacestation: SpaceStation) -> None:
    print(
        f"ID: {spacestation.station_id}\n"
        f"Name: {spacestation.name}\n"
        f"Crew: {spacestation.crew_size} people\n"
        f"Power: {spacestation.power_level} %\n"
        f"Oxygen: {spacestation.oxygen_level} %"
    )

    if spacestation.is_operational is True:
        print("Status: Operational")
    else:
        print("Status: Inoperational")

    if spacestation.notes is not None:
        print(f"Notes:\n{spacestation.notes}")


if __name__ == "__main__":

    print("Space Station Data Validation")
    print("======================================")
    print("Valid station created:")
    spacestation = create_instance()
    show_info(spacestation)

    print("\n======================================")
    print("Expected validation error")
    invalid_spacestation = create_invalid_instance()
    show_info(invalid_spacestation)
