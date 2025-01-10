from datetime import date 
from pydantic import BaseModel

class PaystubSection(BaseModel):
    section_code: str
    paydate: date 
    typecode: str
    typedesc: str
    amount: str 


class Deductions(PaystubSection):
    expectamt: str 

class Taxes(PaystubSection):
    grosswages: str
    dductwages: str 

class NetPay(PaystubSection):
    chkpayamt: str 
    checknum: int
    directdepo: int 