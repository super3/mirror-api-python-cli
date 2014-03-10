#!/usr/bin/python

import sys
import json
import pprint
import urllib2
import httplib2


from apiclient.discovery import build
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow


# Generate a default exchange card, with the exchange logo in the left, and 
# places for the last price, bid, and ask. Note: That this assumes that this is 
# a USD/BTC card. So you if want to expand it you have to change those details.
def exchange_card(img, last, bid, ask):
	return """
	<article>
	  <figure>
	    <img src="{0}"/>
	  </figure>
	  <section>
	    <h1 class="text-large">Bitstamp</h1>
	    <p class="text-x-small">
	      {1} USD &#47; BTC
	    </p>
	    <hr>
	    <p class="text-normal">
	      <div class="green">Bid: &#36;{2}</div>
	      <div class="red">Ask: &#36;{3}</div>
	    </p>
	  </section>
	</article>
	""".format(img, last, bid, ask)


# grab and parse the Bitstamp API to get the ticket info
def get_bitstamp():
	response = urllib2.urlopen('https://www.bitstamp.net/api/ticker/')
	data = json.load(response)
	last, bid, ask = str(data['last']), str(data['bid']), str(data['ask'])
	return exchange_card("http://i.imgur.com/WFl6Q2p.png", last, bid, ask)

message = get_bitstamp()

def insert_timeline_item(service, html, content_type=None, attachment=None,
                         notification_level=None):
  timeline_item = {'html': html}
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

# load the credentials from the file
storage = Storage('credentials')
credentials = storage.get()

# create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

# create a Mirror API service
mirror_service = build('mirror', 'v1', http=http)

# insert it into the timeline
insert_timeline_item(mirror_service, message, None, None, "DEFAULT")

