# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome10_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser
import json

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None
    return x


class Pty:
    id: int
    tp: str
    shr_nm: str

    def __init__(self, id: int, tp: str, shr_nm: str) -> None:
        self.id = id
        self.tp = tp
        self.shr_nm = shr_nm

    @staticmethod
    def from_dict(obj: Any) -> 'Pty':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("Id")))
        tp = from_str(obj.get("Tp"))
        shr_nm = from_str(obj.get("ShrNm"))
        return Pty(id, tp, shr_nm)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_str(str(self.id))
        result["Tp"] = from_str(self.tp)
        result["ShrNm"] = from_str(self.shr_nm)
        return result


class Hdr:
    msg_fctn: str
    prtcol_vrsn: str
    xchg_id: UUID
    cre_dt_tm: datetime
    initg_pty: Pty
    rcpt_pty: Pty

    def __init__(self, msg_fctn: str, prtcol_vrsn: str, xchg_id: UUID, cre_dt_tm: datetime, initg_pty: Pty, rcpt_pty: Pty) -> None:
        self.msg_fctn = msg_fctn
        self.prtcol_vrsn = prtcol_vrsn
        self.xchg_id = xchg_id
        self.cre_dt_tm = cre_dt_tm
        self.initg_pty = initg_pty
        self.rcpt_pty = rcpt_pty

    @staticmethod
    def from_dict(obj: Any) -> 'Hdr':
        assert isinstance(obj, dict)
        msg_fctn = from_str(obj.get("MsgFctn"))
        prtcol_vrsn = from_str(obj.get("PrtcolVrsn"))
        xchg_id = UUID(obj.get("XchgId"))
        cre_dt_tm = from_datetime(obj.get("CreDtTm"))
        initg_pty = Pty.from_dict(obj.get("InitgPty"))
        rcpt_pty = Pty.from_dict(obj.get("RcptPty"))
        return Hdr(msg_fctn, prtcol_vrsn, xchg_id, cre_dt_tm, initg_pty, rcpt_pty)

    def to_dict(self) -> dict:
        result: dict = {}
        result["MsgFctn"] = from_str(self.msg_fctn)
        result["PrtcolVrsn"] = from_str(self.prtcol_vrsn)
        result["XchgId"] = str(self.xchg_id)
        result["CreDtTm"] = self.cre_dt_tm.isoformat()
        result["InitgPty"] = to_class(Pty, self.initg_pty)
        result["RcptPty"] = to_class(Pty, self.rcpt_pty)
        return result


