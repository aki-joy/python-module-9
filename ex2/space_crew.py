from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


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
    def mission_validation_rules(self) -> "SpaceMission":

        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if (not any(m.rank in (Rank.captain, Rank.commander)
                    for m in self.crew)):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )

        count = 0
        if self.duration_days > 365:
            for member in self.crew:
                if member.years_experience >= 5:
                    count += 1
            if len(self.crew) / 2 > count:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew "
                    "(5+ years)"
                    )

        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")

        return self


def create_crew(
    name: str, rank: Rank, specialization: str, experience: int
) -> CrewMember:

    crew = CrewMember(
        member_id="000",
        name=name,
        rank=rank,
        age=20,
        specialization=specialization,
        years_experience=experience,
        is_active=True,
    )

    return crew


def create_mission(crews: list[CrewMember]) -> SpaceMission:
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        budget_millions=2500.0,
        crew=crews,
        mission_status="planned",
    )

    return mission


def show_info(mission: SpaceMission) -> None:
    print(
        f"Mission: {mission.mission_name}\n"
        f"ID: {mission.mission_id}\n"
        f"Destination: {mission.destination}\n"
        f"Duration: {mission.duration_days} days\n"
        f"Budget: ${mission.budget_millions}M\n"
        f"Crew size: {len(mission.crew)}\n"
        "Crew members:"
    )

    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )


def main() -> None:
    print("Space Mission Crew Validation")

    crews: list[CrewMember] = []

    try:
        crew1 = create_crew(
            "Sarah Connor", Rank.commander, "Mission Command", 1
            )
        crews.append(crew1)
        crew2 = create_crew("John Smith", Rank.lieutenant, "Navigation", 5)
        crews.append(crew2)
        crew3 = create_crew("Alice Johnson", Rank.officer, "Engineering", 3)
        crews.append(crew3)

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))
        return

    print("=========================================")
    print("Valid mission created:")

    try:
        mission = create_mission(crews)

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))
        return

    show_info(mission)

    print("\n=========================================")
    print("Expected validation error:")
    crews.pop(0)

    try:
        invalid_mission = create_mission(crews)

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].removeprefix("Value error, "))
        return

    show_info(invalid_mission)


if __name__ == "__main__":
    main()
