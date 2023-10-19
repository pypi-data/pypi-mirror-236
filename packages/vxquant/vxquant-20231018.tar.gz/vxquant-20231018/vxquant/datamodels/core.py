"""数据模型"""

import datetime
from enum import Enum
from vxutils.database.dataclass import vxDataClass
from vxutils.database.fields import (
    vxFloatField,
    vxIntField,
    vxEnumField,
    vxStringField,
    vxDatetimeField,
    vxUUIDField,
    vxPropertyField,
    vxBoolField,
)
from vxutils import vxtime
from vxquant.datamodels.utils import to_symbol
from vxquant.datamodels.preset import vxMarketPreset
from vxquant.datamodels.contants import (
    SecStatus,
    SecType,
    Exchange,
    OrderDirection,
    OrderOffset,
    OrderType,
    OrderStatus,
    OrderRejectReason,
    PositionSide,
    TradeStatus,
)


class vxCalendar(vxDataClass):
    """交易日历模型"""

    trade_date: datetime.datetime = vxDatetimeField("交易日期", fmt_string="%Y-%m-%d")
    exchange_id: Enum = vxEnumField("交易所", default=Exchange.SHSE)
    is_open: bool = vxEnumField("是否开市", default=True)


class vxTick(vxDataClass):
    """行情模型"""

    # 证券标的
    symbol: str = vxStringField("证券标的", default="SHSE.999999", normalizer=to_symbol)
    # 开盘价
    open: float = vxFloatField("开盘价", 0, 4)
    # 最高价
    high: float = vxFloatField("最高价", 0, 4)
    # 最低价
    low: float = vxFloatField("最低价", 0, 4)
    # 最近成交价
    lasttrade: float = vxFloatField("最近成交价", 0, 4)
    # 成交价
    yclose: float = vxFloatField("昨日收盘价", 0, 4)
    # 成交价
    volume: int = vxIntField("成交量", 0, lower_bound=0)
    # 成交金额
    amount: float = vxFloatField("成交金额", 0, 4)
    # 卖1量
    bid1_v: int = vxIntField("卖1量", 0, lower_bound=0)
    # 卖1价
    bid1_p: float = vxFloatField("卖1价", 0, 4)
    # 卖2量
    bid2_v: int = vxIntField("卖2量", 0, lower_bound=0)
    # 卖2价
    bid2_p: float = vxFloatField("卖2价", 0, 4)
    # 卖3量
    bid3_v: int = vxIntField("卖3量", 0, lower_bound=0)
    # 卖3价
    bid3_p: float = vxFloatField("卖3价", 0, 4)
    # 卖4量
    bid4_v: int = vxIntField("卖4量", 0, lower_bound=0)
    # 卖4价
    bid4_p: float = vxFloatField("卖4价", 0, 4)
    # 卖5量
    bid5_v: int = vxIntField("卖5量", 0, lower_bound=0)
    # 卖5价
    bid5_p: float = vxFloatField("卖5价", 0, 4)
    # 买1量
    ask1_v: int = vxIntField("买1量", 0, lower_bound=0)
    # 买1价
    ask1_p: float = vxFloatField("买1价", 0, 4)
    # 买2量
    ask2_v: int = vxIntField("买2量", 0, lower_bound=0)
    # 买2价
    ask2_p: float = vxFloatField("买2价", 0, 4)
    # 买3量
    ask3_v: int = vxIntField("买3量", 0, lower_bound=0)
    # 买3价
    ask3_p: float = vxFloatField("买3价", 0, 4)
    # 买4量
    ask4_v: int = vxIntField("买4量", 0, lower_bound=0)
    # 买4价
    ask4_p: float = vxFloatField("买4价", 0, 4)
    # 买5量
    ask5_v: int = vxIntField("买5量", 0, lower_bound=0)
    # 买5价
    ask5_p: float = vxFloatField("买5价", 0, 4)
    # 换手率
    turnover: float = vxFloatField("换手率", 0, 2, lower_bound=0)
    # 振幅
    amplitude: float = vxFloatField("振幅", 0, 2, lower_bound=0)
    # 涨停价
    uplimit: float = vxFloatField("涨停价", 0, 4, lower_bound=0)
    # 跌停价
    downlimit: float = vxFloatField("跌停价", 0, 4, lower_bound=0)
    # 持仓量
    interest: int = vxIntField("持仓量", 0, lower_bound=0)
    # 交易状态
    status: SecStatus = vxEnumField("交易状态", default=SecStatus.NORMAL)