class Cntxt:
    cshr_id: int

    def __init__(self, cshr_id: int) -> None:
        self.cshr_id = cshr_id

    @staticmethod
    def from_dict(obj: Any) -> 'Cntxt':
        assert isinstance(obj, dict)
        cshr_id = int(from_str(obj.get("CshrId")))
        return Cntxt(cshr_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CshrId"] = from_str(str(self.cshr_id))
        return result


class Mrchnt:
    id: str

    def __init__(self, id: str) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'Mrchnt':
        assert isinstance(obj, dict)
        id = from_str(obj.get("Id"))
        return Mrchnt(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Id"] = from_str(self.id)
        return result


class Envt:
    mrchnt: Mrchnt
    poi: Mrchnt

    def __init__(self, mrchnt: Mrchnt, poi: Mrchnt) -> None:
        self.mrchnt = mrchnt
        self.poi = poi

    @staticmethod
    def from_dict(obj: Any) -> 'Envt':
        assert isinstance(obj, dict)
        mrchnt = Mrchnt.from_dict(obj.get("Mrchnt"))
        poi = Mrchnt.from_dict(obj.get("POI"))
        return Envt(mrchnt, poi)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Mrchnt"] = to_class(Mrchnt, self.mrchnt)
        result["POI"] = to_class(Mrchnt, self.poi)
        return result


class TxDtls:
    ttl_amt: str

    def __init__(self, ttl_amt: str) -> None:
        self.ttl_amt = ttl_amt

    @staticmethod
    def from_dict(obj: Any) -> 'TxDtls':
        assert isinstance(obj, dict)
        ttl_amt = from_str(obj.get("TtlAmt"))
        return TxDtls(ttl_amt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["TtlAmt"] = from_str(self.ttl_amt)
        return result


class PmtReq:
    tx_tp: str
    tx_id: None
    tx_dtls: TxDtls

    def __init__(self, tx_tp: str, tx_id: None, tx_dtls: TxDtls) -> None:
        self.tx_tp = tx_tp
        self.tx_id = tx_id
        self.tx_dtls = tx_dtls

    @staticmethod
    def from_dict(obj: Any) -> 'PmtReq':
        assert isinstance(obj, dict)
        tx_tp = from_str(obj.get("TxTp"))
        tx_id = from_none(obj.get("TxId"))
        tx_dtls = TxDtls.from_dict(obj.get("TxDtls"))
        return PmtReq(tx_tp, tx_id, tx_dtls)

    def to_dict(self) -> dict:
        result: dict = {}
        result["TxTp"] = from_str(self.tx_tp)
        result["TxId"] = from_none(self.tx_id)
        result["TxDtls"] = to_class(TxDtls, self.tx_dtls)
        return result


class SVCReq:
    envt: Envt
    cntxt: Cntxt
    svc_cntt: str
    pmt_req: PmtReq

    def __init__(self, envt: Envt, cntxt: Cntxt, svc_cntt: str, pmt_req: PmtReq) -> None:
        self.envt = envt
        self.cntxt = cntxt
        self.svc_cntt = svc_cntt
        self.pmt_req = pmt_req

    @staticmethod
    def from_dict(obj: Any) -> 'SVCReq':
        assert isinstance(obj, dict)
        envt = Envt.from_dict(obj.get("Envt"))
        cntxt = Cntxt.from_dict(obj.get("Cntxt"))
        svc_cntt = from_str(obj.get("SvcCntt"))
        pmt_req = PmtReq.from_dict(obj.get("PmtReq"))
        return SVCReq(envt, cntxt, svc_cntt, pmt_req)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Envt"] = to_class(Envt, self.envt)
        result["Cntxt"] = to_class(Cntxt, self.cntxt)
        result["SvcCntt"] = from_str(self.svc_cntt)
        result["PmtReq"] = to_class(PmtReq, self.pmt_req)
        return result


class OCSVCReq:
    hdr: Hdr
    svc_req: SVCReq

    def __init__(self, hdr: Hdr, svc_req: SVCReq) -> None:
        self.hdr = hdr
        self.svc_req = svc_req

    @staticmethod
    def from_dict(obj: Any) -> 'OCSVCReq':
        assert isinstance(obj, dict)
        hdr = Hdr.from_dict(obj.get("Hdr"))
        svc_req = SVCReq.from_dict(obj.get("SvcReq"))
        return OCSVCReq(hdr, svc_req)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Hdr"] = to_class(Hdr, self.hdr)
        result["SvcReq"] = to_class(SVCReq, self.svc_req)
        return result


class Welcome10:
    oc_svc_req: OCSVCReq

    def __init__(self, oc_svc_req: OCSVCReq) -> None:
        self.oc_svc_req = oc_svc_req

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome10':
        assert isinstance(obj, dict)
        oc_svc_req = OCSVCReq.from_dict(obj.get("OCSvcReq"))
        return Welcome10(oc_svc_req)

    def to_dict(self) -> dict:
        result: dict = {}
        result["OCSvcReq"] = to_class(OCSVCReq, self.oc_svc_req)
        return result


def ParseOCSvcReq(s: Any) -> Welcome10:
    return Welcome10.from_dict(s)




with open("ocreq.json", 'r') as f:
    v = ParseOCSvcReq(json.load(f))
    print(v.oc_svc_req.hdr.msg_fctn)
    print(v.oc_svc_req.hdr.xchg_id)
    print(v.oc_svc_req.hdr.cre_dt_tm)    