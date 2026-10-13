#!/usr/bin/env python3
"""Module for Exercise 2: Space Crew Management with nested models."""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Enum representing crew member ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Pydantic model representing a space crew member."""

    member_id: str = Field(..., min_length=3, max_length=15)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=2, max_length=50)
    years_of_experience: int = Field(..., ge=0, le=60)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """Pydantic model for space mission with nested crew validation."""

    mission_id: str = Field(..., min_length=3, max_length=15)
    mission_name: str = Field(..., min_length=2, max_length=100)
    destination: str = Field(..., min_length=2, max_length=100)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        """Validate custom rules for space mission and crew composition."""
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader: bool = any(
            m.rank in (Rank.COMMANDER, Rank.CAPTAIN) for m in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must contain at least one Captain or Commander"
            )

        inactive_members = [m for m in self.crew if not m.is_active]
        if inactive_members:
            raise ValueError("All crew members in the mission must be active")

        if self.duration_days > 365:
            experienced_count = sum(
                1 for m in self.crew if m.years_of_experience >= 5
            )
            required_count = len(self.crew) / 2.0
            if experienced_count < required_count:
                raise ValueError(
                    "Long missions (>365 days) require at least 50% "
                    "of the crew to have 5+ years of experience"
                )

        return self


def main() -> None:
    """Demonstrate SpaceMission model validation and error handling."""
    print("Space Mission & Crew Validation")
    print("========================================")

    try:
        commander = CrewMember(
            member_id="CREW001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=42,
            specialization="Command & Navigation",
            years_of_experience=15,
            is_active=True,
        )
        pilot = CrewMember(
            member_id="CREW002",
            name="John Miller",
            rank=Rank.OFFICER,
            age=29,
            specialization="Piloting",
            years_of_experience=6,
            is_active=True,
        )

        valid_mission = SpaceMission(
            mission_id="M_ARES_01",
            mission_name="Ares One Mars Exploration",
            destination="Mars",
            duration_days=500,
            crew=[commander, pilot],
        )

        print("Valid mission created:")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Name: {valid_mission.mission_name}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Crew size: {len(valid_mission.crew)} members")
        for member in valid_mission.crew:
            print(f"  - {member.name} ({member.rank.value.title()})")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}")

    print("========================================")
    print("Expected validation error (No Commander/Captain):")

    try:
        cadet = CrewMember(
            member_id="CREW003",
            name="Alex Vance",
            rank=Rank.CADET,
            age=22,
            specialization="Engineering",
            years_of_experience=1,
            is_active=True,
        )
        SpaceMission(
            mission_id="M_LUNA_02",
            mission_name="Lunar Base Resupply",
            destination="Moon",
            duration_days=30,
            crew=[cadet],
        )
    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
