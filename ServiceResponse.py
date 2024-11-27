import datetime
from typing import List
import uuid

from Header import Header, Party
import StringUtily


class TransactionIdentification:
    transaction_date_time: datetime
    transaction_reference: str

    def __init__(self, transaction_date_time: datetime, transaction_reference: str) -> None:
        self.transaction_date_time = transaction_date_time
        self.transaction_reference = transaction_reference

    def to_dict(self) -> dict:
        return {
            "transactionDateTime": self.transaction_date_time.isoformat(),
            "transactionReference": self.transaction_reference,
        }

class Receipt:
    output_content: str
    document_qualifier: str

    def __init__(self, output_content: str, document_qualifier: str) -> None:
        self.output_content = output_content
        self.document_qualifier = document_qualifier
    def to_dict(self) -> dict:
        return {
            "outputContent": self.output_content,
            "documentQualifier": self.document_qualifier,
        }    


class ResponseToAuthorisation:
    response: str

    def __init__(self, response: str) -> None:
        self.response = response
    def to_dict(self) -> dict:
        return {
            "response": self.response,
        }


class AuthorisationResult:
    authorisation_code: int
    response_to_authorisation: ResponseToAuthorisation

    def __init__(self, authorisation_code: int, response_to_authorisation: ResponseToAuthorisation) -> None:
        self.authorisation_code = authorisation_code
        self.response_to_authorisation = response_to_authorisation
    def to_dict(self) -> dict:
        return {
            "authorisationCode": self.authorisation_code,
            "responseToAuthorisation": self.response_to_authorisation.to_dict(),
        }


class ReceiptDetails:
    ref_id: str
    msk_pan: str
    card_aid: str
    card_lbl: str
    emv_tag_tsi: int
    emv_tag_tvr: str
    balance_due: str
    account_type: str
    apprdecl_iso: str
    host_invoice: str
    host_sequence: int
    record_number: str
    invoice_number: int
    card_data_ntry_md: str
    emv_tag_cryptogram: str

    def __init__(self, ref_id: str, msk_pan: str, card_aid: str, card_lbl: str, emv_tag_tsi: int, emv_tag_tvr: str, balance_due: str, account_type: str, apprdecl_iso: str, host_invoice: str, host_sequence: int, record_number: str, invoice_number: int, card_data_ntry_md: str, emv_tag_cryptogram: str) -> None:
        self.ref_id = ref_id
        self.msk_pan = msk_pan
        self.card_aid = card_aid
        self.card_lbl = card_lbl
        self.emv_tag_tsi = emv_tag_tsi
        self.emv_tag_tvr = emv_tag_tvr
        self.balance_due = balance_due
        self.account_type = account_type
        self.apprdecl_iso = apprdecl_iso
        self.host_invoice = host_invoice
        self.host_sequence = host_sequence
        self.record_number = record_number
        self.invoice_number = invoice_number
        self.card_data_ntry_md = card_data_ntry_md
        self.emv_tag_cryptogram = emv_tag_cryptogram
    def to_dict(self) -> dict:
        return {
            "refId": self.ref_id,
            "mskPan": self.msk_pan,
            "cardAid": self.card_aid,
            "cardLbl": self.card_lbl,
            "emvTagTsi": self.emv_tag_tsi,
            "emvTagTvr": self.emv_tag_tvr,
            "balanceDue": self.balance_due,
            "accountType": self.account_type,
            "apprdeclIso": self.apprdecl_iso,
            "hostInvoice": self.host_invoice,
            "hostSequence": self.host_sequence,
            "recordNumber": self.record_number,
            "invoiceNumber": self.invoice_number,
            "cardDataNtryMd": self.card_data_ntry_md,
            "emvTagCryptogram": self.emv_tag_cryptogram,
        }


class DetailedAmount:
    fees: int
    cashback: str
    gratuity: str
    amount_goods_and_services: str

    def __init__(self, fees: int, cashback: str, gratuity: str, amount_goods_and_services: str) -> None:
        self.fees = fees
        self.cashback = cashback
        self.gratuity = gratuity
        self.amount_goods_and_services = amount_goods_and_services
    
    def to_dict(self) -> dict:
        return {
            "fees": self.fees,
            "cashback": self.cashback,
            "gratuity": self.gratuity,
            "amountGoodsAndServices": self.amount_goods_and_services,
        }


class TransactionDetails:
    total_amount: str
    detailed_amount: DetailedAmount

    def __init__(self, total_amount: str, detailed_amount: DetailedAmount) -> None:
        self.total_amount = total_amount
        self.detailed_amount = detailed_amount
    
    def to_dict(self) -> dict:
        return {
            "totalAmount": self.total_amount,
            "detailedAmount": self.detailed_amount.to_dict(),
        }


class TransactionResponse:
    signature_data: str
    receipt_details: ReceiptDetails
    transaction_details: TransactionDetails
    authorisation_result: AuthorisationResult

    def __init__(self, signature_data: str, receipt_details: ReceiptDetails, transaction_details: TransactionDetails, authorisation_result: AuthorisationResult) -> None:
        self.signature_data = signature_data
        self.receipt_details = receipt_details
        self.transaction_details = transaction_details
        self.authorisation_result = authorisation_result
    
    def to_dict(self) -> dict:
        return {
            "signatureData": self.signature_data,
            "receiptDetails": self.receipt_details.to_dict(),
            "transactionDetails": self.transaction_details.to_dict(),
            "authorisationResult": self.authorisation_result.to_dict(),
        }


