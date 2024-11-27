from enum import Enum

import StringUtily



# Singleton class for TransactionData
class TransactionData:
    # Private static instance variable to hold the Singleton instance
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Ensure only one instance is created
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            # Initialize the instance variables if it's the first creation
            cls._instance.isRunning = False
            cls._instance.status = StringUtily.TransactionStatus.NoneStatus
            cls._instance.tipAmount = 0.0
            cls._instance.cashback = 0.0
            cls._instance.surchargeFee = 0.0
            cls._instance.serviceFee = 0.0
            cls._instance.enableSignature = False
            cls._instance.currencyCode = 'USD'
            cls._instance.splitPayment = False
            cls._instance.splitAmount = 0.0
            cls._instance.terminalStatus = StringUtily.TerminalStatus.IDLE.name
            cls._instance.transactionType = StringUtily.ETransType.TT_SESSION_HEARTBEAT
            cls._instance.identification = ''
            cls._instance.type = ''
            cls._instance.respnseCode = ''
            cls._instance.responseMessage = ''
            cls._instance.transactionStatus = ''
            cls._instance.exchangeIdentification = ''
            cls._instance.service_attribute = None
            cls._instance.amount_qualifier = None
            cls._instance.validity_duration = None
            cls._instance.total_amount = None
            cls._instance.moto_indicator = False
            cls._instance.purchaseAmount = 0.0

            cls._instance.invoice_number = ''
            cls._instance.message_function = ''




        # Return the Singleton instance

        return cls._instance

    # Method to format amounts to 2 decimals
    @staticmethod
    def format_amount(amount):
        try:
            # Convert to float if amount is not already a float
            amount = float(amount)
            return f"{amount:.2f}"
        except (ValueError, TypeError):
            # Handle cases where conversion fails
            return "0.00"

    # Method to get the status string
    def get_status_string(self):
        return self.status

    # Method to get the terminal status string
    def get_terminal_status_string(self):
        return self.terminalStatus

    # Method to print the transaction data
    def __str__(self):
        return (f"TransactionData(isRunning: {self.isRunning},"
                f"ErrorScrenario: {self.get_status_string()}, tipAmount: {self.format_amount(self.tipAmount)}, "
                f"cashback: {self.format_amount(self.cashback)}, surchargeFee: {self.format_amount(self.surchargeFee)}, "
                f"serviceFee: {self.format_amount(self.serviceFee)}, enableSignature: {self.enableSignature}, "
                f"currencyCode: {self.currencyCode}, splitPayment: {self.splitPayment}, "
                f"splitAmount: {self.format_amount(self.splitAmount)}, terminalStatus: {self.get_terminal_status_string()}, "
                f"message_function: {self.message_function}, transactionType: {self.transactionType}, identification: {self.identification} ")
                
                

    # Optionally, reset the Singleton instance if needed (e.g., for testing purposes)
    def reset_instance(self):
        self.isRunning = False
        self.status = StringUtily.TransactionStatus.NoneStatus
        self.tipAmount = 0.0
        self.cashback = 0.0
        self.surchargeFee = 0.0
        self.serviceFee = 0.0
        self.enableSignature = False
        self.currencyCode = 'USD'
        self.splitPayment = False
        self.splitAmount = 0.0
        self.terminalStatus = StringUtily.TerminalStatus.IDLE.name
        self.transactionType = StringUtily.ETransType.TT_SESSION_HEARTBEAT
        self.identification = ''
        self.type = ''
        self.respnseCode = ''
        self.responseMessage = ''
        self.transactionStatus = ''
        self.exchangeIdentification = ''
        self.service_attribute = None
        self.amount_qualifier   = None
        self.validity_duration  = None
        self.total_amount       = None
        self.moto_indicator     = False
        self.purchaseAmount     = 0.0
        self.invoice_number     = ''
        self.message_function   = ''

# Example usage
if __name__ == "__main__":
    # Accessing the Singleton instance
    transaction = TransactionData()

    # Setting values
    transaction.isRunning = True
   
    transaction.status = StringUtily.TransactionStatus.NoneStatus
    transaction.tipAmount = 5.25
    transaction.cashback = 2.5
    transaction.surchargeFee = 1.5
    transaction.serviceFee = 3.0
    transaction.enableSignature = True
    transaction.currencyCode = "USD"
    transaction.splitPayment = True
    transaction.splitAmount = 10.00
    transaction.terminalStatus = StringUtily.TerminalStatus.BUSY.name
    transaction.messageFunction = StringUtily.get_message_function(StringUtily.ETransType.TT_SALE)
    transaction.transactionType = StringUtily.ETransType.TT_SALE

    # Print the transaction data
    print(transaction)  # Should print the current state of the transaction data

    # Accessing the Singleton instance again (ensures the same instance is used)
    another_transaction = TransactionData()
    print(another_transaction == transaction)  # Should print 'True' because they are the same instance

    print(StringUtily.get_transaction_type("AUTQ"))  # Should print 'TT_SALE'