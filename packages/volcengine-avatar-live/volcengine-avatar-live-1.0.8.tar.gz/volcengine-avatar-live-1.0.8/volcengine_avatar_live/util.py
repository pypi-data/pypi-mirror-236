# coding=utf-8

import datetime
import random
import logging


def create_logger(name: str, level: int) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(name)s: %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def generate_log_id() -> str:
    log_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    seed = "0123456789ABCDEF"
    for i in range(20):
        log_id += random.choice(seed)
    return log_id
