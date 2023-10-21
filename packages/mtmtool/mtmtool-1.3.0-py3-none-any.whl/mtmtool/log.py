import logging


# 默认的日志格式
datefmt_classic = "%Y-%m-%d %H:%M:%S %z"
fmt_classic = '%(asctime)s %(levelname)s %(name)s: %(message)s'

def add_handler(logger:str|logging.Logger, handler:logging.Handler, clear:bool=False):
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    if not isinstance(logger, logging.Logger):
        raise TypeError("logger must be a str or logging.Logger object")
    if clear:
        logger.handlers.clear()
    formatter = logging.Formatter(fmt=fmt_classic, datefmt=datefmt_classic)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def stream_logger(name="Logger", log_level="INFO", clear=True, stream=None):
    handler = logging.StreamHandler(stream=stream)
    logger = add_handler(name, handler, clear=clear)
    logger.setLevel(log_level)
    return logger


def file_logger(name, filename, log_level="INFO", clear=False):
    handler = logging.FileHandler(filename, mode='a', encoding=None, delay=False)
    logger = add_handler(name, handler, clear=clear)
    logger.setLevel(log_level)
    return logger