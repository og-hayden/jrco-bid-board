from app.email_watcher.gmail_service import gmail_authentication, set_up_watch_request, get_email, stop_watch_request
from app.email_watcher.email_parser import extract_email_data
from app.database import store_email_data, check_email_exists
import time
from googleapiclient.errors import HttpError
import requests

def process_new_emails():
    service = gmail_authentication()
    print("Starting email watcher. Watching for new emails...")
    
    while True:
        try:
            history_id = set_up_watch_request(service)
            
            print(f"Watching for new emails. Starting from history ID: {history_id}")
            
            while True:
                try:
                    # Check for new emails
                    history = service.users().history().list(userId='me', startHistoryId=history_id).execute()
                    
                    if 'history' in history:
                        # Process only the most recent email
                        latest_history = history['history'][-1]
                        if 'messages' in latest_history:
                            email_id = latest_history['messages'][0]['id']
                            
                            # Retrieve the email
                            email = get_email(service, 'me', email_id)
                            
                            # Extract email data
                            email_data = extract_email_data(email)
                            
                            # Check if the email has already been processed
                            if not check_email_exists(email_data):
                                # Store email data in the database
                                new_history_id = latest_history['id']
                                store_email_data(email_data, new_history_id)
                                
                                print(f"Email data stored successfully for email {email_id}.")
                                print(f"New history ID: {new_history_id}")

                                # Trigger email processor
                                try:
                                    url = "http://localhost:8080/process_email"  # Update this URL as needed
                                    payload = {
                                        "email_id": new_history_id
                                    }
                                    headers = {
                                        "Content-Type": "application/json"
                                    }

                                    print(f"Making API request to URL: {url}")
                                    response = requests.post(url, json=payload, headers=headers, timeout=70)
                                    print("API request completed.")

                                    if response.status_code == 200:
                                        print(f"API request successful for email {email_id}.")
                                        print(response.json())
                                    else:
                                        print(f"Unexpected status code: {response.status_code} for email {email_id}")
                                        print(response.text)
                                except Exception as e:
                                    print(f"Error occurred during API request: {str(e)}")
                            else:
                                print(f"Email {email_id} already exists. Skipping.")
                        
                        # Break out of the inner loop to start watching again
                        break
                    
                    # If no new emails, continue watching
                    print("No new emails. Continuing to watch...")
                    time.sleep(10)  # Wait for 10 seconds before checking again
                
                except HttpError as error:
                    if error.resp.status == 404:
                        print("Watch request expired. Restarting the watch request.")
                        break  # Break the inner loop to restart the watch request
                    else:
                        print(f"Error occurred: {str(error)}")
                        raise error
        
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            time.sleep(10)  # Wait for a short interval before retrying
        
        finally:
            # Stop watching for new emails before restarting the watch request
            stop_watch_request(service)

def start_email_processing():
    process_new_emails()