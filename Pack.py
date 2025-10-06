import asyncio
import datetime
import json
import os
import struct
import uuid
from FIFOStatusSender import FIFOStatusSender
from Header import Header, Party
import LoggerManager

from ParameterSingleton import ParameterSingleton
from ServiceResponse import AuthorisationResult, DetailedAmount, OCserviceResponse, PackServiceResponse, PaymentResponse, Receipt, ReceiptDetails, Response, ResponseToAuthorisation, RetailerPaymentResult, ReversalResponse, ServiceResponse, TransactionDetails, TransactionIdentification, TransactionResponse
import StringUtily

from TransactionDB import TransactionDB
from TransactionData import TransactionData
from card import get_aid_number, get_app_name, get_card_type, get_masked_pan, get_random_card
from print import write_receipt_fifo
from receipt import ReceiptGenerator
import sessionmgr
from monitor import Monitor, log_monitor  # Ensure correct import




def  createRequest():
    
    # get current UTC time
    now = datetime.datetime.utcnow()

    # format the time string with milliseconds
    utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    
    random_uuid = uuid.uuid4()

    v = TransactionData()

    p = ParameterSingleton()

   
    if v.transactionType not in  [StringUtily.ETransType.TT_SESSION_HEARTBEAT]: 
        random_uuid = v.exchangeIdentification
    #print("UUID:", random_uuid)

    tid = p.get_tid()
    #pid = p.get_pid()
    authkey = p.get_auth_key()

    # check transactionType empty or none 

    if v.transactionType == None or v.transactionType == "":
        v.transactionType = StringUtily.ETransType.TT_SESSION_HEARTBEAT

    log = LoggerManager.LoggerManager().logger
    log.debug(v.transactionType)

    if v.status in [ StringUtily.TransactionStatus.Cancellation]:
        v.cancelStatus = True
 
    if v.cancelStatus == True and TransactionData().transactionStatus == "ACPT":
        
        initg_pty = Party(tid,"TID",authkey)
        #rcpt_pty = sessionmgr.InitiatingParty(pid,"","PID")


        message_function = StringUtily.get_message_function(StringUtily.ETransType.TT_SESSION_HEARTBEAT)

        #if (v.transactionType == Constants.TransctionType.SALE):
        #    print("SALE")
        #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
        #    msgFunction = "SASQ"

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty)

        #print(json.dumps(hdr.to_dict()))
        log = LoggerManager.LoggerManager().logger
        log.debug(TransactionData().exchangeIdentification)

        poi_grp_id = sessionmgr.POIGroupIdentification(exchange_action="CUCL",exchange_identification=TransactionData().exchangeIdentification)

        poi_cmpnt = sessionmgr.POIComponent(poi_grp_id,TransactionData().terminalStatus)

        ssn_mgmt_req = sessionmgr.SessionManagementRequest(poi_cmpnt)
        
        oc_ssn_mgmt_req = sessionmgr.OCsessionManagementRequest(hdr,ssn_mgmt_req)

        request = sessionmgr.Request(oc_ssn_mgmt_req)

        v.cancelStatus = False

        return json.dumps(request.to_dict())
     

    elif v.transactionType in [StringUtily.ETransType.TT_SESSION_HEARTBEAT, StringUtily.ETransType.TT_SESSION_MGR_PAT] or v.status in [StringUtily.TransactionStatus.NoResponse, StringUtily.TransactionStatus.Cancellation]:
    
        log.debug("Session Management Request")

        initg_pty = Party(tid,"TID",authkey)
        #rcpt_pty = sessionmgr.InitiatingParty(pid,"","PID")


        message_function = StringUtily.get_message_function(v.transactionType)

        #if (v.transactionType == Constants.TransctionType.SALE):
        #    print("SALE")
        #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
        #    msgFunction = "SASQ"

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty)

        #print(json.dumps(hdr.to_dict()))

        poi_grp_id = sessionmgr.POIGroupIdentification("NOTI",None)

        poi_cmpnt = sessionmgr.POIComponent(poi_grp_id,TransactionData().terminalStatus)

        ssn_mgmt_req = sessionmgr.SessionManagementRequest(poi_cmpnt)
        
        oc_ssn_mgmt_req = sessionmgr.OCsessionManagementRequest(hdr,ssn_mgmt_req)

        request = sessionmgr.Request(oc_ssn_mgmt_req)

        return json.dumps(request.to_dict())
    elif v.transactionType in [StringUtily.ETransType.TT_SALE, StringUtily.ETransType.TT_REFUND, 
                                StringUtily.ETransType.TT_CREDIT_PREAUTH,
                                StringUtily.ETransType.TT_TIP_ADJUSTMENT,
                               
                               StringUtily.ETransType.TT_CRYPTO, StringUtily.ETransType.TT_MOTO]:
        message_function = StringUtily.get_response_message_function(v.transactionType)

        initg_pty = Party(tid,"TID",authkey)
        rcpt_pty = Party(TransactionData().identification,TransactionData().type)

        now = datetime.datetime.now(datetime.timezone.utc)

        utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


       

            #if (v.transactionType == Constants.TransctionType.SALE):
            #    print("SALE")
            #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
            #    msgFunction = "SASQ"

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty,rcpt_pty)



        TransactionData().entryMode = StringUtily.EntryMode.EM_SMC

        # Get card data
        card = get_random_card()
        

        #fill the receipt details
        term_num = ParameterSingleton().get_tid()
        record_num = StringUtily.generate_record_number()
        host_invoice_num = StringUtily.generate_host_invoicenum()
        host_seq_num = "10010002640"
        merch_invoice_num = "10002640"
        card_num = get_masked_pan(card)
        card_type = "CREDIT/" + get_card_type(card)
        date = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        amount = TransactionData().totalAmount
        auth_num = StringUtily.generate_auth_code()
        hts_num = StringUtily.generate_hts()
        aid_num = get_aid_number(card)
        tc_num = "017AA200ACFBD5CC"
        tvr_num = "0440008000"
        tsi_num = "E800"
 
        copy_type = "Customer Copy"

        transaction_name = "SALE"
        if v.transactionType == StringUtily.ETransType.TT_REFUND:
            transaction_name = "REFUND"
        elif v.transactionType == StringUtily.ETransType.TT_VOID:
            transaction_name = "VOID"
        elif v.transactionType == StringUtily.ETransType.TT_CREDIT_PREAUTH:
            if (v.serviceAttribute == "IRES"):
                transaction_name = "PREAUTH"
            elif (v.serviceAttribute == "URES"):
                transaction_name = "INCREMENTAL AUTH"
            else:
                transaction_name = "PREAUTH"

        elif v.transactionType == StringUtily.ETransType.TT_CREDIT_PREAUTH_COMPLETION:
            transaction_name = "PREAUTH COMPLETION"
        elif v.transactionType == StringUtily.ETransType.TT_TIP_ADJUSTMENT:
            transaction_name = "TIP ADJUSTMENT"
        elif v.transactionType == StringUtily.ETransType.TT_CREDIT_INCREMENTAL_AUTH:
            transaction_name = "INCREMENTAL AUTH"
        elif v.transactionType == StringUtily.ETransType.TT_SALE:
            transaction_name = "SALE"
        elif v.transactionType == StringUtily.ETransType.TT_CRYPTO:
            transaction_name = "CRYPTO"
        elif v.transactionType == StringUtily.ETransType.TT_MOTO:
            transaction_name = "MOTO"

        card_type_name = get_card_type(card)
        
        app_name = get_app_name(card)

        entry_mode = StringUtily.get_card_data_entry_mode(TransactionData().entryMode)        
            

        r1 = ReceiptGenerator(term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num, copy_type,transaction_name,app_name)
        
        receipt_cust = r1.generate_receipt()
        # replace '\n' to '|' in the receipt
        receipt_cust = receipt_cust.replace('\n', '|')
        
        copy_type = "Merchant Copy"
        
        r2 = ReceiptGenerator(term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num, copy_type,transaction_name,app_name)
        # replace '\n' to '|' in the receipt
        receipt_merchant = r2.generate_receipt()
        receipt_merchant = receipt_merchant.replace('\n', '|')

        # Write receipt log to /tmp/cust_fifo and /tmp/merch_fifo write write_receipt_fifo
        #call it ascynchronously
        asyncio.run(write_receipt_fifo("/tmp/cust_fifo", receipt_merchant))
        asyncio.run(write_receipt_fifo("/tmp/merc_fifo", receipt_cust))



        receipt1 = Receipt(receipt_cust, "CRCP")
        receipt2 = Receipt(receipt_merchant, "HRCP")

        transaction_identification = TransactionIdentification(
            datetime.datetime.now(), record_num
        )

        response = None
        
        if v.status in [StringUtily.TransactionStatus.Decline]:
            response = Response("DECL")
        else:
            response = Response("APPR")  # Successful response code



        detailed_amount = DetailedAmount("0.00", "0.00", "0.00", "0.00")
        transaction_details = TransactionDetails(TransactionData().totalAmount, detailed_amount)

        response_to_authorisation = ResponseToAuthorisation("APPR")

        if v.status in [StringUtily.TransactionStatus.Decline]:
            response_to_authorisation = ResponseToAuthorisation("DECL")


        authorisation_result = AuthorisationResult(auth_num, response_to_authorisation)



        # fill the receipt details
       

        receipt_details = ReceiptDetails(
           ref_id=record_num, record_number=record_num,msk_pan=card_num,card_aid=aid_num,card_lbl=app_name,emv_tag_tsi=tsi_num,emv_tag_tvr=tvr_num,balance_due=amount,account_type=app_name,apprdecl_iso="APPR",host_invoice=host_invoice_num,host_sequence=host_seq_num,invoice_number=merch_invoice_num,card_data_ntry_md=entry_mode,emv_tag_cryptogram=tc_num)

        # generate signature
        #signature = StringUtily.generate_signature(text="NTS",font_size=30)

        signature = ""

        if TransactionData().enableSignature:
            signature = StringUtily.load_signature_from_image("signature.png")


        transaction_response = TransactionResponse(
            signature, receipt_details, transaction_details, authorisation_result
        )


        type_transaction_total = None

        if v.transactionType in [StringUtily.ETransType.TT_SALE, StringUtily.ETransType.TT_REFUND]:
            type_transaction_total = "CRDT"
        elif v.transactionType in [StringUtily.ETransType.TT_VOID]:
            type_transaction_total = "CRDR"
        elif v.transactionType in [StringUtily.ETransType.TT_CREDIT_PREAUTH, StringUtily.ETransType.TT_CREDIT_PREAUTH_COMPLETION, StringUtily.ETransType.TT_TIP_ADJUSTMENT, StringUtily.ETransType.TT_CREDIT_INCREMENTAL_AUTH, StringUtily.ETransType.TT_CRYPTO, StringUtily.ETransType.TT_MOTO]:
            type_transaction_total = "CRDT"
        else: 
            type_transaction_total = "CRDT"

        retailer_payment_result = RetailerPaymentResult(type_transaction_total, transaction_response)

        payment_response = None 
        reversal_response = None

        if v.transactionType in [StringUtily.ETransType.TT_VOID]:
            reversal_response = ReversalResponse(
                [receipt1, receipt2],
                retailer_payment_result,
                transaction_identification,
                transaction_identification,
               
            )

        else:

            payment_response = PaymentResponse(
                [receipt1, receipt2],
                retailer_payment_result,
                record_num,
                transaction_identification,
                transaction_identification
            )


        batch_response = None

        if TransactionData().status not in [StringUtily.TransactionStatus.NoneStatus]:
            payment_response = None
            reversal_response = None

        service_response = ServiceResponse(response, [payment_response],reversal_response,batch_response)
        oc_service_response = OCserviceResponse(hdr, service_response)

        request = PackServiceResponse(oc_service_response)





        #Insert the transaction data into database from TransactoinDB    
        # try:
        #     db = TransactionDB()

        #     transaction_data = (
        #         "", TransactionData().entryMode.name, TransactionData().clerkId, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), TransactionData().reconciliationIndentifier,
        #         TransactionData().invoiceNumber, record_num,  auth_num,TransactionData().responseMessage, TransactionData().transactionType.name, card_type_name, amount,
        #         TransactionData().purchaseAmount, TransactionData().tipAmount, TransactionData().cashback, TransactionData().surchargeFee,TransactionData().serviceFee, tid, "mid", aid_num,
        #         tvr_num, tc_num, app_name, host_seq_num, host_seq_num,
        #         datetime.datetime.now().strftime("%Y-%m-%d"), datetime.datetime.now().strftime("%H:%M:%S"), tsi_num, record_num, TransactionData().serviceAttribute,
        #        TransactionData().amountQualifier, TransactionData().validityDuration, TransactionData().motoIndicator
        #     )

        #     # Log the transaction data
        #     log.info("Transaction Data: %s", transaction_data)

        #     db.insert_transaction(transaction_data)
        #     db.close()
        # except Exception as e:
        #     log.error("Error inserting transaction data into database: %s", e)

        

        # Display the dictionary (or convert to JSON for a more readable format)

        if TransactionData().responseCode:
            TransactionData().responseCode = "N/A"

        status_data = {
            "TerminalStatus": TransactionData().get_terminal_status_string(),
            "TransactionStatus": "RSPN",
            "Response": TransactionData().responseCode,
            "CancelStatus": "N/A"
        }
        sender = FIFOStatusSender()
        sender.send_status(status_data)
       
        return json.dumps(request.to_dict())
    
    elif v.transactionType in [StringUtily.ETransType.TT_VOID,StringUtily.ETransType.TT_CREDIT_PREAUTH_COMPLETION,
                               StringUtily.ETransType.TT_CREDIT_INCREMENTAL_AUTH]:
        # Void Response
        message_function = StringUtily.get_response_message_function(v.transactionType)

        initg_pty = Party(tid,"TID",authkey)
        rcpt_pty = Party(TransactionData().identification,TransactionData().type)

        now = datetime.datetime.utcnow()
        utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty,rcpt_pty)

        response = Response("APPR")

        # if response is successful, increment the batch number
        if response.responseCode == "APPR":
            p.increment_batch_number()
    elif v.transactionType in [StringUtily.ETransType.TT_BATCH_CLOSE_GENERAL]:
        # Batch Close Response
        message_function = StringUtily.get_response_message_function(v.transactionType)

        initg_pty = Party(tid,"TID",authkey)
        rcpt_pty = Party(TransactionData().identification,TransactionData().type)

        now = datetime.datetime.utcnow()
        utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty,rcpt_pty)

        response = Response("APPR")

        # if response is successful, increment the batch number
        if response.responseCode == "APPR":
            p.increment_batch_number()


    
    elif v.transactionType in [StringUtily.ETransType.TT_REPORT]:
        # Report Response

        message_function = StringUtily.get_response_message_function(v.transactionType)

        initg_pty = Party(tid,"TID",authkey)
        rcpt_pty = Party(TransactionData().identification,TransactionData().type)

        now = datetime.datetime.utcnow()
        utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty,rcpt_pty)

        response = Response("APPR")

def packReuqest():
    #print("pack data")
    req = createRequest()
  
    log_monitor("Network --> Cloud", req)

    random_bytes = os.urandom(8)
    random_digits = random_bytes[:8]


    packed_length = struct.pack('>I', len(req)+12)
    packed_data = packed_length + bytes.fromhex("01000201") + random_digits +  req.encode()
    
    #print(packed_data)
    log = LoggerManager.LoggerManager().logger
    log.debug("Packed Data: %s", req)
    log.debug("length of packed data: %d", len(req))

    # log packed data with hex format
    log.debug("Packed Data: %s", packed_data.hex())

    return packed_data

