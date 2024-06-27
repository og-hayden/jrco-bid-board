from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from models import EmailData, Project, Bid, Users
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

def store_email_data(email_data, history_id):
    session = Session()
    new_email = EmailData(
        sender_email=email_data.get('email_address'),
        sender_name=email_data.get('sender'),
        subject=email_data.get('subject'),
        body=email_data.get('body'),
        has_attachments=email_data.get('has_attachments', False),
        history_id=history_id,
        processed_at=datetime.now(timezone.utc)
    )
    session.add(new_email)
    session.commit()
    session.close()

def get_email_data_by_history_id(history_id, session=None):
    if session is None:
        Session = sessionmaker(bind=engine)
        session = Session()
    
    email_data = session.query(EmailData).filter(EmailData.history_id == history_id).first()
    
    if session.new:
        session.close()
    
    return email_data

def get_last_processed_history_id():
    session = Session()
    last_processed = session.query(EmailData).order_by(desc(EmailData.processed_at)).first()
    session.close()
    return last_processed.history_id if last_processed else None

def check_email_exists(email_data, session=None):
    if session is None:
        Session = sessionmaker(bind=engine)
        session = Session()

    exists_query = session.query(EmailData).filter(
        and_(
            EmailData.sender_email == email_data['email_address'],
            EmailData.sender_name == email_data['sender'],
            EmailData.subject == email_data['subject']
        )
    ).exists()

    result = session.query(exists_query).scalar()

    if session.new:
        session.close()

    return result