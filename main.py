import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helper import parse

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]


def send_reminder():
    try:
        service = build("gmail", "v1", credentials=get_creds())
        message = EmailMessage()

        message.set_content(get_drafts()["body"])

        message["To"] = "yli292@fordham.edu"
        message["From"] = "alvenli1009@gmail.com"
        message["Subject"] = f"hey you have {get_drafts()['count']} drafts LOOK!"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


def get_drafts():
    """Retrieve draft texts"""
    try:
        service = build("gmail", "v1", credentials=get_creds())
        drafts = service.users().drafts().list(userId="me").execute().get("drafts")
        draft_count = len(drafts)
        body = "".join(
            [
                parse(
                    service.users()
                    .drafts()
                    .get(userId="me", id=draft["id"], format="raw")
                    .execute()["message"]["raw"]
                )
                for draft in drafts
            ]
        )

        if not drafts:
            print("No drafts found.")
            return
        print("drafts:")
        for draft in drafts:
            print(draft["message"])

    except HttpError as error:
        return f"An error occurred: {error}"
    return {"body": body, "count": draft_count}


def get_creds():
    """Return credentials"""
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
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


send_reminder()
