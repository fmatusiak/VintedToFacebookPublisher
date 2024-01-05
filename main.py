import sys

from Facebook.facebook_publisher import FacebookPublisher
from config_loader import loadConfig
from product_updater import ProductUpdater


def main():
    try:
        config = loadConfig()

        productUpdater = ProductUpdater(config)
        productUpdater.update()

        publisher = FacebookPublisher(config)
        publisher.publish()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        sys.exit()


if __name__ == '__main__':
    main()
