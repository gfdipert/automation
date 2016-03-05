#uses Yelp API to grab cost of dinner and address of restaurant in city location

import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import json, ast
from bs4 import BeautifulSoup
from urllib2 import urlopen


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = '_Bw8ZSwd87GhXHgpq8o-fQ'
CONSUMER_SECRET = 'LOPzKjyjHr-e9Ec3iLIJ5Ik5HEU'
TOKEN = 'uD-OQeKbbi2XnYxrAqC22ndbfQ5GgNCX'
TOKEN_SECRET = 'exjb_01kod848E9822FvIN1QSdA'

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    #return response

    #return URL
    dic = response[response.keys()[2]][0]
    return dic[dic.keys()[2]]
    

def search(term, location):

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': 1
    }
    return request(API_HOST, SEARCH_PATH,url_params=url_params)

url = search('dinner','durham, nc')

html = urlopen(url).read()
soup = BeautifulSoup(html, "lxml")

item = soup.find("span", {"class":"business-attribute price-range"})
dollar = item.get_text()

item2 = soup.find("address", {"itemprop":"address"})
address = item2.get_text()

print dollar
print len(dollar)
print address

