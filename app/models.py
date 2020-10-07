from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()

class URL(Base):

    __tablename__ = "urls"

    url_short = Column("url_short", String(3), primary_key = True)
    url_long = Column("url_long", String(2084))
    added = Column("added", DateTime())

    def __init__(self, url_short, url_long, added):

        self.url_short = url_short
        self.url_long = url_long
        self.added = added
