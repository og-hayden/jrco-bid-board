from sqlalchemy.orm import sessionmaker
from ..database import engine
from ..models import Project, Bid, StatusEnum
from datetime import datetime

Session = sessionmaker(bind=engine)

# FIXME
def calculate_region(address):
    return 'Default Region'

def add_or_update_bid(bid_data):
    session = Session()

    existing_project = session.query(Project).filter_by(
        address=bid_data['Location']['StreetAddress'],
        city=bid_data['Location']['City'],
        state=bid_data['Location']['State'],
        zip_code=bid_data['Location']['ZipCode']
    ).first()

    if existing_project:
        existing_bid = session.query(Bid).filter_by(
            project_id=existing_project.id,
            general_contractor=bid_data['SenderName'],
            email=bid_data['Email']
        ).first()

        if existing_bid:
            existing_bid.bid_expiry_date = datetime.strptime(bid_data['BidExpiryDate'], '%Y-%m-%d')
            existing_bid.email_content = bid_data.get('EmailContent', '')
            existing_bid.links = {'ProjectLink': bid_data['ProjectLink']}
        else:
            new_bid = Bid(
                project=existing_project,
                general_contractor=bid_data['SenderName'],
                email=bid_data['Email'],
                bid_expiry_date=datetime.strptime(bid_data['BidExpiryDate'], '%Y-%m-%d'),
                email_content=bid_data.get('EmailContent', ''),
                links={'ProjectLink': bid_data['ProjectLink']}
            )
            session.add(new_bid)
    else:
        new_project = Project(
            project_name=bid_data['ProjectName'],
            project_description=bid_data['ProjectDescription'],
            address=bid_data['Location']['StreetAddress'],
            city=bid_data['Location']['City'],
            state=bid_data['Location']['State'],
            zip_code=bid_data['Location']['ZipCode'],
            region=calculate_region(bid_data['Location']['State']),
            status=StatusEnum.Not_Started
        )
        session.add(new_project)
        session.flush()

        new_bid = Bid(
            project=new_project,
            general_contractor=bid_data['SenderName'],
            email=bid_data['Email'],
            bid_expiry_date=datetime.strptime(bid_data['BidExpiryDate'], '%Y-%m-%d'),
            email_content=bid_data.get('EmailContent', ''),
            links={'ProjectLink': bid_data['ProjectLink']}
        )
        session.add(new_bid)

    project = existing_project or new_project
    project.expiry_date = min(bid.bid_expiry_date for bid in project.bids)

    timestamp = datetime.now().isoformat()
    project.audit_log = project.audit_log or {}
    project.audit_log[timestamp] = f"Bid {'updated' if existing_project else 'added'} from {bid_data['SenderName']}"

    session.commit()
    session.close()