ONEDAY = 60 * 60 * 24


def _filled_vwap(vxorder: "vxOrder") -> float:
    """成交均价"""
    return (
        round(vxorder.filled_amount / vxorder.filled_volume, 4)
        if vxorder.filled_volume > 0
        else 0.0
    )


class vxTrade(vxDataClass):
    """成交回报"""

    # 账户id
    account_id: str = vxUUIDField("账户id", "AC", False)
    # 委托id
    order_id: str = vxUUIDField("委托id", "OD", False)
    # 交易所委托id
    exchange_order_id: str = vxUUIDField("交易所委托id", "EXOD", False)
    # 成交id
    trade_id: str = vxUUIDField("成交id", "TD", True)
    # 证券代码
    symbol: str = vxStringField("证券代码", "", normalizer=to_symbol)
    # 买卖方向
    order_direction: OrderDirection = vxEnumField("买卖方向", OrderDirection.Unknown)
    # 开平仓标志
    order_offset: OrderOffset = vxEnumField("开平仓标志", OrderOffset.Unknown)
    # 成交价格
    price: float = vxFloatField("成交价格", 0, ndigits=4, lower_bound=0.0)
    # 成交数量
    volume: int = vxIntField("成交数量", 0, lower_bound=0)
    # 交易佣金
    commission: float = vxFloatField("交易佣金", 0, ndigits=2, lower_bound=0.0)
    # 成交状态
    status: TradeStatus = vxEnumField("成交状态", TradeStatus.Unknown)
    # 拒绝代码
    reject_code: OrderRejectReason = vxEnumField("拒绝代码", OrderRejectReason.Unknown)
    # 拒绝原因
    reject_reason: str = vxStringField("拒绝原因", "", normalizer=str)


class vxOrder(vxDataClass):
    """委托订单"""

    # 账号id
    account_id: str = vxUUIDField("账户id", "AC", False)
    # 算法委托id
    algo_order_id: str = vxUUIDField("算法委托id", "ALGO", False)
    # 交易所委托id
    exchange_order_id: str = vxUUIDField("交易所委托id", "EXOD", False)
    # 委托id
    order_id: str = vxUUIDField("委托id", "OD", True)
    # 证券代码
    symbol: str = vxStringField("证券代码", "", normalizer=to_symbol)
    # 买卖方向
    order_direction: OrderDirection = vxEnumField("买卖方向", OrderDirection.Unknown)
    # 开平仓标志
    order_offset: OrderOffset = vxEnumField("开平仓标志", OrderOffset.Unknown)
    # 订单类型
    order_type: OrderType = vxEnumField("订单类型", OrderType.Unknown)
    # 委托数量
    volume: int = vxIntField("委托数量", 0, lower_bound=0)
    # 委托价格
    price: float = vxFloatField("委托价格", 0.0, 4, lower_bound=0)
    # 成交数量
    filled_volume: int = vxIntField("成交数量", 0, lower_bound=0)
    # 成交均价
    filled_vwap: float = vxPropertyField("成交均价", _filled_vwap, 0.0, formatter=str)
    # 成交总额（含手续费）
    filled_amount: float = vxFloatField("成交总额（含手续费）", 0.0, 2)
    # 订单状态
    status: OrderStatus = vxEnumField("订单状态", OrderStatus.PendingNew)
    # 订单超时时间
    due_dt: float = vxDatetimeField(
        "订单超时时间", default_factory=lambda: vxtime.today("15:00:00")
    )
    # 拒绝代码
    reject_code: OrderRejectReason = vxEnumField("拒绝代码", OrderRejectReason.Unknown)
    # 拒绝原因
    reject_reason: str = vxStringField("拒绝原因", "", normalizer=str)


def _available_volume(obj):
    """可用仓位计算规则"""
    return max(
        (obj.volume - obj.frozen) if obj.allow_t0 else obj.volume_his - obj.frozen, 0
    )


