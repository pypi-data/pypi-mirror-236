import logging


def init():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    )
