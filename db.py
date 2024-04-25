from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

Base = declarative_base()

# Tworzenie silnika bazy danych
engine = create_engine('sqlite:///task_manager.db', echo=False)

# Tworzenie sesji
Session = sessionmaker(bind=engine)
session = Session()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Priority(Base):
    __tablename__ = 'priorities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)