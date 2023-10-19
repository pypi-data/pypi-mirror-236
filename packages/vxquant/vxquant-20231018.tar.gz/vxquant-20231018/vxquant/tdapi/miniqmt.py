from .base import vxTdAPI
from vxutils import logger, vxtime
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from xtquant import xtconstant


class vxQMTTdAPI(vxTdAPI):
    __defaults__ = {}

    def set_context(
        self,
        context,
        userdata_mini_path="",
        account_id="",
    ):
        self._context = context
        userdata_mini_path = self._context.settings.get(
            "userdata_mini_path", userdata_mini_path
        )
        account_id = self._context.settings.get("account_id", account_id)
        self._context.trader = XtQuantTrader(userdata_mini_path, int(vxtime.now()))
        self._context.account = StockAccount(account_id)
        self._context.trader.start()
        status = self._context.trader.connect()
        if not status:
            raise ConnectionError("QMT连接失败")
        self._context.trader.subscribe(self._context.account)
