"""配置文件"""
import json
from pathlib import Path
from typing import Union
from vxquant.mdapi.base import vxMdAPI
from vxutils.collections import vxDict
from vxutils.importutils import import_by_config
from vxutils.sched.context import vxContext
from vxutils import logger, vxtime


__default_settings__ = {
    "mdapi": {"class": "vxquant.mdapi.vxMdAPI", "params": {}},
    "tdapis": {},
    "objs": {},
    "preset_events": {
        "before_trade": "09:15:00",
        "on_trade": "09:30:00",
        "noon_break_start": "11:30:00",
        "noon_break_end": "13:00:00",
        "before_close": "14:45:00",
        "on_close": "14:55:00",
        "after_close": "15:30:00",
        "on_settle": "16:30:00",
    },
}


class QuantContext(vxContext):
    """Quant上下文"""

    def initialize(self):
        """初始化"""

        for attr, method in self.settings.items():
            if attr == "mdapi":
                self._init_mdapi(method)
            elif attr == "tdapis":
                self._init_tdapis(method)
            elif isinstance(method, dict) and "class" in method:
                setattr(self, attr, import_by_config(method))
                logger.info(f"初始化配置项: {attr}={method}")

    def _init_mdapi(self, mdapi_config: dict = None):
        if mdapi_config:
            self.mdapi = import_by_config(mdapi_config)
            trade_dates = self.mdapi.calendar("2005-01-01")
            vxtime.add_businessdays(trade_dates)
            logger.info("添加交易日历: %s个", len(trade_dates))
            ticks = self.mdapi.current("SHSE.000300")
            logger.info("行情接口测试成功，沪深300指数最新指数: %.2f", ticks["SHSE.000300"].lasttrade)
        else:
            self.mdapi = vxMdAPI()
            logger.warning("未配置行情接口")

    def _init_tdapis(self, tdapis_config: dict = None):
        if tdapis_config:
            self.tdapis = vxDict()
            for name, config in tdapis_config.items():
                tdapi = import_by_config(config)

                tdapi.set_context(context=self)
                self.tdapis[name] = tdapi
                logger.info("交易接口测试成功，接口(%s): %s", name, tdapi.__class__.__name__)
        else:
            self.tdapis = None
            logger.warning("未配置交易接口")


if __name__ == "__main__":
    context = QuantContext.load_json("log/config.json")
    context.params.t1 = 300
    print(vxtime.is_holiday("2023-9-10"))
    print(vxtime.is_holiday("2023-9-11"))
    print(context.mdapi.current("SHSE.000300"))
    print(context.params.lasttrade)
    context.save_json("log/config.json")
    print(context.tdapis.gmtdapi.get_positions())
