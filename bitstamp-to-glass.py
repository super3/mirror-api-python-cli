import json
import urllib2
import httplib2

from toglass import insert_timeline_item
from toglass import build_mirror


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

def run_card():
  message = get_bitstamp()
  mirror_service = build_mirror()
  insert_timeline_item(mirror_service, message, None, None, "DEFAULT", 'html')

if __name__ == "__main__":
  run_card()