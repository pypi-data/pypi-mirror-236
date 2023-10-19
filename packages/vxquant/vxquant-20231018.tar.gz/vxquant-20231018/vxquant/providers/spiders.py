"""交易日期基础接口"""
import random
import datetime
import json
from enum import Enum
from itertools import product, chain
from typing import List, Union, Dict
from vxutils import vxtime, logger, to_datetime, to_enum
from vxutils.networking.httpget import vxHttpGet
from vxquant.datamodels.contants import Exchange
from vxquant.datamodels.core import vxTick
from vxquant.providers.base import (
    DateTimeType,
    vxCalendarProvider,
    vxHQProvider,
    InstrumentType,
)
from multiprocessing.managers import SyncManager

SyncManager("0.0.0.0")


SSE_CALENDAR_LIST = "http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{month}&random={timestamp}"
TENCENT_HQ_URL = "http://qt.gtimg.cn/q={symbol}&random={timestamp}"


TENCENT_COLUMNS = [
    "symbol",
    "name",  # 1: 股票名字
    "code",  # 2: 股票代码
    "lasttrade",  # 3: 当前价格
    "yclose",  # 4: 昨收
    "open",  # 5: 今开
    "volume",  # 6: 成交量（手）
    "outter_vol",  # 7: 外盘
    "intter_vol",  # 8: 内盘
    "bid1_p",  # 9: 买一
    "bid1_v",  # 10: 买一量（手）
    "bid2_p",  # 11: 买二
    "bid2_v",  # 12：买二量（手）
    "bid3_p",  # 13: 买三
    "bid3_v",
    "bid4_p",  # 14：买三量（手）  # 15: 买四
    "bid4_v",  # 16：买四量（手）
    "bid5_p",  # 17: 买五
    "bid5_v",  # 18：卖五量（手）
    "ask1_p",  # 19: 卖一
    "ask1_v",  # 20: 卖一量（手）
    "ask2_p",  # 21: 卖二
    "ask2_v",  # 22：卖二量（手）
    "ask3_p",  # 23: 卖三
    "ask3_v",  # 24：卖三量（手）
    "ask4_p",  # 25: 卖四
    "ask4_v",  # 26：卖四量（手）
    "ask5_p",  # 27: 卖五
    "ask5_v",  # 28：卖五量（手）
    "last_volume",  # 29: 最近逐笔成交
    "created_dt",  # 30: 时间
    "change",  # 31: 涨跌
    "pct_change",  # 32: 涨跌%
    "high",  # 33: 最高
    "low",  # 34: 最低
    "combine",  # 35: 价格/成交量（手）/成交额
    "volume_backup",  # 36: 成交量（手）
    "amount",  # 37: 成交额（万）
    "turnover",  # 38: 换手率
    "pe",  # 39: 市盈率
    "unknow",  # 40:
    "high2",  # 41: 最高
    "low2",  # 42: 最低
    "amplitude",  # 43: 振幅
    "negotiablemv",  # 44: 流通市值
    "totmktcap",  # 45: 总市值
    "pb",  # 46: 市净率
    "uplimit",  # 47: 涨停价
    "downlimit",  # 48: 跌停价
]

VOLUME_COLUMNS = [
    "volume",
    "bid1_v",
    "ask1_v",
    "bid2_v",
    "ask2_v",
    "bid3_v",
    "ask3_v",
    "bid4_v",
    "ask4_v",
    "bid5_v",
    "ask5_v",
]


