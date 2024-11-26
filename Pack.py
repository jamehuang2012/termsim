import asyncio
import datetime
import json
import os
import struct
import uuid
import LoggerManager
import Transaction
import Constants
import sessionmgr
from monitor import Monitor, log_monitor  # Ensure correct import


def  getTransctionType():
    v = Transaction.Transaction().getInstance();

    #print(v.transactionType)
    #print(Constants.TransctionType.SALE)

    if ( v.transactionType == Constants.TransctionType.SALE):
        return "AUTQ"
    elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
        return "SASQ"

    else:
        v.transactionType = Constants.TransctionType.SESSIONMGR
        return "SASQ"


def  createRequest():
    
    # get current UTC time
    now = datetime.datetime.utcnow()

    # format the time string with milliseconds
    utc_string = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    
    random_uuid = uuid.uuid4()

    v = Transaction.Transaction().getInstance()

    if (v.transactionType != Constants.TransctionType.SESSIONMGR):
        random_uuid = v.xchagId
    

    #print("UUID:", random_uuid)

    initg_pty = sessionmgr.InitiatingParty(Constants.TID,Constants.AuthKey,"TID")
    rcpt_pty = sessionmgr.InitiatingParty(Constants.PID,"","PID")


    msgFunction = getTransctionType()

    #if (v.transactionType == Constants.TransctionType.SALE):
    #    print("SALE")
    #elif (v.transactionType == Constants.TransctionType.SESSIONMGR):
    #    msgFunction = "SASQ"

    hdr = sessionmgr.Header(msgFunction,"3.0",uuid.uuid4(),utc_string,initg_pty)

    #print(json.dumps(hdr.to_dict()))

    poi_grp_id = sessionmgr.POIGroupIdentification("NOTI")

    poi_cmpnt = sessionmgr.POIComponent(poi_grp_id,"IDLE")

    ssn_mgmt_req = sessionmgr.SessionManagementRequest(poi_cmpnt)
    
    oc_ssn_mgmt_req = sessionmgr.OCsessionManagementRequest(hdr,ssn_mgmt_req)

    request = sessionmgr.Request(oc_ssn_mgmt_req)

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
    #log = LoggerManager.LoggerManager().logger
    #log.debug("Packed Data: %s", packed_data)
    return packed_data

def parseRequest(packed_data):
    # Step 1: Extract the length of the request (first 4 bytes)
    total_length = struct.unpack('>I', packed_data[:4])[0]
    
    # Step 2: Extract the header (next 4 bytes)
    header = packed_data[4:8].hex()  # Convert bytes to hexadecimal string
    
    # Step 3: Extract the random digits (next 8 bytes)
    random_digits = packed_data[8:16]
    
    # Step 4: Extract the original request data (remaining bytes)
    request_data = packed_data[16:].decode()  # Decode bytes to string

    # Semd monitor data
    
    log_monitor("Cloud --> Network", request_data)

    # Logging extracted information
    #log = LoggerManager.LoggerManager().logger
    #log.debug("Parsed Data: Length=%d, Header=%s, Random Digits=%s, Request Data=%s",
    #          total_length, header, random_digits.hex(), request_data)
    
    # Return parsed components as a dictionary
    return {
        "length": total_length,
        "header": header,
        "random_digits": random_digits.hex(),
        "request_data": request_data
    }
