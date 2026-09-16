from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime
from typing import Optional
import sys


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError("Strong signals should include received messages")

        return self


def create_instance() -> AlienContact:
    try:
        aliencontact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 1, 1),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=False,
        )

    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
        sys.exit(1)

    return aliencontact


def create_invalid_instance() -> AlienContact:
    try:
        aliencontact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 1, 1),
            location="Area 51, Nevada",
            contact_type=ContactType.telepathic,
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

    return aliencontact


def show_info(aliencontact: AlienContact) -> None:
    print(
        f"ID: {aliencontact.contact_id}\n"
        f"Type: {aliencontact.contact_type.value}\n"
        f"Location: {aliencontact.location}\n"
        f"Signal: {aliencontact.signal_strength}/10\n"
        f"Duration: {aliencontact.duration_minutes} minutes\n"
        f"Witnesses: {aliencontact.witness_count}\n"
        f"Message: {aliencontact.message_received}\n"
    )


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("============================================")
    print("Valid contact report:")
    aliencontact = create_instance()
    show_info(aliencontact)

    print("\n===========================================")
    print("Expected validation error:")
    aliencontact = create_invalid_instance()
    show_info(aliencontact)
