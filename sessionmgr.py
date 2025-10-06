from typing import Any, TypeVar, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser

from Header import Header, Party

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()



class POIGroupIdentification:
    def __init__(self, exchange_action: str,exchange_identification:str) -> None:
        self.exchange_action = exchange_action
        self.exchange_identification = exchange_identification

    # exchange_identification might be None , if None then it will not be included in the dict
    def to_dict(self) -> dict:
        if self.exchange_identification:
            return {
                "exchangeAction": self.exchange_action,
                "exchangeIdentification": str(self.exchange_identification),
            }
        else:
            return {
                "exchangeAction": self.exchange_action,
            }


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

class TransactionInProcess:
    transaction_status: str
    cancel_status: str
    exchange_identification: str

    def __init__(self, transaction_status: str, cancel_status: str, exchange_identification: str) -> None:
        self.transaction_status = transaction_status
        self.cancel_status = cancel_status
        self.exchange_identification = exchange_identification


class SessionManagementResponse:
    session_response: SessionResponse
    transaction_in_process: TransactionInProcess

    def __init__(self, session_response: SessionResponse, transaction_in_process: TransactionInProcess) -> None:
        self.session_response = session_response
        self.transaction_in_process = transaction_in_process


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


# Updated function to parse OCsessionManagementResponse with optional transactionInProcess
def parse_ocsession_management_response(data: dict) -> OCsessionManagementResponse:
    # Parse Header
    header_data = data["header"]
    header = Header(
        message_function=header_data["messageFunction"],
        protocol_version=header_data["protocolVersion"],
        exchange_identification=UUID(header_data["exchangeIdentification"]),
        creation_date_time=header_data["creationDateTime"],
        initiating_party=Party(
            identification=header_data["initiatingParty"]["identification"],
            authentication_key=UUID(header_data["initiatingParty"]["authenticationKey"]),
            type=header_data["initiatingParty"]["type"]
        )
    )
    
    # Parse SessionResponse
    session_response_data = data["sessionManagementResponse"]["sessionResponse"]
    session_response = SessionResponse(response=session_response_data["response"])

    # Check if transactionInProcess exists
    transaction_data = data["sessionManagementResponse"].get("transactionInProcess")
    transaction_in_process = None
    if transaction_data:
        transaction_in_process = TransactionInProcess(
            transaction_status=transaction_data.get("transactionStatus", "N/A"),

            cancel_status=transaction_data.get("cancelStatus", "N/A"),
            exchange_identification=UUID(transaction_data["exchangeIdentification"])
        )

    # Create SessionManagementResponse instance
    session_management_response = SessionManagementResponse(
        session_response=session_response,
        transaction_in_process=transaction_in_process  # Allow None
    )

    # Return final OCsessionManagementResponse
    return OCsessionManagementResponse(
        header=header,
        session_management_response=session_management_response
    )