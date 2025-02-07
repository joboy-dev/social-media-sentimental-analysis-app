import logging


logging.basicConfig(filename='logs/sqlalchemy.log')
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
