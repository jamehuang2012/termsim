from typing import Any, TypeVar, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


class Party:
    def __init__(self, identification: str,  type: str,authentication_key: UUID = None,shortName:str = None) -> None:
        self.identification = identification
        self.authentication_key = authentication_key
        self.type = type
        self.shortName = shortName

    def to_dict(self) -> dict:
        return {
            "identification": self.identification,
            # if authentication_key is not None or emtpy, add it to the dictionary
            **({"authenticationKey": str(self.authentication_key)} if self.authentication_key else {}),
            "type": self.type,

            # if shortName is not None or emtpy, add it to the dictionary
            **({"shortName": self.shortName} if self.shortName else {})
        }


class Header:
    def __init__(
        self,
        message_function: str,
        protocol_version: str,
        exchange_identification: UUID,
        creation_date_time: Any,  # Allow both datetime and str
        initiating_party: Party,
        recipient_party: Party = None,
    ) -> None:
        self.message_function = message_function
        self.protocol_version = protocol_version
        self.exchange_identification = exchange_identification
        self.recipient_party = recipient_party
        
        # Parse string to datetime if necessary
        if isinstance(creation_date_time, str):
            self.creation_date_time = dateutil.parser.parse(creation_date_time)
        elif isinstance(creation_date_time, datetime):
            self.creation_date_time = creation_date_time
        else:
            raise TypeError("creation_date_time must be a datetime or a string")

        self.initiating_party = initiating_party

    def to_dict(self) -> dict:
        return {
            "messageFunction": self.message_function,
            "protocolVersion": self.protocol_version,
            "exchangeIdentification": str(self.exchange_identification),
            "creationDateTime": self.creation_date_time.isoformat(),
            "initiatingParty": self.initiating_party.to_dict(),
            # if recipient_party is not None, add it to the dictionary
            **({"recipientParty": self.recipient_party.to_dict()} if self.recipient_party is not None else {})

        }