from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(80))
    city = Column(String(20))
    stream = Column(String(20))
    gender = Column(String(7))


engine = create_engine('sqlite:///student.db')
Base.metadata.create_all(engine)
