import fire
from pprint import pprint

from lib.config import config
from lib.data import load_from_tsv, save_to_json, load_from_json, save_to_tsv
from lib.exceptions import FormLinkNotFoundError
from lib.geocode import Geocoder
from lib.geoitem import GoogleGeoItem, YandexGeoItem, geo_item_factory
from lib.geomapper import Geomapper
import logging
logging.basicConfig()
log = logging.getLogger(__name__)


def print_config():
    pprint(config)


def get_geocoder(main_area=None):
    return Geocoder(api_key=config['YANDEX_GEO_API_KEY'],
                    endpoint=config['YANDEX_GEO_ENDPOINT'],
                    main_area=main_area or config.get('MAIN_AREA', None))


def geocode_address(address, main_area=None):
    coder = get_geocoder(main_area)
    pprint(coder.geocode(address))


def geocode_df(source_df, geocode_json, main_area=None):
    df = load_from_tsv(source_df)
    coder = get_geocoder(main_area)
    geo = coder.get_geo_for_df(df)
    save_to_json(geo, geocode_json)


def map_geo_for_df(source_path, output_path,
                   geocode_json=None,
                   geo_service=None,
                   form_link=None,
                   main_area=None):
    df = load_from_tsv(source_path)
    if geocode_json is not None:
        geocode_result = load_from_json(geocode_json)
    else:
        coder = get_geocoder(main_area)
        geocode_result = coder.get_geo_for_df(df)
    form_link = form_link or config['FORM_LINK']
    if form_link is None:
        raise FormLinkNotFoundError()
    mapper = Geomapper(geo_item_factory(geo_service, form_link))
    result_df = mapper.map_geo_for_df(df, geocode_result)
    save_to_tsv(result_df, output_path)


def main():
    fire.Fire()


if __name__ == '__main__':
    main()
