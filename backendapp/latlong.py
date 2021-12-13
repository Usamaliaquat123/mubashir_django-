import requests
import logging
from django.conf import settings
db_logger = logging.getLogger('backendapp')

#find lat & long using venue and address
def find_LatLong(address):
    try:
        address = address.replace(' ', '+')
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': address,
            'sensor': 'false',
            'key': settings.GOOGLE_API_KEY
        }
        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()
        return res
    except Exception as e:
        db_logger.exception(e)
        return False

#find lat & long
def find_zipcode(zipcode):

      try:
         location   = {}
         GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
         params = {
               'address': zipcode,
               'sensor': 'false',
               'key': settings.GOOGLE_API_KEY
         }
         # Do the request and get the response data
         req = requests.get(GOOGLE_MAPS_API_URL, params=params)
         res = req.json()
         if res['status'] == 'OK':
               result                   = res['results'][0]
               location['latitude']     = result['geometry']['location']['lat']
               location['longitude']    = result['geometry']['location']['lng']
         return location

      except Exception as e:

        db_logger.exception(e)

        return False