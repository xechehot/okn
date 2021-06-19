from requests import request

from lib.geoitem import AbstractGeoItem


class Geocoder(object):
    def __init__(self, api_key, endpoint,
                 main_area=None):
        self.endpoint = endpoint
        self.api_key = api_key
        self.main_area = main_area

    def geocode(self, address):
        path = f'{self.endpoint}/?apikey={self.api_key}&format=json&geocode={address}'
        # headers = None
        res = request('get', path)
        if not 200 <= res.status_code < 300:
            print(res.status_code)
            raise Exception(res.text)
        return res.json()

    def get_geo_for_df(self, df):
        geocode_result = {}
        for i, row in df.iterrows():
            address = row.address if not self.main_area else f'{self.main_area}, {row.address}'
            geocode_result[row.id] = self.geocode(address)
        return geocode_result
