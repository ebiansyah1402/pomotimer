import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/tasks.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def main():
    """Lists user's tasks and upcoming calendar events"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, 
    # and is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    output_data = {"tasks": [], "calendar_events": [], "holidays": []}
    
    try:
        # Call the Tasks API
        service_tasks = build('tasks', 'v1', credentials=creds)
        results_tasklists = service_tasks.tasklists().list().execute()
        tasklists = results_tasklists.get('items', [])

        if tasklists:
            for tasklist in tasklists:
                task_result = service_tasks.tasks().list(tasklist=tasklist['id']).execute()
                tasks = task_result.get('items', [])
                if tasks:
                    for task in tasks:
                        output_data["tasks"].append({
                            "title": task.get('title'),
                            "due": task.get('due')
                        })

        # Call the Calendar API
        service_calendar = build('calendar', 'v3', credentials=creds)
        now_utc = datetime.datetime.now(datetime.UTC)
        timeMin_str = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
        timeMax_dt = now_utc + datetime.timedelta(days=7)
        timeMax_str = timeMax_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        max_results = 10

        # Fetch events from Primary Calendar
        events_primary_result = service_calendar.events().list(
            calendarId='primary',
            timeMin=timeMin_str,
            timeMax=timeMax_str,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events_primary = events_primary_result.get('items', [])
        if events_primary:
            for event in events_primary:
                start = event['start'].get('dateTime', event['start'].get('date'))
                output_data["calendar_events"].append({
                    "summary": event['summary'],
                    "start": start
                })

        # Fetch events from Holidays in Indonesia Calendar
        calendar_id_holidays = 'en.indonesian#holiday@group.v.calendar.google.com'
        calendar_id_name ='Holidays in Indonesia'
        events_holidays_result = service_calendar.events().list(
            calendarId=calendar_id_holidays,
            timeMin=timeMin_str,
            timeMax=timeMax_str,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events_holidays = events_holidays_result.get('items', [])
        if events_holidays:
            for event in events_holidays:
                start = event['start'].get('dateTime', event['start'].get('date'))
                output_data["holidays"].append({
                    "summary": event['summary'],
                    "start": start
                })
        
        #save data to JSON file
        with open('google_tasks_and_calendar.json', 'w') as f:
            json.dump(output_data, f, indent=4)    
    
    except HttpError as err:
        print(f'An error occurred: {err}')

if __name__ == '__main__':
    main()