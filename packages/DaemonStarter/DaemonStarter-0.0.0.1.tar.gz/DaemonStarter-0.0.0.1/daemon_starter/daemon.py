# @Time : 2023-10-19 11:24
# @Author  : inflowers@126.com
# @Desc : ==============================================
# Life is Short I Use Python!!!                      ===
# ======================================================
# @Project : Daemon
# @FileName: Daemon
# @Software: PyCharm
import datetime
import logging.handlers
import logging.handlers
import os
import subprocess
import sys
import time
from pathlib import Path


def get_logger(file_name='app.log', format_str='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
               file_count=10, backup_count=5, open_file=True, open_stream=False, level=logging.INFO):
    formatter = logging.Formatter(format_str)
    formatter.datefmt = datefmt
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.level = logging.INFO

    path = Path(__file__).parent.joinpath(file_name)
    file_handler = logging.handlers.RotatingFileHandler(path, maxBytes=1024 * 1024 * file_count,
                                                        backupCount=backup_count,
                                                        encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.level = logging.INFO

    logger = logging.getLogger("myLogger")
    if open_file:
        logger.addHandler(file_handler)
    if open_stream:
        logger.addHandler(stream_handler)
    logger.setLevel(level)
    return logger


def sub_service_loop():
    args = [sys.executable] + ['-W%s' % o for o in sys.warnoptions] + sys.argv
    _win = (sys.platform == "win32")
    new_environ = os.environ.copy()
    new_environ["SUB_SERVICE"] = 'true'
    while True:
        exit_code = subprocess.call(args, env=new_environ)
        if exit_code == 0:
            return exit_code
        logging.info('任务异常,重启服务: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(1)


def starter(func, params):
    if 'SUB_SERVICE' in os.environ and os.environ["SUB_SERVICE"]:
        func(**params)
    else:
        sub_service_loop()
