import asyncio
import datetime
import json
import os
import struct
import uuid
from Header import Header, Party
import LoggerManager

from ParameterSingleton import ParameterSingleton
from ServiceResponse import AuthorisationResult, DetailedAmount, OCserviceResponse, PackServiceResponse, PaymentResponse, Receipt, ReceiptDetails, Response, ResponseToAuthorisation, RetailerPaymentResult, ServiceResponse, TransactionDetails, TransactionIdentification, TransactionResponse
import StringUtily
import Transaction

from TransactionData import TransactionData
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
        random_uuid = v.xchagId

    #print("UUID:", random_uuid)

    tid = p.get_tid()
    #pid = p.get_pid()
    authkey = p.get_auth_key()

    # check transactionType empty or none 

    if v.transactionType == None or v.transactionType == "":
        v.transactionType = StringUtily.ETransType.TT_SESSION_HEARTBEAT

    log = LoggerManager.LoggerManager().logger
    log.debug(v.transactionType)


    if v.transactionType in [StringUtily.ETransType.TT_SESSION_HEARTBEAT, StringUtily.ETransType.TT_SESSION_MGR_PAT]:
    
        log.debug("Session Management Request")

        initg_pty = sessionmgr.Party(tid,authkey,"TID")
        #rcpt_pty = sessionmgr.InitiatingParty(pid,"","PID")


        message_function = StringUtily.get_message_function(v.transactionType)

        #if (v.transactionType == Constants.TransctionType.SALE):
        #    print("SALE")
        #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
        #    msgFunction = "SASQ"

        hdr = sessionmgr.Header(message_function,"3.0",random_uuid,utc_string,initg_pty)

        #print(json.dumps(hdr.to_dict()))

        poi_grp_id = sessionmgr.POIGroupIdentification("NOTI")

        poi_cmpnt = sessionmgr.POIComponent(poi_grp_id,"IDLE")

        ssn_mgmt_req = sessionmgr.SessionManagementRequest(poi_cmpnt)
        
        oc_ssn_mgmt_req = sessionmgr.OCsessionManagementRequest(hdr,ssn_mgmt_req)

        request = sessionmgr.Request(oc_ssn_mgmt_req)

        return json.dumps(request.to_dict())
    elif v.transactionType in [StringUtily.ETransType.TT_SALE, StringUtily.ETransType.TT_REFUND, 
                               StringUtily.ETransType.TT_VOID, StringUtily.ETransType.TT_CREDIT_PREAUTH,
                               StringUtily.ETransType.TT_CREDIT_PREAUTH_COMPLETION, StringUtily.ETransType.TT_TIP_ADJUSTMENT,
                               StringUtily.ETransType.TT_CREDIT_INCREMENTAL_AUTH]:
        message_function = StringUtily.get_response_message_function(v.transactionType)

        initg_pty = Party(tid,authkey,"TID")
        rcpt_pty = Party(TransactionData().identification,"",TransactionData().type)

        now = datetime.datetime.utcnow()
        utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


       

            #if (v.transactionType == Constants.TransctionType.SALE):
            #    print("SALE")
            #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
            #    msgFunction = "SASQ"

        hdr = Header(message_function,"3.0",random_uuid,utc_string,initg_pty,rcpt_pty)

        response = Response("APPR")  # Successful response code

        #fill the receipt details
        term_num = ParameterSingleton().get_tid()
        record_num = StringUtily.generate_record_num()
        host_invoice_num = StringUtily.generate_host_invoice_num()
        host_seq_num = "10010002640"
        merch_invoice_num = "10002640"
        card_num = "************0401"
        card_type = "CREDIT/AMEX"
        date = datetime.datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        amount = TransactionData().total_amount
        auth_num = StringUtily.generate_auth_num()
        hts_num = StringUtily.generate_HTS()
        aid_num = "A0000000041010"
        tc_num = "017AA200ACFBD5CC"
        tvr_num = "0440008000"
        tsi_num = "E800"
 
        copy_type = "Customer Copy"
        receipt_cust = ReceiptGenerator(term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num, copy_type)
        
        # replace '\n' to '|' in the receipt
        receipt_cust = receipt_cust.replace('\n', '|')
        
        copy_type = "Merchant Copy"
        
        receipt_merchant = ReceiptGenerator(term_num, record_num, host_invoice_num, host_seq_num, merch_invoice_num, card_num, card_type, date, amount, auth_num, hts_num, aid_num, tc_num, tvr_num, tsi_num, copy_type)
        # replace '\n' to '|' in the receipt
        receipt_merchant = receipt_merchant.replace('\n', '|')


        receipt1 = Receipt(receipt_cust, "CRCP")
        receipt2 = Receipt(receipt_merchant, "HRCP")

        transaction_identification = TransactionIdentification(
            datetime.datetime.now(), record_num
        )

        detailed_amount = DetailedAmount(0.00, 0.00, 0.00, 0.00)
        transaction_details = TransactionDetails(TransactionData().total_amount, detailed_amount)

        response_to_authorisation = ResponseToAuthorisation("APPR")
        authorisation_result = AuthorisationResult(auth_num, response_to_authorisation)

        # fill the receipt details
        '''
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
        '''

        receipt_details = ReceiptDetails(
            record_number=record_num,mask_pan=card_num,card_aid=aid_num,card_lbl=card_type,emv_tag_tsi=tsi_num,emv_tag_tvr=tvr_num,balance_due=amount,account_type="CREDIT",apprdecl_iso="APPR",host_invoice=host_invoice_num,host_sequence=host_seq_num,invoice_number=merch_invoice_num,card_data_ntry_md="CHIP",emv_tag_cryptogram=tc_num)
        


        transaction_response = TransactionResponse(
            "", receipt_details, transaction_details, authorisation_result
        )

        retailer_payment_result = RetailerPaymentResult("CRDR", transaction_response)

        payment_response = PaymentResponse(
            [receipt1, receipt2],
            retailer_payment_result,
            "SaleRef123",
            transaction_identification,
            transaction_identification
        )

        service_response = ServiceResponse(response, [payment_response])
        oc_service_response = OCserviceResponse(hdr, service_response)

        request = PackServiceResponse(oc_service_response)

        # Display the dictionary (or convert to JSON for a more readable format)
       
        return json.dumps(request.to_dict())

                               
                             




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
    return packed_data

