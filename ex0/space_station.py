#!/usr/bin/env python3
"""Module for Exercise 0: Space Station Data validation using Pydantic."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Pydantic model representing space station data with validation."""

    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    """Demonstrate SpaceStation model creation and error handling."""
    print("Space Station Data Validation")
    print("========================================")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 10, 1, 12, 0),
            is_operational=True,
            notes="All systems operating within normal parameters.",
        )
        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        status = "Operational" if valid_station.is_operational else "Offline"
        print(f"Status: {status}")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="OVER01",
            name="Overcrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
