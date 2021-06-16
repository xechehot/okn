import fire
from pprint import pprint

from lib.config import config
from lib.data import load_from_tsv, save_to_json
from lib.geocode import Geocoder


def print_config():
    pprint(config)


coder = Geocoder(api_key=config['YANDEX_GEO_API_KEY'],
                 endpoint=config['YANDEX_GEO_ENDPOINT'])


def geocode_address(address):
    pprint(coder.geocode(address))


def geocode_df(source_df, geocode_json):
    df = load_from_tsv(source_df)
    geo = coder.get_geo_for_df(df)
    save_to_json(geo, geocode_json)

def main():
    fire.Fire()


if __name__ == '__main__':
    main()
