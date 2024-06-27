import json
from openai import OpenAI
from ..config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

system_message = """You are an email assistant for JR&Co, a roofing subcontractor. 
Your task is to extract and parse key information from incoming bid invitations. 
Specifically, identify the following details from emails sent by general contractors or subcontractors and output them in JSON format, if the Body or Sender is empty, return 
the available data as JSON and the fields for which the data is missing just return them as empty as part of the JSON object:

{
  "SenderName": "string, example: 'General Contractor Name'",
  "ProjectName": "string, example: 'Downtown Renovation'",
  "Location": {
    "State": "string, example: 'California'",
    "City": "string, example: 'Los Angeles'",
    "ZipCode": "string, example: '90001'",
    "StreetAddress": "string, example: '123 Main St'"
  },
  "BidExpiryDate": "date, format: 'YYYY-MM-DD', example: '2024-05-30'",
  "ProjectDescription": "string, brief, example: 'Renovation of a 20-story office building'",
  "ProjectLink": "URL, example: 'http://www.exampleprojectlink.com'",
  "Email": "string, example: 'contractor@example.com'",
  "EmailContent": "string, first 50 characters of the email body, example: 'Hi, we would like to invite you to bid...'"
}

Follow the specified field schema strictly. 
If any required information is missing in the email, leave the corresponding field blank but still include it in your response.
If the email does not contain any bid invitation details, output an empty JSON object: {}
"""

def get_json(email_data):
   sender_name = email_data['sender']
   email_address = email_data['email_address'].split('<')[-1].strip('>')
   subject = email_data['subject']
   body = email_data['body']
   
   email_text = f"From: {sender_name} <{email_address}>\nSubject: {subject}\n\n Body: {body}"

   print("Generating JSON.")
   completion = client.chat.completions.create(
   model="gpt-3.5-turbo",
   temperature=0.1,
   response_format={ "type": "json_object" },
   messages=[
      {"role": "system", "content": system_message},
      {"role": "user", "content": str(email_text)}
   ]
   )

   json_string = completion.choices[0].message.content
   if json_string:
       try:
           json_data = json.loads(json_string)
           return json_data
       except json.JSONDecodeError as e:
           print(f"Error parsing JSON: {str(e)}")
           return None
   else:
       return None