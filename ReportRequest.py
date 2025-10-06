
from uuid import UUID
from Header import Header, Party
from ServiceRequest import Context, Environment


class ReportTransactionRequest:
    report_type: str

    def __init__(self, report_type: str) -> None:
        self.report_type = report_type
    
    # to_dict method
    def to_dict(self):
        return {
            "report_type": self.report_type
        }


class ReportRequest:
    environment: Environment
    context: Context
    svc_cntt: str
    report_transaction_request: ReportTransactionRequest

    def __init__(self, environment: Environment, context: Context, svc_cntt: str, report_transaction_request: ReportTransactionRequest) -> None:
        self.environment = environment
        self.context = context
        self.svc_cntt = svc_cntt
        self.report_transaction_request = report_transaction_request

    def to_dict(self):
        return {
            "environment": self.environment.to_dict(),
            "context": self.context.to_dict(),
            "svc_cntt": self.svc_cntt,
            "report_transaction_request": self.report_transaction_request.to_dict()
        }


class OCreportRequest:
    header: Header
    report_request: ReportRequest

    def __init__(self, header: Header, report_request: ReportRequest) -> None:
        self.header = header
        self.report_request = report_request

    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            "report_request": self.report_request.to_dict()
        }
    

# Parse Report Request
def parse_report_request(json_data: dict) -> OCreportRequest:

    data = json_data['OCreportRequest']

    header_data = data['header']
    service_request_data = data['ReportRequest']

    # Parsing the Header
    header = Header(
        recipient_party=Party(
            identification=header_data['recipientParty']['identification'],
            type=header_data['recipientParty']['type'],
            shortName=header_data['recipientParty']['shortName']
        ),
        initiating_party=Party(
            identification=header_data['initiatingParty']['identification'],
            type=header_data['initiatingParty']['type'],
            shortName=header_data['initiatingParty']['shortName']
        ),
        message_function=header_data['messageFunction'],
        protocol_version=header_data['protocolVersion'],
        creation_date_time=header_data['creationDateTime'],
        exchange_identification=UUID(header_data['exchangeIdentification'])
    )
    
    

    # Parse the Report Request
    report_request = ReportRequest(
        environment=Environment(
            merchant_id=service_request_data['environment']['merchant']['identification'],
            terminal_id=service_request_data['environment']['terminal']['identification'],
           
        ),
        sale_context=Context(
                cashier_id=service_request_data['environment']['saleContext']['cashierIdentification'],
                invoice_number=service_request_data['environment']['saleContext']['invoiceNumber'],
                tokenRequested = service_request_data['environment']['saleContext']['tokenRequested'],
            ),

        svc_cntt=service_request_data['svcCntt'],
        report_transaction_request=ReportTransactionRequest(
            report_type=service_request_data['reportTransactionRequest']['reportType']
        )
    )
 
    return OCreportRequest( header=header, report_request = report_request)
