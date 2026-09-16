from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime
from typing import Optional
import sys


class ConatactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlianContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ConatactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlianContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ConatactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ConatactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact rewuires at least 3 witnesses"
                )
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals should inclde received messages")

        return self


def create_instance() -> AlianContact:
    aliancontact = AlianContact(
        contact_id="AC_2024_001",
        timestamp="2024-01-01",
        location="Area 51, Nevada",
        contact_type="radio",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False,
    )

    return aliancontact


def create_invalid_instanve() -> AlianContact:
    try:
        aliancontact = AlianContact(
            contact_id="AC_2024_001",
            timestamp="2024-01-01",
            location="Area 51, Nevada",
            contact_type="telepathic",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
            is_verified=False,
        )

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
        sys.exit(1)

    return aliancontact


def show_info(aliancontact: AlianContact) -> None:
    print(
        f"ID: {aliancontact.contact_id}\n"
        f"Type: {aliancontact.contact_type}\n"
        f"Location: {aliancontact.location}\n"
        f"Signal: {aliancontact.signal_strength}/10\n"
        f"Duration: {aliancontact.duration_minutes} minutes\n"
        f"witness: {aliancontact.witness_count}\n"
        f"Message: {aliancontact.message_received}\n"
    )


if __name__ == "__main__":
    print("Alian Conatact Log Validation")
    print("============================================")
    print("Valid contact report:")
    aliancontact = create_instance()
    show_info(aliancontact)

    print("\n===========================================")
    print("Expected validation error:")
    aliancontact = create_invalid_instanve()
    show_info(aliancontact)
