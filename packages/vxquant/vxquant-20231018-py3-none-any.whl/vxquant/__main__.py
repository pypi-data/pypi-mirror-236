"""运行脚本"""
import sys
import signal
import subprocess
import argparse
from pathlib import Path
from vxutils import logger, vxtime

__START_TRADE_TIME__ = "09:10:00"
__END_TRADE_TIME__ = "16:00:00"


def main():
    """运行脚本"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--script", help="启动组件", default="app.py")
    parser.add_argument(
        "-c",
        "--config",
        help="config json file path: etc/config.json",
        default="etc/config.json",
        type=str,
    )
    parser.add_argument(
        "-m",
        "--mod",
        help="module directory path : mod/ ",
        default="mod/",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", help="debug 模式", action="store_true", default=False
    )
    parser.add_argument(
        "-i", "--init", help="初始化文件目录树", action="store_true", default=False
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel("DEBUG")

    if not Path(args.script).is_file():
        raise FileNotFoundError(f"脚本文件不存在: {args.script}")

    process = None
    while True:
        if vxtime.now() < vxtime.today(
            __START_TRADE_TIME__
        ) or vxtime.now() > vxtime.today(__END_TRADE_TIME__):
            if process is not None:
                process.send_signal(signal.SIGINT)
                logger.info("终止进程: %s", process.pid)
                vxtime.sleep(1)
                process = None
            sleep_time = vxtime.today(__START_TRADE_TIME__) - vxtime.now()

            if sleep_time < 0:
                sleep_time += 24 * 60 * 60

            logger.info(f"未到开盘时间点，休眠{sleep_time:,.2f}秒至开盘20分钟")
            vxtime.sleep(sleep_time)

        if process is None:
            process = subprocess.Popen(
                [sys.executable, args.script, "-c", args.config, "-m", args.mod]
            )
        vxtime.sleep(1)


if __name__ == "__main__":
    main()
