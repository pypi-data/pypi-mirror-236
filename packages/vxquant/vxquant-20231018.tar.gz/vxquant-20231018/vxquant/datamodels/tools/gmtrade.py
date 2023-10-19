"""gmtrade - 交易数据模型"""
import datetime
from pytdx.params import TDXParams
from enum import Enum
from vxutils.database.dataconvertor import vxDataConvertor
from vxquant.datamodels.core import vxTrade, vxOrder, vxPosition, vxAccountInfo
from vxquant.datamodels.preset import vxMarketPreset
from vxquant.datamodels.contants import SecType


_TRADE_CONVERTORS = {
    # 账户id
    "account_id": "account_id",
    # 委托id
    "order_id": "order_id",
    # 交易所委托id
    "exchange_order_id": "cl_ord_id",
    # 成交id
    "trade_id": "exec_id",
    # 证券代码
    "symbol": "symbol",
    # 买卖方向
    "order_direction": "side",
    # 开平仓标志
    "order_offset": "position_effect",
    # 成交价格
    "price": "price",
    # 成交数量
    "volume": "volume",
    # 交易佣金
    "commission": "commission",
    # 成交状态
    "status": "exec_type",
    # 拒绝代码
    "reject_code": "ord_rej_reason",
    # 拒绝原因
    "reject_reason": "ord_rej_reason_detail",
    # 创建时间
    "created_dt": lambda x: x.created_at["seconds"],
    # 更新时间
    "updated_dt": lambda x: x.created_at["seconds"],
}

gmtTradeConvertor = vxDataConvertor(vxTrade, _TRADE_CONVERTORS)

_ORDER_CONVERTORS = {
    # 账号id
    "account_id": "account_id",
    # 交易所委托id
    "exchange_order_id": "cl_ord_id",
    # 委托id
    "order_id": "order_id",
    # 证券代码
    "symbol": "symbol",
    # 买卖方向
    "order_direction": "side",
    # 开平仓标志
    "order_offset": "position_effect",
    # 订单类型
    "order_type": "order_type",
    # 委托数量
    "volume": "volume",
    # 委托价格
    "price": "price",
    # 成交数量
    "filled_volume": "filled_volume",
    # 成交均价
    "filled_vwap": "filled_vwap",
    # 成交总额（含手续费）
    "filled_amount": "filled_amount",
    # 订单状态
    "status": "status",
    # 拒绝代码
    "reject_code": "ord_rej_reason",
    # 拒绝原因
    "reject_reason": "ord_rej_reason_detail",
    # 创建时间
    "created_dt": lambda x: x.created_at["seconds"],
    # 更新时间
    "updated_dt": lambda x: x.created_at["seconds"],
}

gmtOrderConvertor = vxDataConvertor(vxOrder, _ORDER_CONVERTORS)

_POSITION_CONVERTORS = {
    # 账户id
    "account_id": "account_id",
    # 仓位id
    # "position_id": "position_id",
    # 证券代码
    "symbol": "symbol",
    # 持仓方向
    "position_side": "side",
    # 今日持仓数量
    "volume_today": "volume_today",
    # 昨日持仓数量
    "volume_his": lambda x: x.volume - x.volume_today,
    # 冻结数量
    "frozen": "order_frozen",
    # 持仓成本
    "cost": "cost",
    # 最近成交价
    "lasttrade": "price",
}

gmtPositionConvertor = vxDataConvertor(vxPosition, _POSITION_CONVERTORS)


_ACCOUNT_CONVERTORS = {
    # 账户id
    "account_id": "account_id",
    # 今日转入金额
    "deposit": lambda x: max(x.last_inout, 0),
    # 今日转出金额
    "withdraw": lambda x: -min(x.cum_inout, 0),
    # 净资产
    "nav": "nav",
    # 资金余额
    "balance": lambda x: x.order_frozen + x.available,
    # 冻结金额
    "frozen": "order_frozen",
    # 可用金额
    "available": "available",
    # 总市值
    "marketvalue": "frozen",
    # 浮动盈亏
    "fnl": "fpnl",
}


gmtAccountConvertor = vxDataConvertor(vxAccountInfo, _ACCOUNT_CONVERTORS)
