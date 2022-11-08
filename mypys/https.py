import httplib
import urllib

params = urllib.urlencode({'fsym': 'BTC', 'tsyms': 'USD,EUR'})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPSConnection("min-api.cryptocompare.com")
conn.request("POST", "/data/price", params, headers)
response = conn.getresponse()
print response
conn.close()
