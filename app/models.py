from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, Enum, ForeignKey, JSON, Text
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime, timezone

Base = declarative_base()

class StatusEnum(enum.Enum):
    Not_Started = "Not Started"
    In_Progress = "In Progress"
    Bid_Sent = "Bid Sent"
    Bid_Won = "Bid Won"
    Bid_Lost = "Bid Lost"
    Completed = "Completed"

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    project_description = Column(Text)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    region = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.Not_Started)
    assigned_to = Column(String)
    bid_amount = Column(Float)
    expiry_date = Column(Date)
    audit_log = Column(JSON)

    bids = relationship("Bid", back_populates="project")

class Bid(Base):
    __tablename__ = 'bids'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    general_contractor = Column(String)
    email = Column(String)
    bid_expiry_date = Column(Date)
    email_content = Column(Text)
    links = Column(JSON)

    project = relationship("Project", back_populates="bids")

class EmailData(Base):
    __tablename__ = 'email_data'
    
    id = Column(Integer, primary_key=True)
    sender_email = Column(String)
    sender_name = Column(String)
    subject = Column(String)
    body = Column(String)
    has_attachments = Column(Boolean, default=False)
    history_id = Column(String)
    processed_at = Column(DateTime, default=datetime.now(timezone.utc))

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True) 
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String)