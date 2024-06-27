from flask import Blueprint, request, jsonify
from app.email_processor.openai_service import get_json
from app.email_processor.add_bid import add_or_update_bid
from app.database import get_email_data_by_history_id

email_processor_bp = Blueprint('email_processor', __name__)

@email_processor_bp.route('/process_email', methods=['POST'])
def process_email():
    email_id = request.json.get('email_id')
    
    if not email_id:
        return jsonify({'error': 'email_id is required'}), 400
    
    email_data = get_email_data_by_history_id(email_id)
    
    if email_data:
        email_text = {
            'subject': email_data.subject,
            'body': email_data.body,
            'sender': email_data.sender_name,
            'email_address': email_data.sender_email,
        }
        
        json_data = get_json(email_text)

        if json_data:
            add_or_update_bid(json_data)
            return jsonify({'message': f"Bid data processed successfully for email {email_id}.", 'data': json_data}), 200
        else:
            return jsonify({'message': f"No valid bid data found in email {email_id}."}), 400
    else:
        return jsonify({'error': f"Email data not found for email {email_id}."}), 404