class RetailerPaymentResult:
    transaction_type: str
    transaction_response: TransactionResponse

    def __init__(self, transaction_type: str, transaction_response: TransactionResponse) -> None:
        self.transaction_type = transaction_type
        self.transaction_response = transaction_response
    
    def to_dict(self) -> dict:
        return {
            "transactionType": self.transaction_type,
            "transactionResponse": self.transaction_response.to_dict(),
        }


class PaymentResponse:
    receipt: List[Receipt]
    retailer_payment_result: RetailerPaymentResult
    sale_reference_identification: str
    poi_transaction_identification: TransactionIdentification
    sale_transaction_identification: TransactionIdentification

    def __init__(self, receipt: List[Receipt], retailer_payment_result: RetailerPaymentResult, sale_reference_identification: str, poi_transaction_identification: TransactionIdentification, sale_transaction_identification: TransactionIdentification) -> None:
        self.receipt = receipt
        self.retailer_payment_result = retailer_payment_result
        self.sale_reference_identification = sale_reference_identification
        self.poi_transaction_identification = poi_transaction_identification
        self.sale_transaction_identification = sale_transaction_identification
    
    def to_dict(self) -> dict:
        return {
            "receipt": [receipt.to_dict() for receipt in self.receipt],
            "retailerPaymentResult": self.retailer_payment_result.to_dict(),
            "saleReferenceIdentification": self.sale_reference_identification,
            "poiTransactionIdentification": self.poi_transaction_identification.to_dict(),
            "saleTransactionIdentification": self.sale_transaction_identification.to_dict(),
        }


class Response:
    response_code: str

    def __init__(self, response_code: str) -> None:
        self.response_code = response_code
    
    def to_dict(self) -> dict:
        return {
            "responseCode": self.response_code,
        }


class ServiceResponse:
    response: Response
    payment_response: List[PaymentResponse]

    def __init__(self, response: Response, payment_response: List[PaymentResponse]) -> None:
        self.response = response
        self.payment_response = payment_response
    
    def to_dict(self) -> dict:
        return {
            "response": self.response.to_dict(),
            "paymentResponse": [payment_response.to_dict() for payment_response in self.payment_response],
        }


class OCserviceResponse:
    header: Header
    service_response: ServiceResponse

    def __init__(self, header: Header, service_response: ServiceResponse) -> None:
        self.header = header
        self.service_response = service_response

    def to_dict(self) -> dict:
        return {
            "header": self.header.to_dict(),
            "serviceResponse": self.service_response.to_dict(),
        }

class PackServiceResponse:
    o_cservice_response: OCserviceResponse

    def __init__(self, o_cservice_response: OCserviceResponse) -> None:
        self.o_cservice_response = o_cservice_response

    def to_dict(self) -> dict:
        return {
            "OCserviceResponse": self.o_cservice_response.to_dict(),
        }

if __name__ == "__main__":

    tid = '12300337'
    authkey = 'fe0d12c9-2b21-41d1-abe3-cbabfbdff567'
    initg_pty = Party(tid,authkey,"TID")
    rcpt_pty = Party(tid,"","PID")

    now = datetime.datetime.utcnow()
    utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


    message_function = "AUTQ"

        #if (v.transactionType == Constants.TransctionType.SALE):
        #    print("SALE")
        #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
        #    msgFunction = "SASQ"

    hdr = Header(message_function,"3.0",uuid.uuid4(),utc_string,initg_pty,rcpt_pty)

    response = Response("APPR")  # Successful response code

    receipt1 = Receipt("Receipt content 1", "DocumentQualifier1")
    receipt2 = Receipt("Receipt content 2", "DocumentQualifier2")

    transaction_identification = TransactionIdentification(
        datetime.datetime.now(), "TXN123456789"
    )

    detailed_amount = DetailedAmount(5, "10", "2", "50")
    transaction_details = TransactionDetails("67", detailed_amount)

    response_to_authorisation = ResponseToAuthorisation("Approved")
    authorisation_result = AuthorisationResult(123456, response_to_authorisation)

    receipt_details = ReceiptDetails(
        "REF123", "1234****5678", "AID1234", "VISA",
        123, "tvrExample", "0.00", "Credit", "ISO123",
        "Invoice001", 12, "RN001", 456, "EntryMode", "CryptogramData"
    )

    transaction_response = TransactionResponse(
        "SignatureDataExample", receipt_details, transaction_details, authorisation_result
    )

    retailer_payment_result = RetailerPaymentResult("Sale", transaction_response)

    payment_response = PaymentResponse(
        [receipt1, receipt2],
        retailer_payment_result,
        "SaleRef123",
        transaction_identification,
        transaction_identification
    )

    service_response = ServiceResponse(response, [payment_response])
    oc_service_response = OCserviceResponse(hdr, service_response)

    pack_service_response = PackServiceResponse(oc_service_response)
    print(pack_service_response.to_dict())
    
