from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Env(Enum):
    SANDBOX = 0
    PRODUCTION = 1
    
class PayType(Enum):
    Wechat = '400'
    Alipay = '300'

class PayMethod(Enum):
    MINIPROG = 'MINIPROG'

class GoodsDetail(BaseModel):
    goods_id: Optional[str] = None
    goods_name: Optional[str] = None
    goods_quantity: Optional[str] = None
    goods_price: Optional[str] = None

class PayResult(BaseModel):
    return_code: str
    return_msg: str
    result_code: Optional[str]
    mch_no: str
    shop_no: Optional[str]
    mch_name: str
    shop_name: Optional[str]
    pay_type: str
    pay_trace_no: str
    pay_time: str
    total_amount: str
    trade_no: str
    attach: Optional[str]
    appId: Optional[str]
    timeStamp: Optional[str]
    nonceStr: Optional[str]
    packages: Optional[str]
    signType: Optional[str]
    paySign: Optional[str]
    ali_trade_no: Optional[str]
    sign: str
    
class PayNotification(BaseModel):
    return_code: str
    return_msg: str
    result_code: str
    pay_type: str
    pay_trace_no: str
    pay_time: str
    end_time: Optional[str] = None
    inst_no: Optional[str] = None
    mch_no: Optional[str] = None
    mch_name: Optional[str] = None
    shop_no: Optional[str] = None
    shop_name: Optional[str] = None
    trade_no: str
    td_trade_no: Optional[str] = None
    qd_trade_no: Optional[str] = None
    o_trade_no: Optional[str] = None
    total_amount: str
    receipt_amount: Optional[str] = None
    pay_amount: Optional[str] = None
    coupon_amount: Optional[str] = None
    discount_amount: Optional[str] = None
    user_id: Optional[str]
    attach: Optional[str] = None
    sign: str