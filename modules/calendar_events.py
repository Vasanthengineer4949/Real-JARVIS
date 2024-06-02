import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      return

    # Prints the start and name of the next 10 events
    return_events = []
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      parsed_datetime = datetime.datetime.fromisoformat(start)
      date_ist = parsed_datetime.date()
      time_ist = parsed_datetime.time()
      return_events.append("Date: " + str(date_ist) + ", Time: " + str(time_ist) + ", Event: " + event["summary"])
    
    return "\n".join(return_events)

  except HttpError as error:
    print(f"An error occurred: {error}")

def create_event(date, start_time, end_time, summary):
  """Shows basic usage of the Google Calendar API.
  Prints start and name of the next 10 events on the user's calendar.
  """
  creds = None

  start_date_str = date + start_time
  end_date_str = date + end_time

  start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d%I:%M%p')
  end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d%I:%M%p')

  start_time = start_date.isoformat()
  end_time = end_date.isoformat()
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    # creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    os.remove("token.json")

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

    try:
      service = build("calendar", "v3", credentials=creds)

      # Call the Calendar API
      with open("schedule_events.json", "r+") as f:
        event = json.load(f)

      event["start"]["dateTime"] = start_time
      event["end"]["dateTime"] = end_time
      event["summary"] = summary
      print(event)
      event = service.events().insert(calendarId='primary', body=event).execute()
      
      return 'Event Created'

    except HttpError as error:
      print(f"An error occurred: {error}")