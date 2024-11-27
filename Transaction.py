
class Support:
    sale: int
    refund: int
    void: int
    preauth: int
    completion: int

    def __init__(self, sale: int, refund: int, void: int, preauth: int, completion: int) -> None:
        self.sale = sale
        self.refund = refund
        self.void = void
        self.preauth = preauth
        self.completion = completion

class Config:
    url: str
    port: int
    support: Support

    def __init__(self, url: str, port: int, support: Support) -> None:
        self.url = url
        self.port = port
        self.support = support


class Transaction:
    __instance = None

    sta = None;
    transactionType = None;
    tipAmount = 0;
    purchaseAmount = 0;
    tipEnabled = False;
    xchagId = None;

    def __init__(self):
        if Transaction.__instance == None:
            Transaction.__instance = self
            self.variable = None

    @staticmethod
    def getInstance():
        if Transaction.__instance == None:
            Transaction()
        return Transaction.__instance
    



