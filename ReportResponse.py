from typing import List
from Header import Header
from ServiceRequest import Context, Environment
from ServiceResponse import DetailedAmount


class TransactionDetailReport:
    type: str
    entry_mode: str
    card_masked: str
    detailed_amount: DetailedAmount
    cumulative_amount: int

    def __init__(self, type: str, entry_mode: str, card_masked: str, detailed_amount: DetailedAmount, cumulative_amount: int) -> None:
        self.type = type
        self.entry_mode = entry_mode
        self.card_masked = card_masked
        self.detailed_amount = detailed_amount
        self.cumulative_amount = cumulative_amount
    
    # to_dict method
    def to_dict(self):
        return {
            "type": self.type,
            "entryMode": self.entry_mode,
            "cardMasked": self.card_masked,
            "detailedAmount": self.detailed_amount.to_dict(),
            "cumulativeAmount": self.cumulative_amount
        }


class TransactionTotalsSet:
    brand: str
    sale_identification: int
    payment_instrument_type: str
    transaction_detail_report: TransactionDetailReport
    sale_reconciliation_identification: int

    def __init__(self, brand: str, sale_identification: int, payment_instrument_type: str, transaction_detail_report: TransactionDetailReport, sale_reconciliation_identification: int) -> None:
        self.brand = brand
        self.sale_identification = sale_identification
        self.payment_instrument_type = payment_instrument_type
        self.transaction_detail_report = transaction_detail_report
        self.sale_reconciliation_identification = sale_reconciliation_identification

    # to_dict method
    def to_dict(self):
        return {
            "brand": self.brand,
            "saleIdentification": self.sale_identification,
            "paymentInstrumentType": self.payment_instrument_type,
            "transactionDetailReport": self.transaction_detail_report.to_dict(),
            "saleReconciliationIdentification": self.sale_reconciliation_identification
        }

class ReportGetTotalsResponse:
    transaction_totals_set: List[TransactionTotalsSet]
    poi_reconciliation_identification: int

    def __init__(self, transaction_totals_set: List[TransactionTotalsSet], poi_reconciliation_identification: int) -> None:
        self.transaction_totals_set = transaction_totals_set
        self.poi_reconciliation_identification = poi_reconciliation_identification

    
    # to_dict method
    def to_dict(self):
        return {
            "transactionTotalsSet": [transaction.to_dict() for transaction in self.transaction_totals_set],
            "poiReconciliationIdentification": self.poi_reconciliation_identification
        }


class ReportResponse:
    context: Context
    response: str
    environment: Environment
    report_get_totals_response: ReportGetTotalsResponse

    def __init__(self, context: Context, response: str, environment: Environment, report_get_totals_response: ReportGetTotalsResponse) -> None:
        self.context = context
        self.response = response
        self.environment = environment
        self.report_get_totals_response = report_get_totals_response
    
    # to_dict method
    def to_dict(self):
        return {
            "context": self.context.to_dict(),
            "response": self.response,
            "environment": self.environment.to_dict(),
            "reportGetTotalsResponse": self.report_get_totals_response.to_dict()
        }

class OCreportResponse:
    header: Header
    report_response: ReportResponse

    def __init__(self, header: Header, report_response: ReportResponse) -> None:
        self.header = header
        self.report_response = report_response
    
    # to_dict method
    def to_dict(self):
        return {
            "header": self.header.to_dict(),
            "reportResponse": self.report_response.to_dict()
        }


# Pack Report Response
def PackOCreportResponse(ocreport_response: OCreportResponse) -> dict:
    return {
        "OCreportResponse": ocreport_response.to_dict()
    }