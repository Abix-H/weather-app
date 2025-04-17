from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

class WeatherHistory(Base):
    __tablename__ = 'weather_history'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    date = Column(Date)
    time = Column(Time)  # ⬅️ New field
    temperature = Column(Float)
    humidity = Column(Integer)
    description = Column(String)

engine = create_engine('sqlite:///history.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
