"""gmtrade接口"""

from typing import Dict, List
from gmtrade import api as gmsimapi
from collections.abc import Sequence
from vxutils.sched.context import vxContext
from vxutils import logger
from vxquant.datamodels.contants import SecType, OrderType, OrderDirection, OrderOffset
from vxquant.datamodels.core import vxAccountInfo, vxOrder, vxPosition, vxTrade
from vxquant.datamodels.preset import vxMarketPreset
from vxquant.providers.base import (
    InstrumentType,
    vxGetAccountProvider,
    vxGetExecutionReportsProvider,
    vxGetPositionsProvider,
    vxOrderBatchProvider,
    vxOrderCancelProvider,
    vxGetOrdersProvider,
)
from vxquant.datamodels.tools.gmtrade import (
    gmtTradeConvertor,
    gmtOrderConvertor,
    gmtPositionConvertor,
    gmtAccountConvertor,
)
from vxquant.tdapi.base import vxTdAPI

_default_context = {
    "settings": {
        "endpoint": "api.myquant.cn:9000",
        "gmtoken": "your token",
        "account_id": "your account id",
        "account_alias": "your account alias",
    }
}


class vxGMGetAccountProvider(vxGetAccountProvider):
    def __call__(self, account_id: str = None) -> vxAccountInfo:
        gmt_cash = gmsimapi.get_cash(self.context.account)
        return gmtAccountConvertor(gmt_cash)


class vxGMGetPositionsProvider(vxGetPositionsProvider):
    def __call__(
        self, symbol: InstrumentType = None, acccount_id: str = None
    ) -> Dict[InstrumentType, vxPosition]:
        gmt_positions = gmsimapi.get_positions(self.context.account)
        positions = dict(
            map(lambda p: gmtPositionConvertor(p, key="symbol"), gmt_positions)
        )
        return positions if symbol is None else positions.get(symbol)


class vxGMGetOrdersProvider(vxGetOrdersProvider):
    def __call__(
        self, account_id: str = None, filter_finished: bool = False
    ) -> Dict[str, vxOrder]:
        if filter_finished:
            gmt_orders = gmsimapi.get_unfinished_orders(self.context.account)
        else:
            gmt_orders = gmsimapi.get_orders(self.context.account)

        orders = dict(map(lambda o: gmtOrderConvertor(o, key="order_id"), gmt_orders))
        return orders


class vxGMGetExecutionReportsProvider(vxGetExecutionReportsProvider):
    def __call__(
        self, account_id: str = None, order_id: str = None, trade_id: str = None
    ) -> Dict[str, vxTrade]:
        gmt_trades = gmsimapi.get_execution_reports(self.context.account)
        trades = dict(map(lambda t: gmtTradeConvertor(t, key="trade_id"), gmt_trades))
        if order_id:
            for trade in trades.values():
                if trade.order_id != order_id:
                    return trade
        elif trade_id:
            return trades.get(trade_id)

        return trades


class vxGMOrderBatchProvider(vxOrderBatchProvider):
    def __call__(self, *vxorders) -> List[vxOrder]:
        if (
            len(vxorders) == 1
            and isinstance(vxorders[0], Sequence)
            and not isinstance(vxorders[0], str)
        ):
            vxorders = vxorders[0]

        gmt_orders = [
            {
                "symbol": vxorder.symbol,
                "volume": vxorder.volume,
                "price": vxorder.price,
                "side": vxorder.order_direction.value,
                "position_effect": vxorder.order_offset.value,
                "order_type": vxorder.order_type.value,
            }
            for vxorder in vxorders
        ]
        ret_orders = gmsimapi.order_batch(gmt_orders, self.context.account)
        return list(map(gmtOrderConvertor, ret_orders))


class vxGMTdAPI(vxTdAPI):
    __defaults__ = {
        "current": {
            "class": "vxquant.providers.spiders.vxTencentHQProvider",
            "params": {},
        },
        "get_account": {
            "class": "vxquant.tdapi.gmtrade.vxGMGetAccountProvider",
            "params": {},
        },
        "get_positions": {
            "class": "vxquant.tdapi.gmtrade.vxGMGetPositionsProvider",
            "params": {},
        },
        "get_orders": {
            "class": "vxquant.tdapi.gmtrade.vxGMGetOrdersProvider",
            "params": {},
        },
        "get_trades": {
            "class": "vxquant.tdapi.gmtrade.vxGMGetExecutionReportsProvider",
            "params": {},
        },
        "order_batch": {
            "class": "vxquant.tdapi.gmtrade.vxGMOrderBatchProvider",
            "params": {},
        },
    }

    def order_volume(
        self,
        symbol: InstrumentType,
        volume: int,
        price: float = None,
        account_id: str = None,
    ) -> int:
        """计算订单数量"""
        if (
            vxMarketPreset(symbol).security_type == SecType.BOND_CONVERTIBLE
            and price is None
        ):
            tick = self.hq(symbol)
            price = tick[symbol].lasttrade

        order = vxOrder(
            account_id=account_id,
            symbol=symbol,
            volume=abs(volume),
            order_type=OrderType.Limit if price else OrderType.Market,
            order_direction=OrderDirection.Buy if volume > 0 else OrderDirection.Sell,
            order_offset=OrderOffset.Open if volume > 0 else OrderOffset.Close,
            price=price,
        )

        return self.order_batch(order)[0]

    def set_context(
        self,
        context=None,
        endpoint: str = "api.myquant.cn:9000",
        gmtoken: str = "",
        account_id: str = "",
        account_alias: str = "",
    ):
        """设置上下文对象"""
        if context is None:
            context = vxContext()

        endpoint = context.settings.get("endpoint", "api.myquant.cn:9000")
        gmsimapi.set_endpoint(endpoint)

        token = context.settings.get("gmtoken", gmtoken)
        gmsimapi.set_token(token)

        account_id = context.settings.get("account_id", account_id)
        account_alias = context.settings.get("account_alias", account_alias)
        context.account = gmsimapi.account(account_id, account_alias)
        gmsimapi.login(context.account)
        logger.info("登录账户: %s(%s)", account_alias, account_id)

        for method, provider in self.__dict__.items():
            if hasattr(provider, "set_context"):
                provider.set_context(context)
                logger.info("方法 %s 设置上下文: %s", method, provider.__class__.__name__)


if __name__ == "__main__":
    tdapi = vxGMTdAPI()
    context = vxContext(_default_context)
    context.settings.gmtoken = "e887dea1271dc25c2b140bdf0283b63f162f9511"
    context.settings.account_id = "689779a7-8f9a-11ec-b0bf-00163e0a4100"
    context.settings.account_alias = "sim"
    tdapi.set_context(context)
    positions = tdapi.get_positions()
    for symbol, position in positions.items():
        logger.info("%s 持仓: %.2f", symbol, position.fnl)

    # tdapi.order_volume("SHSE.600000", 100)
    orders = tdapi.get_account()
    print(orders)
