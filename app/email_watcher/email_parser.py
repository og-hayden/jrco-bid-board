import base64
from bs4 import BeautifulSoup
import re
import html2text

def strip_html(html_content):
    # Convert HTML to plain text
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = True
    h.ignore_tables = True
    plain_text = h.handle(html_content)
    
    # Remove any remaining HTML tags
    plain_text = re.sub(r'<[^>]+>', '', plain_text)
    
    # Remove extra whitespace
    plain_text = re.sub(r'\s+', ' ', plain_text).strip()
    
    return plain_text

def extract_email_data(email):
    payload = email['payload']
    headers = payload['headers']

    from_header = next((header['value'] for header in headers if header['name'] == 'From'), None)
    if from_header:
        match = re.search(r'(.*?)\s*<', from_header)
        sender_name = match.group(1).strip() if match else None
        email_address = from_header
    else:
        sender_name = None
        email_address = None

    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)

    if 'parts' in payload:
        parts = payload['parts']
        body = None
        for part in parts:
            if part['mimeType'] == 'text/html':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                body = strip_html(body)
                break
            elif part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        if not body:
            body = ""
    else:
        body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        if payload.get('mimeType') == 'text/html':
            body = strip_html(body)

    has_attachments = 'attachmentId' in payload['body'] or 'attachmentId' in str(payload.get('parts', ''))

    return {
        'sender': sender_name,
        'email_address': email_address,
        'subject': subject,
        'body': body,
        'has_attachments': has_attachments
    }