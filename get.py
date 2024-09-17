import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GetDraftTimes:
    """
    A class to interact with the Gmail API to retrieve draft creation times and calculate the time difference
    from the current time.
 
    Attributes:
    - service: googleapiclient.discovery.Resource
        The Gmail API service instance.
    """

    def __init__(self):
        """
            Initializes with the provided credentials.
    
            Parameters:
            - credentials: Credentials
                The OAuth2 credentials to access the Gmail API.
    
            Raises:
            - ValueError:
                If the credentials are invalid or not provided.
            """
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json")
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json"
                    )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())


    def get_drafts(self):

        try:
            service = build("gmail", "v1", credentials=self.creds)
            drafts = service.users().drafts().list(userId='me').execute()
            draft_times = []

            if 'drafts' in drafts and drafts['resultSizeEstimate']!=0:
                for draft in drafts['drafts']:
                    draft_detail = service.users().drafts().get(userId='me', id=draft['id']).execute()
                    
                    # creation_time = draft_detail['internalDate']
                    # draft_times.append(datetime.datetime.fromtimestamp(int(creation_time) / 1000))
            else:
                raise Exception("There is no draft in your mailbox right now.")
            return drafts
        except Exception as e:
            raise Exception(f"An error occurred while retrieving drafts: {e}")

print(GetDraftTimes().get_drafts())
# times = GetDraftTimes()
# print(times)