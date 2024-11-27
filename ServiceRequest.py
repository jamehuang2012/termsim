import json
from uuid import UUID
from Header import Header, Party


class SaleContext:
    cashier_identification: str
    invoice_number: int
    identification_type: str

    def __init__(self, cashier_identification: str, invoice_number: int, identification_type: str) -> None:
        self.cashier_identification = cashier_identification
        self.invoice_number = invoice_number
        self.identification_type = identification_type


class Context:
    sale_context: SaleContext

    def __init__(self, sale_context: SaleContext) -> None:
        self.sale_context = sale_context


class Poi:
    identification: str

    def __init__(self, identification: str) -> None:
        self.identification = identification


class Environment:
    merchant: Poi
    poi: Poi

    def __init__(self, merchant: Poi, poi: Poi) -> None:
        self.merchant = merchant
        self.poi = poi


class DetailedAmount:
    gratuity: str
    amount_goods_and_services: str

    def __init__(self, gratuity: str, amount_goods_and_services: str) -> None:
        self.gratuity = gratuity
        self.amount_goods_and_services = amount_goods_and_services


class TransactionDetails:
    total_amount: str
    validity_duration: int
    amount_qualifier: str
    moto_indicator: bool
    detailed_amount: DetailedAmount

    def __init__(self, total_amount: str, validity_duration: int, amount_qualifier: str, moto_indicator: bool, detailed_amount: DetailedAmount) -> None:
        self.total_amount = total_amount
        self.validity_duration = validity_duration
        self.amount_qualifier = amount_qualifier
        self.moto_indicator = moto_indicator
        self.detailed_amount = detailed_amount


class PaymentRequest:
    transaction_type: str
    service_attribute: str
    transaction_identification: str
    transaction_details: TransactionDetails

    def __init__(self, transaction_type: str, service_attribute: str, transaction_identification: str, transaction_details: TransactionDetails) -> None:
        self.transaction_type = transaction_type
        self.service_attribute = service_attribute
        self.transaction_identification = transaction_identification
        self.transaction_details = transaction_details


class ServiceRequest:
    environment: Environment
    context: Context
    service_content: str
    payment_request: PaymentRequest

    def __init__(self, environment: Environment, context: Context, service_content: str, payment_request: PaymentRequest) -> None:
        self.environment = environment
        self.context = context
        self.service_content = service_content
        self.payment_request = payment_request


class OCserviceRequest:
    header: Header
    service_request: ServiceRequest

    def __init__(self, header: Header, service_request: ServiceRequest) -> None:
        self.header = header
        self.service_request = service_request

        

# ParseServiceRequest function remains mostly the same but handles nested dictionaries
def ParseServiceRequest(json_data: dict) -> OCserviceRequest:
    data = json_data['OCserviceRequest']

    header_data = data['header']
    service_request_data = data['serviceRequest']

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

    # Parsing the ServiceRequest
    service_request = ServiceRequest(
        environment=Environment(
            merchant=Poi(service_request_data['environment']['merchant']['identification']),
            poi=Poi(service_request_data['environment']['POI']['identification'])
        ),
        context=Context(
            sale_context=SaleContext(
                cashier_identification=service_request_data['context']['saleContext'].get('cashierIdentification', ''),
                invoice_number=int(service_request_data['context']['saleContext'].get('invoiceNumber', 0)),
                identification_type=service_request_data['context']['saleContext'].get('identificationType', '')
            )
        ),
        service_content=service_request_data['serviceContent'],
        payment_request=PaymentRequest(
            transaction_type=service_request_data['paymentRequest']['transactionType'],
            service_attribute=service_request_data['paymentRequest'].get('serviceAttribute', ''),
            transaction_identification=service_request_data['paymentRequest'].get('transactionIdentification', ''),
            transaction_details=TransactionDetails(
                total_amount=service_request_data['paymentRequest']['transactionDetails']['totalAmount'],
                validity_duration=service_request_data['paymentRequest']['transactionDetails'].get('validityDuration', 0),
                amount_qualifier=service_request_data['paymentRequest']['transactionDetails'].get('amountQualifier', ''),
                moto_indicator=service_request_data['paymentRequest']['transactionDetails']['MOTOIndicator'],
                detailed_amount=DetailedAmount(
                    gratuity=service_request_data['paymentRequest']['transactionDetails']['detailedAmount']['gratuity'],
                    amount_goods_and_services=service_request_data['paymentRequest']['transactionDetails']['detailedAmount']['amountGoodsAndServices']
                )
            )
        )
    )

    return OCserviceRequest(header, service_request)


# Test the function
if __name__ == "__main__":
    # JSON data as a string
    json_data = '''
    {
        "header": {
            "messageFunction": "FAUQ",
            "protocolVersion": "2.0",
            "exchangeIdentification": "229e92af-07d7-4a51-b639-817b1f4dc629",
            "creationDateTime": "2024-11-26T13:16:01.430036Z",
            "initiatingParty": {
                "identification": "22000353",
                "type": "PID",
                "shortName": "Cash Register ID",
                "authenticationKey": "3225b06e-79e2-4820-b795-cb6cc71c2a8c"
            },
            "recipientParty": {
                "identification": "12000353",
                "type": "TID",
                "shortName": "Terminal ID"
            }
        },
        "serviceRequest": {
            "environment": {
                "merchant": {
                    "identification": "7800199838"
                },
                "POI": {
                    "identification": "12000353"
                }
            },
            "context": {
                "saleContext": {
                    "cashierIdentification": "",
                    "invoiceNumber": "123",
                    "identificationType": ""
                }
            },
            "serviceContent": "FSPQ",
            "paymentRequest": {
                "transactionType": "CRDP",
                "serviceAttribute": "IRES",
                "transactionIdentification": "",
                "transactionDetails": {
                    "totalAmount": "20.00",
                    "validityDuration": "7",
                    "AmountQualifier": "ESTM"
                },
            "MOTOIndicator": false,
            "detailedAmount": {
                "gratuity": "1.00",
                "amountGoodsAndServices": "1.00"
            }
            }
        }
    }
    '''

    # Convert the JSON string to a Python dictionary
    data_dict = json.loads(json_data)

    # Parse the data and create an OCserviceRequest object
    oc_service_request = ParseServiceRequest(data_dict)

    # Print the parsed object to verify correctness
    print(oc_service_request.header.message_function)
    print(oc_service_request.header.initiating_party.identification)
    print(oc_service_request.service_request.environment.merchant.identification)
    print(oc_service_request.service_request.context.sale_context.invoice_number)
    print(oc_service_request.service_request.payment_request.transaction_details.total_amount)
    print(oc_service_request.service_request.payment_request.transaction_details.detailed_amount.gratuity)
    
    #serviceAttribute
    print(oc_service_request.service_request.payment_request.service_attribute)
    #AmountQualifier 
    print(oc_service_request.service_request.payment_request.transaction_details.amount_qualifier)
    #validityDuration
    print(oc_service_request.service_request.payment_request.transaction_details.validity_duration)

    #MOTOIndicator
    print(oc_service_request.service_request.payment_request.transaction_details.moto_indicator)


    #"exchangeIdentification": "229e92af-07d7-4a51-b639-817b1f4dc629",
    print(oc_service_request.header.exchange_identification)

     