class CNCalenderProvider(vxCalendarProvider):
    def get_trade_dates(
        self,
        market: Union[Enum, str] = Exchange.SHSE,
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
    ) -> List:
        market = to_enum(market, Exchange)
        if market != Exchange.SHSE:
            raise NotImplementedError(f"暂不支持 {market}类型")

        start_date = to_datetime(start_date) or datetime.datetime(2005, 1, 1)
        end_date = to_datetime(end_date) or datetime.datetime.now().replace(
            month=12, day=31, hour=0, minute=0, second=0
        )

        urls = [
            SSE_CALENDAR_LIST.format(
                year=year, month=month, timestamp=random.randint(100000, 10000000)
            )
            for year, month in product(
                range(start_date.year, end_date.year + 1), range(1, 13)
            )
        ]
        httpget = vxHttpGet(parser=self._parser, timeout=5, retry_times=5, workers=3)
        return sorted(set(chain(*httpget(*urls))))

    def _parser(self, resp):
        resp.raise_for_status()
        reply = json.loads(resp.text)
        if "data" in reply and reply["data"]:
            cals = [
                trade_date["jyrq"]
                for trade_date in reply["data"]
                if trade_date["jybz"] == "1"
            ]
            return map(to_datetime, cals)
        return []


class vxTencentHQProvider(vxHQProvider):
    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        urls = [
            self.build_tencent_hq_url(symbols, i, i + 80)
            for i in range(0, len(symbols), 80)
        ]

        httpget = vxHttpGet(parser=self._parser)
        return dict((tick.symbol, tick) for tick in chain(*httpget(*urls)))

    def build_tencent_hq_url(self, symbols, start=0, end=-1):
        return TENCENT_HQ_URL.format(
            symbol=",".join(
                [symbol.replace("SE.", "").lower() for symbol in symbols[start:end]]
            ),
            timestamp=int(vxtime.now() * 1000),
        )

    def _parser(self, response) -> Dict[InstrumentType, vxTick]:
        ticks = []
        for line in response.text.split(";\n"):
            try:
                data_line = line.split("~")
                if len(data_line) < len(TENCENT_COLUMNS):
                    continue
                tick = dict(zip(TENCENT_COLUMNS, data_line))
                tick["symbol"] = tick["symbol"].split("=")[0][2:]
                tick = vxTick(**tick)
                for col in VOLUME_COLUMNS:
                    tick[col] = float(tick[col]) * 100
                ticks.append(tick)
            except Exception:
                pass

        return ticks


