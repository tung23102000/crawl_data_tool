from sqlalchemy import create_engine, Column, Integer, String, Date, Time, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import * 
import urllib.parse
Base = declarative_base()
user = DB_USER 
password = urllib.parse.quote_plus(DB_PASSWORD) 
host = urllib.parse.quote_plus(DB_HOST) 
port = DB_PORT 
database = DB_DATABASE 

DATABASE_URL = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine, autoflush=False)

class Contract(Base):
    __tablename__ = 'contracts' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False)
    notice = Column(Text, nullable=False)
    contract_name = Column(Text, nullable=False)
    inviter = Column(Text, nullable=True)
    investor = Column(Text, nullable=True)
    date_posted = Column(DateTime, nullable=True)
    field = Column(String(255), nullable=True)
    location = Column(Text, nullable=True)
    closing_time = Column(Time, nullable=True)
    closing_date = Column(Date, nullable=True)
    bidding_method = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Contract(code={self.code}, contract_name={self.contract_name})>"

Base.metadata.create_all(engine)

