from typing import Any, TypeVar, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class InitiatingParty:
    def __init__(self, identification: str, authentication_key: UUID, type: str) -> None:
        self.identification = identification
        self.authentication_key = authentication_key
        self.type = type

    def to_dict(self) -> dict:
        return {
            "identification": self.identification,
            "authenticationKey": str(self.authentication_key),
            "type": self.type,
        }


class Header:
    def __init__(
        self,
        message_function: str,
        protocol_version: str,
        exchange_identification: UUID,
        creation_date_time: Any,  # Allow both datetime and str
        initiating_party: InitiatingParty,
    ) -> None:
        self.message_function = message_function
        self.protocol_version = protocol_version
        self.exchange_identification = exchange_identification
        
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
        }


class POIGroupIdentification:
    def __init__(self, exchange_action: str) -> None:
        self.exchange_action = exchange_action

    def to_dict(self) -> dict:
        return {"exchangeAction": self.exchange_action}


class POIComponent:
    def __init__(self, poi_group_identification: POIGroupIdentification, state: str) -> None:
        self.poi_group_identification = poi_group_identification
        self.state = state

    def to_dict(self) -> dict:
        return {
            "POIGroupIdentification": self.poi_group_identification.to_dict(),
            "state": self.state,
        }


class SessionManagementRequest:
    def __init__(self, poi_component: POIComponent) -> None:
        self.poi_component = poi_component

    def to_dict(self) -> dict:
        return {"POIComponent": self.poi_component.to_dict()}


class OCsessionManagementRequest:
    def __init__(self, header: Header, session_management_request: SessionManagementRequest) -> None:
        self.header = header
        self.session_management_request = session_management_request

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "sessionManagementRequest": self.session_management_request.to_dict(),
        }



class SessionResponse:
    response: str

    def __init__(self, response: str) -> None:
        self.response = response


class SessionManagementResponse:
    session_response: SessionResponse

    def __init__(self, session_response: SessionResponse) -> None:
        self.session_response = session_response


class OCsessionManagementResponse:
    header: Header
    session_management_response: SessionManagementResponse

    def __init__(self, header: Header, session_management_response: SessionManagementResponse) -> None:
        self.header = header
        self.session_management_response = session_management_response




class Request:
    def __init__(self, o_csession_management_request: OCsessionManagementRequest) -> None:
        self.o_csession_management_request = o_csession_management_request

    def to_dict(self) -> dict:
        return {
            "OCsessionManagementRequest": self.o_csession_management_request.to_dict(),
        }
