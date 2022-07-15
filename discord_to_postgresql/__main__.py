import fire

from discord_to_postgresql.run import run


def main():
    fire.Fire(run)


if __name__ == '__main__':
    main()