class vxPosition(vxDataClass):
    """股票持仓"""

    # 账户id
    account_id: str = vxUUIDField("账户ID", "AC", False)
    # 仓位id
    position_id: str = vxUUIDField("仓位ID", "PO", True)
    # 证券类型
    security_type: SecType = vxPropertyField(
        "证券类型", lambda obj: vxMarketPreset(obj.symbol).security_type
    )
    # 证券代码
    symbol: str = vxStringField("证券代码", "", normalizer=to_symbol)
    # 持仓方向
    position_side: PositionSide = vxEnumField("持仓方向", PositionSide.Long)
    # 今日持仓数量
    volume_today: float = vxFloatField("今日持仓数量", 0.0, 2, lower_bound=0)
    # 昨日持仓数量
    volume_his: float = vxFloatField("昨日持仓数量", 0.0, 2, lower_bound=0)
    # 持仓数量 --- 自动计算字段，由 volume_today + volume_his 计算所得
    volume: float = vxPropertyField(
        "持仓数量",
        lambda obj: obj.volume_his + obj.volume_today,
        formatter=lambda x: f"{x:,.2f}",
    )
    # 冻结数量
    frozen: float = vxFloatField("冻结数量", 0.0, 2, lower_bound=0)
    # 可用数量  --- 自动计算字段，由 volume - frozen计算
    available: int = vxPropertyField(
        "可用数量", _available_volume, formatter=lambda x: f"{x:,.2f}"
    )
    # 持仓市值
    marketvalue: float = vxPropertyField(
        "持仓市值",
        lambda obj: round(obj.volume * obj.lasttrade, 2),
        formatter=lambda x: f"{x:,.2f}",
    )
    # 持仓成本
    cost: float = vxFloatField("持仓成本", 0, 2)
    # 浮动盈利
    fnl: float = vxPropertyField(
        "浮动盈利",
        lambda obj: round(obj.marketvalue - obj.cost, 4),
        formatter=lambda x: f"{x:,.2f}",
    )
    # 持仓成本均价
    vwap: float = vxPropertyField(
        "持仓成本均价",
        lambda obj: round(obj.cost / obj.volume, 4) if obj.volume > 0 else 0.0,
        formatter=lambda x: f"{x:,.4f}",
    )
    # 最近成交价
    lasttrade: float = vxFloatField("最近成交价", 1.0, 4)
    # 是否T0
    allow_t0: bool = vxPropertyField(
        "是否T0", lambda obj: vxMarketPreset(obj.symbol).allow_t0
    )


class vxAccountInfo(vxDataClass):
    """账户信息类型"""

    # 账户id
    account_id: str = vxUUIDField("账户ID", "AC", False)
    # 账户币种
    currency: str = vxStringField("账户币种", "CNY")
    # 今日转入金额
    deposit: float = vxFloatField("今日转入金额", 0, 2, lower_bound=0)
    # 今日转出金额
    withdraw: float = vxFloatField("今日转出金额", 0, 2, lower_bound=0)
    # 净资产
    nav: float = vxPropertyField(
        "净资产", lambda obj: round(obj.balance + obj.marketvalue, 2)
    )
    # 资金余额
    balance: float = vxFloatField("资金余额", 0, 2)
    # 冻结金额
    frozen: float = vxFloatField("冻结金额", 0, 2)
    # 可用金额
    available: float = vxPropertyField(
        "可用金额",
        lambda obj: max(obj.balance - obj.frozen, 0),
        0,
        formatter=lambda x: f"{x:,.2f}",
    )
    # 总市值
    marketvalue: float = vxFloatField("总市值", 0, 2)
    # 今日盈利
    today_profit: float = vxPropertyField(
        "今日盈利", lambda obj: obj.nav - obj.nav_yd + obj.deposit - obj.withdraw
    )
    # 浮动盈亏
    fnl: float = vxFloatField("浮动盈亏", 0, 2)
    # 昨日净资产
    nav_yd: float = vxFloatField("昨日净资产", 0, 2)
    # 上一结算日
    settle_day: float = vxDatetimeField(
        "上一结算日",
        default_factory=lambda: vxtime.today("23:59:59") - ONEDAY,
        fmt_string="%F",
    )


if __name__ == "__main__":
    # tick = vxTick(symbol="sh.600000", open=3.14)
    # print(tick)
    vxorder = vxAccountInfo(
        symbol="sh.513500",
        lasttrade=11.6,
        volume_today=100,
        volume_his=1000,
        frozen=50,
        cost=22000,
    )
    logger.info(vxorder)
