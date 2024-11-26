from enum import Enum


TID = "12300337"
PID = "20000004"
URL = "terminal-poi-sandbox.nuvei.com"
AuthKey = "b68b525d-6c18-40fe-9e39-132fb5a687da"

#URL = "127.0.0.1"
#URL = "10.152.183.251"
PORT = 18080
STATUS = "IDLE"





class TransctionType(Enum):
    SALE = 1
    REFUND = 2
    VOID = 3
    PRE_AUTH = 4
    COMPLETION = 5
    SETTLE = 6
    SESSIONMGR = 7

