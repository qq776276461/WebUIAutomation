import logging
import time
import logzero
from src.utils.PathUtil import path_join


def init_log(log_level='i', out_logfile=False):
    if log_level.casefold() == 'debug'.casefold() or log_level.casefold() == 'd'.casefold():
        __log_level = logging.DEBUG
    elif log_level.casefold() == "warn".casefold() \
            or log_level.casefold() == 'w'.casefold() \
            or log_level.casefold() == 'warning'.casefold():
        __log_level = logging.WARN
    elif log_level.casefold() == 'critical' or log_level.casefold() == 'c'.casefold():
        __log_level = logging.CRITICAL
    else:
        __log_level = logging.INFO
    __ch_formartter = \
        f'%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] :%(end_color)s %(message)s'
    __log_formatter = f'[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] : %(message)s'
    __date_format = '%Y-%m-%d %H:%M:%S'
    _log: logging.Logger = logzero.logger
    logzero.loglevel(__log_level)
    logzero.formatter(logzero.LogFormatter(fmt=__ch_formartter, datefmt=__date_format), update_custom_handlers=True)
    if out_logfile:

        __report_dir = f"{time.strftime('%Y-%m-%d %H_%M', time.localtime(int(time.time())))}"
        logzero.logfile(
            f"{path_join('output', __report_dir)}/script_log.log",
            loglevel=logging.DEBUG,
            formatter=logging.Formatter(__log_formatter, __date_format),
            encoding='utf8',
            maxBytes=1024 * 1024,
            backupCount=3
        )

    return _log


if __name__ == '__main__':
    log = init_log("d", out_logfile=True)

    log.debug("我是debug")
    log.info("我是info")
    log.warning("我是warn")
    log1 = init_log("w")
    log.error("我是error")
    log.exception("我是exception")
    log.critical("我是critical")

    log1.debug("我是debuaaaaaaag")
    log1.info("我是infoaaa")
    log1.warning("我是warnaaaa")
    log1.error("我是erroraaa")
    log1.exception("我是exceptionaaa")
    log1.critical("我是criticaaaal")
