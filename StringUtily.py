

# Terminal status enum
from enum import Enum
import random


class TerminalStatus(Enum):
    IDLE = 1
    BUSY = 2

# Enum for TransactionStatus
class TransactionStatus(Enum):
    Decline = 1
    Cancellation = 2
    NoResponse = 3
    NoneStatus = 4


class ETransType(Enum):
    TT_TRANS_BEGIN = 1
    TT_SALE = 2
    TT_REFUND = 3
    TT_VOID = 4
    TT_MOTO = 5
    TT_CREDIT_PREAUTH = 6
    TT_CREDIT_PREAUTH_COMPLETION = 7
    TT_CREDIT_INCREMENTAL_AUTH = 8
    TT_BATCH_CLOSE_GENERAL = 9
    TT_HOST_TOTALS_GENERAL = 10
    TT_REPORT = 11
    TT_SESSION_MGR = 12
    TT_SESSION_MGR_PAT = 13
    TT_TIP_ADJUSTMENT = 14
    TT_PAT_AT_TABLE = 15
    TT_SESSION_HEARTBEAT = 16
    TT_CANCEL_TRANSACTION = 17
    TT_TIP_RESPONSE = 18
    TT_RECOVER_TRANSACTION = 19
    TT_FORCE_CANCEL = 20
    TT_RECOVER_TRANSACTION_PAT = 21
    TT_TERMINAL_STATUS = 22
    TT_CRYPTO = 23
    TT_UPOS = 24
    TT_TOKEN_REFUND = 25
    TT_TOKEN_SALE = 26
    TT_TOKEN_PRE_AUTH = 27
    TT_TOKEN_COMPLETION = 28
    TT_TOKEN_PAYOUT = 29
    TT_GIFT_END = 30

'''enum ENTRYMODE
{
	EM_NONE,
	EM_SWIPED,
	EM_MANUAL,
	EM_RFID,
	EM_VIVO,
	EM_SMC,
	EM_END
};
'''
class EntryMode(Enum):
    EM_NONE = 1
    EM_SWIPED = 2
    EM_MANUAL = 3
    EM_RFID = 4
    EM_VIVO = 5
    EM_SMC = 6
    EM_END = 7
    
def get_message_function(trans_type):

    # compare the value of the enum instance

    if trans_type.value == ETransType.TT_SALE.value:
        return "AUTQ"
    elif trans_type.value == ETransType.TT_CRYPTO.value:
        return "CRPQ"
    elif trans_type.value == ETransType.TT_REFUND.value:
        return "RFNQ"
    elif trans_type.value == ETransType.TT_VOID.value:
        return "FMPV"
    elif trans_type.value == ETransType.TT_CREDIT_PREAUTH.value:
        return "FAUQ"
    elif trans_type.value == ETransType.TT_CREDIT_PREAUTH_COMPLETION.value:
        return "CMPV"
    elif trans_type.value == ETransType.TT_HOST_TOTALS_GENERAL.value:
        return "RCLQ"
    elif trans_type.value == ETransType.TT_TERMINAL_STATUS.value:
        return "SASQ"
    elif trans_type.value == ETransType.TT_SESSION_MGR_PAT.value:
        return "SAPQ"
    elif trans_type.value == ETransType.TT_REPORT.value:
        return "RPTQ"
    elif trans_type.value == ETransType.TT_TIP_ADJUSTMENT.value:
        return "TADV"
    elif trans_type.value == ETransType.TT_TIP_RESPONSE.value:
        return "TATK"
    else:
        return "SASQ"
    

    
