import logging

logger = logging.getLogger('newtown-mixcloud')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

hdlr = logging.FileHandler('./debug.log')
hdlr.setFormatter(formatter)

logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
