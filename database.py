from sqlalchemy import *
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, ForeignKey, exc
from sqlalchemy.orm import relationship


class BaseDB:

    def __init__(self):
        self.engine = create_engine('sqlite:///data.db', echo=True)
        self.metadata = MetaData(bind=None)
        self.table = Table('datos', self.metadata,
                           Column('id', Integer, primary_key=True),
                           Column('dato1', Integer, nullable=False),
                           )

        self.metadata.create_all(self.engine)

    def getdata(self):
        query = select([self.table])
        connection = self.engine.connect()
        result = connection.execute(query).fetchall()
        connection.close()
        midata = []
        for item in result:
            midata.append(dict(item.items()))
        return midata

    def erasedata(self):
        connection = self.engine.connect()
        try:
            connection.execute(self.table.delete())
        except Exception:
            connection.close()
            return False
        connection.close()
        return True
