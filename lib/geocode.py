from requests import request


class Geocoder(object):
    def __init__(self, api_key, endpoint='https://geocode-maps.yandex.ru/1.x'):
        self.endpoint = endpoint
        self.api_key = api_key
        self.main_area = 'Свердловская область, г. Екатеринбург'

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
            geocode_result[row.id] = self.geocode(f'{self.main_area}, {row.address}')
        return geocode_result

    def get_google_item(self, row, x, y):
        data = {
            'x': x,
            'y': y,
            'name': row.obj_name,
            'reg_id': row.reg_id,
            'type': row.type,
            'date': row.date,
            'address': row.address,
            'form_link': f'https://docs.google.com/forms/d/e/1FAIpQLSdo5DGW_9RLSg_yvQE4Vr-egpqH6gqSNHFsqn7miGK5_tmnGQ/viewform?usp=pp_url&entry.2006182935={row.reg_id}',
            'state': '-',
            'comment': ''
        }
        return data

    def map_geo_for_df(self, df, geocode_result):
        map_data = []
        for _, row in df.iterrows():
            geo = geocode_result[str(row.id)]
            geo_collection = geo['response']['GeoObjectCollection']
            found = geo_collection['metaDataProperty']['GeocoderResponseMetaData']['found']
            if int(found) not in [1, 2]:
                print(f'WARN: {row.id}: found {found}')
                continue
            y, x = geo_collection['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
            #     data = get_yandex_item(row)
            data = self.get_google_item(row, x, y)
            map_data.append(data)
        return map_data
