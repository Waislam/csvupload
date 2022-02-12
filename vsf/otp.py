# from __future__ import print_function

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re

import base64
import email

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://mail.google.com/']

class GmailOtp():

    def __init__(self):
        pass

    def mark_read(self, service, messages):
        for msg in messages:
            service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()
            break;

    def search_messages(self, service, messages):
        # result = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], q='from:donotreply@vfsglobal.com').execute()
        # messages = result.get('messages')

        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            otp_txt = txt['snippet']
            numbers = re.findall(r'\d+', otp_txt)
            for otp in numbers:
                return otp

            break;


    def gmail_authenticate(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        print('Authentication done')
        # message fetching starting from below
        result = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], q='from:donotreply@vfsglobal.com').execute()
        messages = result.get('messages')
        try:
            if messages:
                otp = self.search_messages(service, messages)
                self.mark_read(service, messages)
                return otp
            else:
                print('will search after sleeping')
                time.sleep(5)
                otp = self.search_messages(service, messages)
                self.mark_read(service, messages)
                return otp
        except:
            print('not found')
            return False





