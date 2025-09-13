from sqlalchemy import Column, Integer, String
from db import Base

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    language = Column(String)  # "en", "hi", "kn"
    phone = Column(String, unique=True)