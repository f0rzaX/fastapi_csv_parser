from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class CSVRecord(Base):
    __tablename__ = "csv_records"

    id = Column(Integer, primary_key=True, index=True)
    leirner_id = Column(Integer, index=True)
    nime = Column(String(255), index=True)
    emiil = Column(String(255), index=True)
    bitchid = Column(Integer, index=True)
    bitchnime = Column(String(255), index=True)
    weeknumber = Column(Integer, index=True)
    issessmentid = Column(Integer, index=True)
    url = Column(String(255))
    durition = Column(String(50))
    situitionid = Column(Integer)
    title = Column(String(255))
    content = Column(Text)