# define response message function 
def get_response_message_function(trans_type):
    # compare the value of the enum instance

    if trans_type.value == ETransType.TT_SALE.value:
        return "AUTP"
    elif trans_type.value == ETransType.TT_CRYPTO.value:
        return "CRPP"
    elif trans_type.value == ETransType.TT_REFUND.value:
        return "RFNP"
    elif trans_type.value == ETransType.TT_VOID.value:
        return "FMPK"
    elif trans_type.value == ETransType.TT_CREDIT_PREAUTH.value:
        return "FAUP"
    elif trans_type.value == ETransType.TT_CREDIT_PREAUTH_COMPLETION.value:
        return "CMPK"
    elif trans_type.value == ETransType.TT_CREDIT_INCREMENTAL_AUTH.value:
        return "FAUP"
    elif trans_type.value in [ETransType.TT_HOST_TOTALS_GENERAL.value, ETransType.TT_BATCH_CLOSE_GENERAL.value]:
        return "RCLP"
    elif trans_type.value in [ETransType.TT_TERMINAL_STATUS.value, ETransType.TT_SESSION_MGR.value,
                        ETransType.TT_SESSION_HEARTBEAT.value, ETransType.TT_RECOVER_TRANSACTION.value,
                        ETransType.TT_FORCE_CANCEL.value, ETransType.TT_CANCEL_TRANSACTION.value]:
        return "SASP"
    elif trans_type.value == ETransType.TT_SESSION_MGR_PAT.value:
        return "SAPP"
    elif trans_type.value == ETransType.TT_REPORT.value:
        return "RPTP"
    elif trans_type.value == ETransType.TT_TIP_ADJUSTMENT.value:
        return "TADK"
    elif trans_type.value == ETransType.TT_TIP_RESPONSE.value:
        return "TATK"
    elif trans_type.value == ETransType.TT_RECOVER_TRANSACTION_PAT.value:
        return "SAPP"
    else:
        return "FAUP"


# Reverse lookup dictionary
message_to_trans_type = {
    "AUTQ": ETransType.TT_SALE,
    "CRPQ": ETransType.TT_CRYPTO,
    "RFNQ": ETransType.TT_REFUND,
    "FMPV": ETransType.TT_VOID,
    "FAUQ": ETransType.TT_CREDIT_PREAUTH,  # Default case maps to FAUQ
    "CMPV": ETransType.TT_CREDIT_PREAUTH_COMPLETION,
    "RCLQ": ETransType.TT_HOST_TOTALS_GENERAL,  # Could also map to TT_BATCH_CLOSE_GENERAL
    "SASQ": ETransType.TT_TERMINAL_STATUS,  # Multiple types map to SASQ
    "SAPQ": ETransType.TT_SESSION_MGR_PAT,
    "RPTQ": ETransType.TT_REPORT,
    "TADV": ETransType.TT_TIP_ADJUSTMENT,
    "TATK": ETransType.TT_TIP_RESPONSE,
}

def get_transaction_type(message_code):
    return message_to_trans_type.get(message_code, None)


def generate_auth_code():
    # format A + 5 digit random number
    return 'A' + str(random.randint(10000, 99999))

def generate_record_number():
    # format 7 digit random number
    return str(random.randint(1000000, 9999999))

def generate_host_invoicenum():
    # format 7 digit random number
    return str(random.randint(1000000, 9999999))

def generate_hts():
    # format 7 digit random number
    return str(random.randint(1000000, 9999999))
    

# main function
if __name__ == "__main__":
    # Accessing the Singleton instance


    print(get_transaction_type("AUTQ"))  # Should print 'TT_SALE'
    print(get_transaction_type("FAUQ"))  # Should print 'TT_CREDIT_PREAUTH'
    print(get_transaction_type("RCLQ"))  # Should print 'TT_HOST_TOTALS_GENERAL'
    print(get_transaction_type("SASQ"))  # Should print 'TT_TERMINAL_STATUS'
    print(get_transaction_type("UNKNOWN"))  # Should print 'None'
    print(get_transaction_type("TADV"))  # Should print 'TT_TIP_ADJUSTMENT'
    print(get_transaction_type("TATK"))  # Should print 'TT_TIP_RESPONSE'
    print(get_transaction_type("CMPV"))  # Should print 'TT_CREDIT_PREAUTH_COMPLETION'
    print(get_transaction_type("RFNQ"))  # Should print 'TT_REFUND'
    print(get_transaction_type("SAPQ"))  # Should print 'TT_SESSION_MGR_PAT'
    print(get_transaction_type("RPTQ"))  # Should print 'TT_REPORT'
    print(get_transaction_type("CRPQ"))  # Should print 'TT_CRYPTO'
    print(get_transaction_type("FMPV"))  # Should print 'TT_VOID'
    print(get_transaction_type("FAUQ"))  # Should print 'TT

    print(get_message_function(ETransType.TT_SALE))  # Should print 'AUTQ'
    print(get_message_function(ETransType.TT_CRYPTO))  # Should print 'CRPQ'

    transactionType = ETransType.TT_SALE

    if transactionType in [ETransType.TT_SALE, ETransType.TT_CRYPTO, ETransType.TT_REFUND, ETransType.TT_VOID]:
        print("Transaction type is supported")