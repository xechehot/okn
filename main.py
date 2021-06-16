import fire
from pprint import pprint

from lib.config import config


def print_config():
    pprint(config)


def main():
    fire.Fire()


if __name__ == '__main__':
    main()
