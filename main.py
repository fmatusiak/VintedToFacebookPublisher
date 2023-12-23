import sys

from ConfigLoader import loadConfig
from Facebook.FacebookPages import FacebookPublisher
from ProductUpdater import ProductUpdater

if __name__ == '__main__':
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
