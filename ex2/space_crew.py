from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime
import random

class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)


    @model_validator(mode="after")
    def mission_validatin_rules(self) -> "SpaceMission":

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission id has to start with 'M'")

        if not any(m.rank in (Rank.captain, Rank.commander) for m in self.crew):
            raise ValueError("At least one captain or commander should be assigned")

        count = 0
        if self.duration_days >365:
            for member in self.crew:
                if member.years_experience >= 5:
                    count += 1
            if len(self.crew) / 2 > count:
                raise ValueError("More than the half of the member should have experienced for five years")

        for member in self.crew:
            if not member.is_active:
                raise ValueError("Some of members are inactive")

        return self


def create_crew(name: str, rank: Rank, specialization:str, experience: int) -> CrewMember:

    crew = CrewMember(
        member_id="000",
        name=name,
        rank=rank,
        age=random.randint(18, 80),
        specialization=specialization,
        years_experience=experience,
        is_active=True
    )

    return crew


def create_mission(crews: list[CrewMember]) -> SpaceMission:
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="MARS",
        duration_days=900,
        budget_millions=2500.0,
        crew = crews,
        mission_status="planned"
    )


if __name__ =="__main__":
    crews: list[CrewMember] = None

    crew = create_crew("Sarah Conner", "commander", "Mission command", 10)
    crews.append(crew)
    crew = create_crew("Jhon Smith", "lieutenant", "Navigation", 5)
    crews.append(crew)
    crew = create_crew("Alice Johnson", "officer", "Engineering", 3)
    crews.append(crew)

    mission = create_mission(crews)
    