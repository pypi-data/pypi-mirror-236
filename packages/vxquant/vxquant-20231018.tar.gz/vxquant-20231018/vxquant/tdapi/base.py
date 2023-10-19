"""交易接口"""


from vxutils.importutils import vxAPIWrappers


class vxTdAPI(vxAPIWrappers):
    __defaults__ = {
        "current": {
            "class": "vxquant.providers.spiders.vxTencentHQProvider",
            "params": {},
        },
        "order_volume": {},
        "get_positions": {},
        "get_orders": {},
        "get_trades": {},
        "get_accountinfo": {},
    }
