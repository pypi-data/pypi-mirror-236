"""行情接口"""


from vxutils.importutils import vxAPIWrappers


class vxMdAPI(vxAPIWrappers):
    __defaults__ = {
        "calendar": {
            "class": "vxquant.providers.spiders.CNCalenderProvider",
            "params": {},
        },
        "current": {
            "class": "vxquant.providers.spiders.vxTencentHQProvider",
            "params": {},
        },
    }


if __name__ == "__main__":
    mdapi = vxMdAPI()
    print(mdapi.current("SHSE.600000"))
