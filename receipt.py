import datetime


class ReceiptGenerator:
    def __init__(self, term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num,copy_type,transaction_name,app_name):
        self.term_num = term_num
        self.record_num = record_num
        self.host_invoice_num = host_invoice_num
        self.host_seq_num = host_seq_num
        self.merch_invoice_num = merch_invoice_num
        self.card_num = card_num
        self.card_type = card_type
        self.date = date
        self.amount = amount
        self.auth_num = auth_num
        self.hts_num = hts_num
        self.aid_num = aid_num
        self.tc_num = tc_num
        self.tvr_num = tvr_num
        self.tsi_num = tsi_num
        self.copy_type = copy_type
        self.transaction_name = transaction_name
        self.app_name = app_name
    def generate_receipt(self):
        receipt = "NUVEI TECHNOLOGIES".center(24) + "\n"
        receipt += "      MONTREAL, PQ\n\n"
        receipt += "TERM #{self.term_num:>18}\n".format(self=self)
        receipt += "RECORD #{self.record_num:>16}\n".format(self=self)
        receipt += "HOST INVOICE #{self.host_invoice_num:>10}\n".format(self=self)
        receipt += "HOST SEQ #{self.host_seq_num:>14}\n".format(self=self)
        receipt += "MERCH INVOICE{self.merch_invoice_num:>11}\n".format(self=self)
        receipt += "------------------------\n"
        receipt += "CARD    {}{}\n".format("*"*12 + self.card_num[-4:], "")
        receipt += "{}{}\n".format(self.card_type, " "*23)
        receipt += "{}\n".format(self.date)
        receipt += "------------------------\n"
        receipt += "{}\n".format(self.transaction_name)
        receipt += "TOTAL{self.amount:>19}\n".format(self=self)
        receipt += "------------------------\n\n"
        receipt += "AUTH#:{}".format(self.auth_num) + " "*9 + "B:0\n"
        receipt += "HTS#:     {}{}\n".format(self.hts_num, " "*18)
        receipt += "TRANSACTION".center(24) +  "\n"
        receipt += "APPROVED 000".center(24) + "\n"
        receipt += "THANK YOU".center(24) + "\n"
        receipt += "\n{}\n".format(self.app_name)
        receipt += "AID:  {}{}\n".format(self.aid_num, " "*(16-len(str(self.aid_num))))
        receipt += "TC:   {}{}\n".format(self.tc_num, " "*16)
        receipt += "TVR:  {}{}\n".format(self.tvr_num, " "*16)
        receipt += "TSI:  {}{}\n".format(self.tsi_num, " "*16)
        receipt += "             \n"
        receipt += self.copy_type.center(24)
        return receipt

if __name__ == "__main__":
    term_num = "10002640"
    record_num = "0001"
    host_invoice_num = "1234567"
    host_seq_num = "10010002640"
    merch_invoice_num = "10002640"
    card_num = "************0401"
    card_type = "CREDIT/AMEX"
    date = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
    amount = "$10.00"
    auth_num = "A26752"
    hts_num = "20230107122221"
    aid_num = "A00000002501"
    tc_num = "017AA200ACFBD5CC"
    tvr_num = "0440008000"
    tsi_num = "E800"
    copy_type = "MERCHANT COPY"
    receipt = ReceiptGenerator(term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num, copy_type)
    print(receipt.generate_receipt())
