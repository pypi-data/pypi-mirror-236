"""tdx数据结构转换器"""
import datetime
from pytdx.params import TDXParams
from enum import Enum
from vxutils.database.dataconvertor import vxDataConvertor
from vxquant.datamodels.core import vxTick
from vxquant.datamodels.preset import vxMarketPreset
from vxquant.datamodels.contants import SecType


class TDXExchange(Enum):
    """通达信市场转换"""

    SHSE = TDXParams.MARKET_SH
    SZSE = TDXParams.MARKET_SZ
    BJSE = 2


def to_tdx_symbol(symbol):
    """转成tdx的symbol格式: (market,code)

    Arguments:
        symbol {_type_} -- symbol
    """
    market, code = symbol.split(".")
    return (TDXExchange[market].value, code)


def parser_tdx_symbol(market, code):
    """将tdx的symbol格式转化成symbol："SHSE.0000001"

    Arguments:
        market {_type_} -- tdx 的market代码
        code {_type_} -- 证券代码
    """
    return f"{TDXExchange(market).name}.{code}"


def tdx_to_timestamp(tdx_timestamp, trade_day=None):
    """通达信时间戳转换为时间戳"""
    if trade_day is None:
        trade_day = datetime.datetime.now()

    tdx_timestamp = f"{tdx_timestamp:0>8}"
    hour = int(tdx_timestamp[:2])
    if hour < 0 or hour > 23:
        tdx_timestamp = f"0{tdx_timestamp}"
        hour = int(tdx_timestamp[:2])

    minute = int(tdx_timestamp[2:4])
    percent = float(f"0.{tdx_timestamp[2:]}")
    if minute < 60:
        second = int(percent * 60)
        microsecond = int((percent * 60 - second) * 1000)
    else:
        minute = int(percent * 60)
        second = int((percent * 60 - minute) * 60)
        microsecond = int(((percent * 60 - minute) * 60 - second) * 1000)
    return datetime.datetime(
        trade_day.year,
        trade_day.month,
        trade_day.day,
        hour,
        minute,
        second,
        microsecond,
    ).timestamp()


_TICK_CONVERTORS = {
    "symbol": lambda x: f"{TDXExchange(x['market']).name}.{x['code']}",
    "open": "open",
    "high": "high",
    "low": "low",
    "lasttrade": lambda x: x["price"] or x["last_close"],
    "yclose": "last_close",
    "volume": "vol",
    "amount": "amount",
    "turnoverratio": 0.0,
    "bid1_v": "bid_vol1",
    "bid1_p": "bid1",
    "bid2_v": "bid_vol2",
    "bid2_p": "bid2",
    "bid3_v": "bid_vol3",
    "bid3_p": "bid3",
    "bid4_v": "bid_vol4",
    "bid4_p": "bid4",
    "bid5_v": "bid_vol5",
    "bid5_p": "bid5",
    "ask1_v": "ask_vol1",
    "ask1_p": "ask1",
    "ask2_v": "ask_vol2",
    "ask2_p": "ask2",
    "ask3_v": "ask_vol3",
    "ask3_p": "ask3",
    "ask4_v": "ask_vol4",
    "ask4_p": "ask4",
    "ask5_v": "ask_vol5",
    "ask5_p": "ask5",
    "interest": lambda x: 0,
    "status": lambda x: "NORMAL",
    "created_dt": lambda x: tdx_to_timestamp(x["reversed_bytes0"]),
    "updated_dt": lambda x: tdx_to_timestamp(x["reversed_bytes0"]),
}

volume_cols = [
    "bid1_v",
    "bid2_v",
    "bid3_v",
    "bid4_v",
    "bid5_v",
    "ask1_v",
    "ask2_v",
    "ask3_v",
    "ask4_v",
    "ask5_v",
    "volume",
]

price_cols = [
    "open",
    "high",
    "low",
    "lasttrade",
    "yclose",
    "bid1_p",
    "bid2_p",
    "bid3_p",
    "bid4_p",
    "bid5_p",
    "ask1_p",
    "ask2_p",
    "ask3_p",
    "ask4_p",
    "ask5_p",
]


_tdxTickConvter = vxDataConvertor(vxTick, _TICK_CONVERTORS)


def tdxTickConvter(dataobj, key: str = "") -> vxTick:
    if key:
        key, dataobj = _tdxTickConvter(dataobj, key=key)
    else:
        dataobj = _tdxTickConvter(dataobj)

    preset = vxMarketPreset(dataobj.symbol)

    volume_unit = 100
    price_unit = 10
    if preset.security_type in [SecType.STOCK, SecType.INDEX]:
        volume_unit = 100
        price_unit = 1
    elif preset.security_type in [SecType.BOND_CONVERTIBLE, SecType.BOND, SecType.REPO]:
        volume_unit = 100
        price_unit = 100

    for col in volume_cols:
        dataobj[col] *= volume_unit

    for col in price_cols:
        dataobj[col] /= price_unit

    return (key, dataobj) if key else dataobj
