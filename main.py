import fire


def hello(name):
    return 'Hello {name}!'.format(name=name)


def main():
    fire.Fire(hello)


if __name__ == '__main__':
    main()
