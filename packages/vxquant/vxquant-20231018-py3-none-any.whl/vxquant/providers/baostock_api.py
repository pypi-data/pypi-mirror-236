"""baostock provider"""

import baostock as bs
import datetime
from typing import List, Union
from vxutils import logger, to_datetime
from vxutils.sched.context import vxContext
from vxquant.providers.base import vxCalendarProvider

DateTimeType = Union[str, datetime.datetime, float, int]
InstrumentType = Union[str, int]


class vxBaostockCalendarProvider(vxCalendarProvider):
    def set_context(self, context: vxContext, **kwargs):
        lg = bs.login()
        if str(lg.error_code) != "0":
            raise ConnectionError(f"[{lg.error_code}]: login failed! {lg.error_msg}")

        return super().set_context(context, **kwargs)

    def get_trade_dates(
        self,
        market: str = "cn",
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
    ) -> List[datetime.datetime]:
        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        if str(rs.error_code) != "0":
            raise ConnectionError(
                f"[{rs.error_code}]: query_trade_dates failed! {rs.error_msg}"
            )

        data_list = []
        while (rs.error_code == "0") & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())

        return [to_datetime(d[0]) for d in data_list if d[1] != "0"]


if __name__ == "__main__":
    # cal = vxBaostockCalendarProvider(vxContext())
    # cal.set_context(vxContext())
    # trade_days = cal("1990-01-01", "2024-01-02")
    # print(trade_days[0], trade_days[-1])
    bs.login()
    rs = bs.query_stock_basic()
    data_list = []
    while (rs.error_code == "0") & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    print(rs.fields)
