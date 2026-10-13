from sqlalchemy import create_engine, Column, Integer, String, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    location = Column(String)
    raw_text = Column(Text)
    structured_data = Column(JSON) # Store the full AI output here

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skill_name = Column(String, unique=True)

# Database setup helper
def init_db(db_url="sqlite:///./resume_parser.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
