from lib.geoitem import AbstractGeoItem
import pandas as pd
import logging

log = logging.getLogger(__name__)


class Geomapper(object):
    def __init__(self, geo_item: AbstractGeoItem):
        self.geo_item = geo_item

    def map_geo_for_df(self, df, geocode_result):
        map_data = []
        for _, row in df.iterrows():
            geo = geocode_result[str(row.id)]
            geo_collection = geo['response']['GeoObjectCollection']
            found = geo_collection['metaDataProperty']['GeocoderResponseMetaData']['found']
            if int(found) not in [1, 2]:
                log.warning('For row id=%s found %s geo objects, skipping... (%s)', row.id, found, row.obj_name)
                continue
            y, x = geo_collection['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
            data = self.geo_item.get_geo_item(row, x, y)
            map_data.append(data)
        return pd.DataFrame.from_records(map_data)
