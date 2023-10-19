"""供应接口"""

import datetime
from abc import abstractmethod, ABC
from typing import Dict, List, Union, Any
from vxutils.sched.core import vxEvent, vxTrigger
from vxutils import vxtime, logger, diskcache, to_datetime
from vxquant.datamodels.utils import DateTimeType, InstrumentType
from vxquant.datamodels.core import (
    vxTick,
    # vxCalendar,
    vxAccountInfo,
    vxPosition,
    vxOrder,
    vxTrade,
)
from vxquant.datamodels.instruments import vxInstruments

from vxutils.sched.context import vxContext


class vxProviderBase(ABC):
    """供应接口基类"""

    def __init__(self, context: vxContext = None) -> None:
        self._context = context or vxContext()

    @property
    def context(self) -> vxContext:
        """上下文对象"""
        return self._context

    def set_context(self, context: vxContext, **kwargs):
        """设置上下文对象

        Arguments:
            context {vxContext} -- 上下文对象
        """
        self._context = context
        self._context.update(kwargs)

    def __call__(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class vxCalendarProvider(vxProviderBase):
    """交易日历接口"""

    def __call__(
        self,
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        market: str = "SHSE",
    ) -> List[datetime.datetime]:
        start_date = to_datetime(start_date or "2005-01-01")
        end_date = to_datetime(end_date or vxtime.today())

        trade_days = []
        this_year_begin = datetime.datetime.today().replace(
            month=1, day=1, hour=0, minute=0, second=0
        )

        for year in range(start_date.year, end_date.year + 1):
            key = f"calendar_{market}_{year}"
            if key not in diskcache:
                dates = self.get_trade_dates(
                    market, start_date=f"{year}-01-01", end_date=f"{year}-12-31"
                )
                if dates:
                    last_date = to_datetime(dates[-1])
                    expired_dt = last_date if last_date > this_year_begin else None
                    diskcache.set(expired_dt=expired_dt, **{key: dates})
                    trade_days.extend(dates)
                    logger.info(f"更新交易日历: {key}")
            else:
                trade_days.extend(diskcache[key])

        return sorted(
            filter(lambda x: start_date <= to_datetime(x) <= end_date, trade_days)
        )

    def get_trade_dates(
        self,
        market: str = "cn",
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
    ) -> List[datetime.datetime]:
        """获取该市场全部日历 --- 2010年1月1日以来的所有交易日历

        Arguments:
            market {str} -- 市场代码
            start_date {DateTimeType} -- 开始日期
            end_date {DateTimeType} -- 结束日期

        Returns:
            List[InstrumentType] -- 返回值: ['2022-01-01', '2022-01-02', ...]
        """
        raise NotImplementedError


class vxGetInstrumentProvider(vxProviderBase):
    def __call__(
        self,
        sec_type,
        exchange_id: str = None,
    ) -> vxInstruments:
        """获取证券信息接口"""
        raise NotImplementedError


class vxHQProvider(vxProviderBase):
    """行情接口基类"""

    _tickcache = diskcache

    def __call__(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时行情接口

        Returns:
            Dict[InstrumentType, vxTick] -- _description_
        """
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        ticks = self._tickcache.get_many(symbols)
        suspend_symbols = self._tickcache.get("__suspend_symbols__", [])
        _missing_symbols = list(set(symbols) - set(ticks.keys()) - set(suspend_symbols))

        if _missing_symbols:
            hq_ticks = self._hq(*_missing_symbols)
            if hq_ticks:
                now = vxtime.now()
                if now < vxtime.today("09:25:00"):
                    expired_dt = vxtime.today("09:25:01")
                elif now < vxtime.today("16:00:00"):
                    expired_dt = now + 3
                else:
                    expired_dt = vxtime.today("09:25:01") + 24 * 60 * 60

                self._tickcache.set(expired_dt=expired_dt, **hq_ticks)
                ticks.update(hq_ticks)
        return ticks

    @abstractmethod
    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时数据接口

        Returns:
            Dict[InstrumentType, vxTick] -- 返回值样例:
            {
                "SHSE.600000": vxTick(...),
                "SHSE.600001": vxTick(...),
                ...
            }
        """
        raise NotImplementedError("实时数据接口未实现")


class vxGetAccountProvider(vxProviderBase):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        """获取账户信息接口

        Keyword Arguments:
            account_id {str} -- 账号信息 (default: {None})

        Returns:
            vxAccountInfo -- 返回 vxaccountinfo对应的信息
        """
        raise NotImplementedError


class vxGetPositionsProvider(vxProviderBase):
    def __call__(
        self,
        symbol: InstrumentType = None,
        acccount_id: str = None,
    ) -> Dict[InstrumentType, vxPosition]:
        """获取持仓信息接口

        Keyword Arguments:
            symbol {InstrumentType} -- 持仓证券信息 (default: {None})
            acccount_id {str} -- 账号信息 (default: {None})

        Returns:
            Dict[InstrumentType, Union[vxPosition]] -- 返回{symbol: vxposition}的字典
        """
        raise NotImplementedError


class vxGetOrdersProvider(vxProviderBase):
    def __call__(
        self, account_id: str = None, filter_finished: bool = False
    ) -> Dict[str, vxOrder]:
        """获取委托订单接口

        Keyword Arguments:
            account_id {str} -- 账号 (default: {None})
            filter_finished {bool} -- 是否过滤已完成委托订单 (default: {True})


        Returns:
            Dict[str, vxOrder] -- 返回{order_id: vxorder}的字典
        """
        raise NotImplementedError


class vxGetExecutionReportsProvider(vxProviderBase):
    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        """获取成交信息接口

        Keyword Arguments:
            account_id {str} -- 账号 (default: {None})
            order_id {str} -- 委托订单号 (default: {None})
            trade_id {str} -- 成交编号 (default: {None})

        Returns:
            Dict[str, vxTrade] -- 返回{trade_id: vxtrade}的字典
        """
        raise NotImplementedError


class vxOrderBatchProvider(vxProviderBase):
    def __call__(self, *vxorders) -> List[vxOrder]:
        """批量委托下单接口

        Keyword Arguments:
            vxorders {vxOrder} -- 待提交的委托信息

        Returns:
            List[vxOrder] -- 返回提交成功的vxorders，并且将order.exchange_order_id字段予以赋值
        """
        raise NotImplementedError


class vxOrderCancelProvider(vxProviderBase):
    def __call__(self, *vxorders) -> None:
        """批量撤单接口

        Keyword Arguments:
            vxorders {vxOrder} -- 待取消的委托信息，取消委托中order.exchange_order_id字段若为空，则跳过
        """
        raise NotImplementedError


class vxPublisher(vxProviderBase):
    def __call__(
        self,
        event: Union[str, vxEvent],
        data: Any,
        trigger: vxTrigger,
        priority: int,
        **kwargs,
    ) -> None:
        """事件发布接口

        Arguments:
            event {str} -- 事件名称

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError


class vxSubscriber(vxProviderBase):
    def __call__(self, event_type: str, channel: str = "#") -> None:
        """事件订阅接口

        Arguments:
            event_type {str} -- 事件名称
            channel {str} -- 渠道名称

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError
