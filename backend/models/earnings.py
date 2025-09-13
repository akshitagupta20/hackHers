from sqlalchemy import Column, Integer, String, DateTime, Date
from db import Base

class Earnings(Base):
    __tablename__ = "earnings"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer)
    date = Column(DateTime)
    amount = Column(Integer)
    expenses = Column(Integer)
    penalty_code = Column(String)