if __name__ == "__main__":
    # print(diskcache.get("calendar_cn_2020"))
    # from vxutils.cache import diskcache

    #
    # diskcache.clear()
    cal = CNCalenderProvider()
    trade_days = cal("2005-01-01", "2023-12-31", market="SHSE")
    print(len(trade_days))
    for d in trade_days[:10]:
        print(d)

    symbols = [
        "SHSE.110043",
        "SHSE.110044",
        "SHSE.110045",
        "SHSE.110047",
        "SHSE.110048",
        "SHSE.110052",
        "SHSE.110053",
        "SHSE.110055",
        "SHSE.110057",
        "SHSE.110058",
        "SHSE.110059",
        "SHSE.110060",
        "SHSE.110061",
        "SHSE.110062",
        "SHSE.110063",
        "SHSE.110064",
        "SHSE.110067",
        "SHSE.110068",
        "SHSE.110070",
        "SHSE.110072",
        "SHSE.110073",
        "SHSE.110074",
        "SHSE.110075",
        "SHSE.110076",
        "SHSE.110077",
        "SHSE.110079",
        "SHSE.110080",
        "SHSE.110081",
        "SHSE.110082",
        "SHSE.110083",
        "SHSE.110084",
        "SHSE.110085",
        "SHSE.110086",
        "SHSE.110087",
        "SHSE.110088",
        "SHSE.110089",
        "SHSE.110090",
        "SHSE.110091",
        "SHSE.110092",
        "SHSE.111000",
        "SHSE.111001",
        "SHSE.111002",
        "SHSE.111003",
        "SHSE.111004",
        "SHSE.111005",
        "SHSE.111006",
        "SHSE.111007",
        "SHSE.111008",
        "SHSE.111009",
        "SHSE.111010",
        "SHSE.111011",
        "SHSE.111012",
        "SHSE.113011",
        "SHSE.113013",
        "SHSE.113016",
        "SHSE.113017",
        "SHSE.113021",
        "SHSE.113024",
        "SHSE.113025",
        "SHSE.113027",
        "SHSE.113030",
        "SHSE.113033",
        "SHSE.113037",
        "SHSE.113039",
        "SHSE.113042",
        "SHSE.113043",
        "SHSE.113044",
        "SHSE.113045",
        "SHSE.113046",
        "SHSE.113047",
        "SHSE.113048",
        "SHSE.113049",
        "SHSE.113050",
        "SHSE.113051",
        "SHSE.113052",
        "SHSE.113053",
        "SHSE.113054",
        "SHSE.113055",
        "SHSE.113056",
        "SHSE.113057",
        "SHSE.113058",
        "SHSE.113059",
        "SHSE.113060",
        "SHSE.113061",
        "SHSE.113062",
        "SHSE.113063",
        "SHSE.113064",
        "SHSE.113065",
        "SHSE.113504",
        "SHSE.113505",
        "SHSE.113516",
        "SHSE.113519",
        "SHSE.113524",
        "SHSE.113526",
        "SHSE.113527",
        "SHSE.113530",
        "SHSE.113532",
        "SHSE.113534",
        "SHSE.113535",
        "SHSE.113537",
        "SHSE.113542",
        "SHSE.113545",
        "SHSE.113546",
        "SHSE.113549",
        "SHSE.113561",
        "SHSE.113563",
        "SHSE.113565",
        "SHSE.113566",
        "SHSE.113567",
        "SHSE.113569",
        "SHSE.113570",
        "SHSE.113573",
        "SHSE.113574",
        "SHSE.113575",
        "SHSE.113576",
        "SHSE.113577",
        "SHSE.113578",
        "SHSE.113579",
        "SHSE.113582",
        "SHSE.113584",
        "SHSE.113585",
        "SHSE.113588",
        "SHSE.113589",
        "SHSE.113591",
        "SHSE.113593",
        "SHSE.113594",
        "SHSE.113595",
        "SHSE.113596",
        "SHSE.113597",
        "SHSE.113598",
        "SHSE.113600",
        "SHSE.113601",
        "SHSE.113602",
        "SHSE.113604",
        "SHSE.113605",
        "SHSE.113606",
        "SHSE.113608",
        "SHSE.113609",
        "SHSE.113610",
        "SHSE.113615",
        "SHSE.113616",
        "SHSE.113618",
        "SHSE.113619",
        "SHSE.113621",
        "SHSE.113622",
        "SHSE.113623",
        "SHSE.113624",
        "SHSE.113625",
        "SHSE.113626",
        "SHSE.113627",
        "SHSE.113628",
        "SHSE.113629",
        "SHSE.113631",
        "SHSE.113632",
        "SHSE.113633",
        "SHSE.113634",
        "SHSE.113636",
        "SHSE.113637",
        "SHSE.113638",
        "SHSE.113639",
        "SHSE.113640",
        "SHSE.113641",
        "SHSE.113643",
        "SHSE.113644",
        "SHSE.113646",
        "SHSE.113647",
        "SHSE.113648",
        "SHSE.113649",
        "SHSE.113650",
        "SHSE.113651",
        "SHSE.113652",
        "SHSE.113653",
        "SHSE.113654",
        "SHSE.113655",
        "SHSE.113656",
        "SHSE.113657",
        "SHSE.113658",
        "SHSE.113659",
        "SHSE.113660",
        "SHSE.113661",
        "SHSE.113662",
        "SHSE.113663",
        "SHSE.113664",
        "SHSE.113665",
        "SHSE.118000",
        "SHSE.118003",
        "SHSE.118004",
        "SHSE.118005",
        "SHSE.118006",
        "SHSE.118007",
        "SHSE.118008",
        "SHSE.118009",
        "SHSE.118010",
        "SHSE.118011",
        "SHSE.118012",
        "SHSE.118013",
        "SHSE.118014",
        "SHSE.118015",
        "SHSE.118016",
        "SHSE.118017",
        "SHSE.118018",
        "SHSE.118019",
        "SHSE.118020",
        "SHSE.118021",
        "SHSE.118022",
        "SHSE.118023",
        "SHSE.118024",
        "SHSE.118025",
        "SHSE.118026",
        "SHSE.118027",
        "SHSE.118028",
        "SHSE.118029",
        "SHSE.118030",
        "SZSE.123002",
        "SZSE.123004",
        "SZSE.123010",
        "SZSE.123011",
        "SZSE.123012",
        "SZSE.123013",
        "SZSE.123014",
        "SZSE.123015",
        "SZSE.123018",
        "SZSE.123022",
        "SZSE.123025",
        "SZSE.123031",
        "SZSE.123034",
        "SZSE.123035",
        "SZSE.123038",
        "SZSE.123039",
        "SZSE.123044",
        "SZSE.123046",
        "SZSE.123048",
        "SZSE.123049",
        "SZSE.123050",
        "SZSE.123052",
        "SZSE.123054",
        "SZSE.123056",
        "SZSE.123057",
        "SZSE.123059",
        "SZSE.123061",
        "SZSE.123063",
        "SZSE.123064",
        "SZSE.123065",
        "SZSE.123067",
        "SZSE.123071",
        "SZSE.123072",
        "SZSE.123075",
        "SZSE.123076",
        "SZSE.123077",
        "SZSE.123078",
        "SZSE.123080",
        "SZSE.123082",
        "SZSE.123083",
        "SZSE.123085",
        "SZSE.123087",
        "SZSE.123088",
        "SZSE.123089",
        "SZSE.123090",
        "SZSE.123091",
        "SZSE.123092",
        "SZSE.123093",
        "SZSE.123096",
        "SZSE.123098",
        "SZSE.123099",
        "SZSE.123100",
        "SZSE.123101",
        "SZSE.123103",
        "SZSE.123104",
        "SZSE.123105",
        "SZSE.123106",
        "SZSE.123107",
        "SZSE.123108",
        "SZSE.123109",
        "SZSE.123112",
        "SZSE.123113",
        "SZSE.123114",
        "SZSE.123115",
        "SZSE.123116",
        "SZSE.123117",
        "SZSE.123118",
        "SZSE.123119",
        "SZSE.123120",
        "SZSE.123121",
        "SZSE.123122",
        "SZSE.123124",
        "SZSE.123126",
        "SZSE.123127",
        "SZSE.123128",
        "SZSE.123129",
        "SZSE.123130",
        "SZSE.123131",
        "SZSE.123132",
        "SZSE.123133",
        "SZSE.123134",
        "SZSE.123135",
        "SZSE.123136",
        "SZSE.123138",
        "SZSE.123140",
        "SZSE.123141",
        "SZSE.123142",
        "SZSE.123143",
        "SZSE.123144",
        "SZSE.123145",
        "SZSE.123146",
        "SZSE.123147",
        "SZSE.123148",
        "SZSE.123149",
        "SZSE.123150",
        "SZSE.123151",
        "SZSE.123152",
        "SZSE.123153",
        "SZSE.123154",
        "SZSE.123155",
        "SZSE.123156",
        "SZSE.123157",
        "SZSE.123158",
        "SZSE.123159",
        "SZSE.123160",
        "SZSE.123161",
        "SZSE.123162",
        "SZSE.123163",
        "SZSE.123164",
        "SZSE.123165",
        "SZSE.123166",
        "SZSE.123167",
        "SZSE.123168",
        "SZSE.123169",
        "SZSE.123170",
        "SZSE.123171",
        "SZSE.123172",
        "SZSE.123173",
        "SZSE.127004",
        "SZSE.127005",
        "SZSE.127006",
        "SZSE.127007",
        "SZSE.127012",
        "SZSE.127014",
        "SZSE.127015",
        "SZSE.127016",
        "SZSE.127017",
        "SZSE.127018",
        "SZSE.127019",
        "SZSE.127020",
        "SZSE.127021",
        "SZSE.127022",
        "SZSE.127024",
        "SZSE.127025",
        "SZSE.127026",
        "SZSE.127027",
        "SZSE.127028",
        "SZSE.127029",
        "SZSE.127030",
        "SZSE.127031",
        "SZSE.127032",
        "SZSE.127033",
        "SZSE.127034",
        "SZSE.127035",
        "SZSE.127036",
        "SZSE.127037",
        "SZSE.127038",
        "SZSE.127039",
        "SZSE.127040",
        "SZSE.127041",
        "SZSE.127042",
        "SZSE.127043",
        "SZSE.127044",
        "SZSE.127045",
        "SZSE.127046",
        "SZSE.127047",
        "SZSE.127049",
        "SZSE.127050",
        "SZSE.127051",
        "SZSE.127052",
        "SZSE.127053",
        "SZSE.127054",
        "SZSE.127055",
        "SZSE.127056",
        "SZSE.127057",
        "SZSE.127058",
        "SZSE.127059",
        "SZSE.127060",
        "SZSE.127061",
        "SZSE.127062",
        "SZSE.127063",
        "SZSE.127064",
        "SZSE.127065",
        "SZSE.127066",
        "SZSE.127067",
        "SZSE.127068",
        "SZSE.127069",
        "SZSE.127070",
        "SZSE.127071",
        "SZSE.127072",
        "SZSE.127073",
        "SZSE.127074",
        "SZSE.127075",
        "SZSE.127076",
        "SZSE.127077",
        "SZSE.127078",
        "SZSE.127079",
        "SZSE.127080",
        "SZSE.128014",
        "SZSE.128017",
        "SZSE.128021",
        "SZSE.128023",
        "SZSE.128025",
        "SZSE.128026",
        "SZSE.128030",
        "SZSE.128033",
        "SZSE.128034",
        "SZSE.128035",
        "SZSE.128036",
        "SZSE.128037",
        "SZSE.128039",
        "SZSE.128040",
        "SZSE.128041",
        "SZSE.128042",
        "SZSE.128044",
        "SZSE.128048",
        "SZSE.128049",
        "SZSE.128053",
        "SZSE.128056",
        "SZSE.128062",
        "SZSE.128063",
        "SZSE.128066",
        "SZSE.128070",
        "SZSE.128071",
        "SZSE.128072",
        "SZSE.128074",
        "SZSE.128075",
        "SZSE.128076",
        "SZSE.128078",
        "SZSE.128079",
        "SZSE.128081",
        "SZSE.128082",
        "SZSE.128083",
        "SZSE.128085",
        "SZSE.128087",
        "SZSE.128090",
        "SZSE.128091",
        "SZSE.128095",
        "SZSE.128097",
        "SZSE.128100",
        "SZSE.128101",
        "SZSE.128105",
        "SZSE.128106",
        "SZSE.128108",
        "SZSE.128109",
        "SZSE.128111",
        "SZSE.128114",
        "SZSE.128116",
        "SZSE.128117",
        "SZSE.128118",
        "SZSE.128119",
        "SZSE.128120",
        "SZSE.128121",
        "SZSE.128122",
        "SZSE.128123",
        "SZSE.128124",
        "SZSE.128125",
        "SZSE.128127",
        "SZSE.128128",
        "SZSE.128129",
        "SZSE.128130",
        "SZSE.128131",
        "SZSE.128132",
        "SZSE.128133",
        "SZSE.128134",
        "SZSE.128135",
        "SZSE.128136",
        "SZSE.128137",
        "SZSE.128138",
        "SZSE.128140",
        "SZSE.128141",
        "SZSE.128142",
        "SZSE.128143",
        "SZSE.128144",
        "SZSE.128145",
    ]
    symbols = [
        "SHSE.600000",
        "SHSE.600016",
        "SHSE.600004",
        "SHSE.600005",
        "SHSE.000001",
        "SZSE.399001",
        "SZSE.002850",
    ]

    hq = vxTencentHQProvider()
    with vxtime.timeit():
        ticks = hq._hq(*symbols)
    # print(ticks)
    print(len(ticks))
    print(ticks["SZSE.002850"])
