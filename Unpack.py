import json
import struct

from FIFOStatusSender import FIFOStatusSender
import LoggerManager
from ServiceRequest import ParseServiceRequest
import StringUtily
from TransactionData import TransactionData
from monitor import log_monitor
from sessionmgr import parse_ocsession_management_response


def parseResponse(packed_data):
    # Step 1: Extract the length of the request (first 4 bytes)
    total_length = struct.unpack('>I', packed_data[:4])[0]
    
    # Step 2: Extract the header (next 4 bytes)
    header = packed_data[4:8].hex()  # Convert bytes to hexadecimal string
    
    # Step 3: Extract the random digits (next 8 bytes)
    random_digits = packed_data[8:16]
    
    # Step 4: Extract the original request data (remaining bytes)
    request_data = packed_data[16:].decode()  # Decode bytes to string

    # Semd monitor data
    
    log_monitor("Cloud --> Network", request_data)

    # Logging extracted information
    log = LoggerManager.LoggerManager().logger
    log.debug("Parsed Data: Length=%d, Header=%s, Random Digits=%s, Request Data=%s",
              total_length, header, random_digits.hex(), request_data)
    
    if isinstance(request_data, str):
        request_data = json.loads(request_data)

    log = LoggerManager.LoggerManager().logger
    log.debug("request_data type after parsing: %s", request_data)

    CancelStatus = "N/A"

    # Proceed with accessing the key
    if "OCsessionManagementResponse" in request_data:
        ocsession_response = parse_ocsession_management_response(request_data["OCsessionManagementResponse"])
        log.debug("OCsessionManagementResponse: %s", ocsession_response.session_management_response.session_response.response)

        # Set TransactionData.responseCode
        TransactionData().responseCode = ocsession_response.session_management_response.session_response.response

        if ocsession_response.session_management_response.transaction_in_process:
            TransactionData().transactionStatus = ocsession_response.session_management_response.transaction_in_process.transaction_status
            TransactionData().exchangeIdentification = ocsession_response.session_management_response.transaction_in_process.exchange_identification

            if ocsession_response.session_management_response.transaction_in_process.cancel_status == "PEND":
                CancelStatus = "PEND"

        else:
            TransactionData().transactionStatus = "N/A"
            CancelStatus = "N/A"
            
        TransactionData().messageFunction = ocsession_response.header.message_function

        if TransactionData().transactionType  not in ["TT_SESSION_HEARTBEAT", "TT_TERMINAL_STATUS"]:
            TransactionData().transactionType = StringUtily.ETransType.TT_SESSION_HEARTBEAT

        log.debug("CancelStatus: %s", CancelStatus)
        
        status_data = {
            "TerminalStatus": TransactionData().get_terminal_status_string(),
            "TransactionStatus": TransactionData().transactionStatus,
            "Response": TransactionData().responseCode,
            "CancelStatus": CancelStatus
        }

        sender = FIFOStatusSender()
        sender.send_status(status_data)
    elif "OCserviceRequest" in request_data:
        log.debug("OCserviceRequest: %s", request_data["OCserviceRequest"])
        
        oc_service_request = ParseServiceRequest(request_data)

        # fill the transaction data
        TransactionData().messageFunction = oc_service_request.header.message_function
        TransactionData().exchangeIdentification = oc_service_request.header.exchange_identification
        TransactionData().serviceAttribute = oc_service_request.service_request.payment_request.service_attribute
        TransactionData().amountQualifier = oc_service_request.service_request.payment_request.transaction_details.amount_qualifier
        TransactionData().validityDuration = oc_service_request.service_request.payment_request.transaction_details.validity_duration
        TransactionData().totalAmount = oc_service_request.service_request.payment_request.transaction_details.total_amount
        TransactionData().motoIndicator = oc_service_request.service_request.payment_request.transaction_details.moto_indicator
        
        if oc_service_request.service_request.context.sale_context.invoice_number:
            TransactionData().invoiceNumber = oc_service_request.service_request.context.sale_context.invoice_number
        else:
            TransactionData().invoiceNumber = ""

        # Clerk id 
        if oc_service_request.service_request.context.sale_context.cashier_identification:
            TransactionData().clerkId = oc_service_request.service_request.context.sale_context.cashier_identification
        else:
            TransactionData().clerkId = ""
 
        
        TransactionData().transactionType = StringUtily.get_transaction_type(TransactionData().messageFunction)
        TransactionData().identification = oc_service_request.header.initiating_party.identification
        TransactionData().type = oc_service_request.header.initiating_party.type

        if TransactionData().transactionType in [StringUtily.ETransType.TT_VOID]:
            TransactionData().localReferenceNumber = oc_service_request.service_request.reversal_request.transaction_identification


        status_data = {
            "TerminalStatus": TransactionData().get_terminal_status_string(),
            "TransactionStatus": "ACPT",
            "Response": "N/A",
            "CancelStatus": CancelStatus
        }

        sender = FIFOStatusSender()
        sender.send_status(status_data)


    elif "OCreportRequest" in request_data:
        log.debug("OCreportRequest: %s", request_data["OCreportRequest"])
    
    else:
        log.error("OCsessionManagementResponse key not found in request_data.")

    

    # if root element is "OCsessionManagementReseponse"
    # if "OCsessionManagementReseponse" in root:
    #     ocsession_response = parse_ocsession_management_response(request_data["OCsessionManagementResponse"])
    #     log = LoggerManager.LoggerManager().logger
    #     log.debug("OCsessionManagementResponse: %s", ocsession_response.session_management_response.session_response.response)



    # elif "OCserviceRequest" in root:
    #     return root["OCtransactionResponse"]
    # elif "OCreportRequest" in root:
    #     return root["OCreportRequest"]
    

def parseSessionManagementResponse(response):
    # Extract the session management response
    #log = LoggerManager.LoggerManager().logger
    #log.debug("Session Management Response: %s", response)
    
    # Extract the session management response
    #log = LoggerManager.LoggerManager().logger
    #log.debug("Session Management Response: %s", response)
    return response
    

    