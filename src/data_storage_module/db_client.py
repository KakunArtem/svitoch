from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker

from src.configuration import config, logger


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DbClient(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = create_engine(self.create_connection())
        self.session = scoped_session(sessionmaker(self.engine))

    def create_connection(self):
        return URL.create(
            drivername="postgresql",
            username=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    def create_tables(self, base):
        logger.info('Creating required tables')
        base.metadata.create_all(self.engine)

    def get_session(self):
        return self.session

    def add_to_db(self, obj):
        try:
            self.session.add(obj)
            self.session.commit()
        except Exception as e:
            raise e

    def get_from_db(self, model, **filters):
        result = self.session.query(model).filter_by(**filters).all()
        return result