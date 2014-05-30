#!/usr/bin/python

import sys
import pprint
import httplib2

from oauth2client.file import Storage
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

def insert_timeline_item(service, text, content_type=None, attachment=None,
                         notification_level=None, item_type='text'):
  timeline_item = {item_type: text}
  media_body = None
  if notification_level:
    timeline_item['notification'] = {'level': notification_level}
  if content_type and attachment:
    media_body = MediaIoBaseUpload(
      io.BytesIO(attachment), mimetype=content_type, resumable=True)
  try:
    return service.timeline().insert(
      body=timeline_item, media_body=media_body).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def build_mirror():
  # load the credentials from the file
  storage = Storage('credentials')
  credentials = storage.get()

  # Create an httplib2.Http object and authorize it with our credentials
  http = httplib2.Http()
  http = credentials.authorize(http)

  # create a Mirror API service
  return build('mirror', 'v1', http=http)

def command_line():
  # Get command line argument
  try:
    message = str(sys.argv[1])
  except IndexError:
    print 'Error! Usage send-to-glass.py \'Hello World!\''

  # insert it into the timeline
  mirror_service = build_mirror()
  insert_timeline_item(mirror_service, message, None, None, "DEFAULT", 'text')

if __name__ == "__main__":
  command_line()