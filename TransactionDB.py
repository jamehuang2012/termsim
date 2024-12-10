import sqlite3

class TransactionDB:
    def __init__(self, db_name='account.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()


    # Create the transaction table , add signature data with binary data type

    def create_tansaaction_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expireDate TEXT,
                    entryMode TEXT,
                    clerkId TEXT,
                    Date TEXT,
                    Time TEXT,
                    batchNo TEXT,
                    InvoiceNo TEXT,
                    SeqNo TEXT,
                    responseCode TEXT,
                    responseMessage TEXT,
                    transactionType TEXT,
                    cardType TEXT,
                    totalAmount REAL,
                    purchaseAmount REAL,
                    tipAmount REAL,
                    cashbackAmount REAL,
                    surchargeAmount REAL,
                    serviceFee REAL,
                    tid TEXT,
                    mid TEXT,
                    aid TEXT,
                    tvr TEXT,
                    emvCryptogram TEXT,
                    emvapp TEXT,
                    hostReferenceNo TEXT,
                    hostSequenceNo TEXT,
                    ResponseDate TEXT,
                    ResponseTime TEXT,
                    tsi TEXT,
                    transactionReference TEXT,
                    service_attribute TEXT,
                    amount_qualifier TEXT,
                    validity_duration INTEGER,
                    moto_indicator BOOLEAN,
                    is_void BOOLEAN,
                );
            ''')

    # Create pre-auth table

    def create_pre_auth_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS pre_auth (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expireDate TEXT,
                    entryMode TEXT,
                    clerkId TEXT,
                    Date TEXT,
                    Time TEXT,
                    batchNo TEXT,
                    InvoiceNo TEXT,
                    SeqNo TEXT,
                    responseCode TEXT,
                    responseMessage TEXT,
                    transactionType TEXT,
                    cardType TEXT,
                    totalAmount REAL,
                    purchaseAmount REAL,
                    tipAmount REAL,
                    cashbackAmount REAL,
                    surchargeAmount REAL,
                    serviceFee REAL,
                    tid TEXT,
                    mid TEXT,
                    aid TEXT,
                    tvr TEXT,
                    emvCryptogram TEXT,
                    emvapp TEXT,
                    hostReferenceNo TEXT,
                    hostSequenceNo TEXT,
                    ResponseDate TEXT,
                    ResponseTime TEXT,
                    tsi TEXT,
                    transactionReference TEXT,
                    service_attribute TEXT,
                    amount_qualifier TEXT,
                    validity_duration INTEGER,
                    moto_indicator BOOLEAN,
                    is_complete BOOLEAN,
                );
            ''')

    def create_print_history(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS print_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expireDate TEXT,
                    entryMode TEXT,
                    clerkId TEXT,
                    Date TEXT,
                    Time TEXT,
                    batchNo TEXT,
                    InvoiceNo TEXT,
                    SeqNo TEXT,
                    responseCode TEXT,
                    responseMessage TEXT,
                    transactionType TEXT,
                    cardType TEXT,
                    totalAmount REAL,
                    purchaseAmount REAL,
                    tipAmount REAL,
                    cashbackAmount REAL,
                    surchargeAmount REAL,
                    serviceFee REAL,
                    tid TEXT,
                    mid TEXT,
                    aid TEXT,
                    tvr TEXT,
                    emvCryptogram TEXT,
                    emvapp TEXT,
                    hostReferenceNo TEXT,
                    hostSequenceNo TEXT,
                    ResponseDate TEXT,
                    ResponseTime TEXT,
                    tsi TEXT,
                    transactionReference TEXT,
                    service_attribute TEXT,
                    amount_qualifier TEXT,
                    validity_duration INTEGER,
                    moto_indicator BOOLEAN,
                    is_signed BOOLEAN,
                    signature BLOB,
                );
            ''')

    # Create those 3 tables
    def create_table(self):
        self.create_tansaaction_table()
        self.create_pre_auth_table()
        self.create_print_history()


    def insert_transaction(self, transaction_data):
        with self.connection:
            self.connection.execute('''
                INSERT INTO transactions (
                    expireDate, entryMode, clerkId, Date, Time, batchNo, InvoiceNo, SeqNo,
                    responseCode, responseMessage, transactionType, cardType, totalAmount,
                    purchaseAmount, tipAmount, cashbackAmount, surchargeAmount, serviceFee,
                    tid, mid, aid, tvr, emvCryptogram, emvapp, hostReferenceNo, hostSequenceNo,
                    ResponseDate, ResponseTime, tsi, transactionReference, service_attribute,
                    amount_qualifier, validity_duration, moto_indicator
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', transaction_data)

    # Close the connection when done
    def close(self):
        self.connection.close()

# Example Usage
if __name__ == "__main__":
    db = TransactionDB()

    # insert a transaction  Transaction Data: ('', '', '', '2024-12-03', '02:25:09', 0, '', '9565186', 'A50832', '', <ETransType.TT_SALE: 2>, 'CREDIT/DISCOVER', '1.00', 0.0, '0.00', 0.0, 0.0, 0.0, '12300337', 'mid', 'A0000001523010', '0440008000', '017AA200ACFBD5CC', 'DISCOVER', '10010002640', '10010002640', '2024-12-02', '20:25:09', 'E800', '9565186', None, None, None, False)
    #db.insert_transaction(('', '', '', '2024-12-03', '02:25:09', 0, '', '9565186', 'A50832', '', '2', 'CREDIT/DISCOVER', '1.00', 0.0, '0.00', 0.0, 0.0, 0.0, '12300337', 'mid', 'A0000001523010', '0440008000', '017AA200ACFBD5CC', 'DISCOVER', '10010002640', '10010002640', '2024-12-02', '20:25:09', 'E800', '9565186', None, None, None, False))

    # list of transaction data from table transactions

    for row in db.connection.execute('SELECT * FROM transactions'):
        print(row)
