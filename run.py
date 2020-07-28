import os, json, time
from email_manager import EmailManager
import sentry_sdk
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(funcName)s - %(message)s")
LOGGER = logging.getLogger(__name__)


# Getting information from config.JSON
def load_config():
    try:
        with open("./config.json") as config_contents:
            config = json.load(config_contents)
            for cnf in config.keys():
                os.environ[cnf] = config[cnf]
    except:
        raise Exception('Please edit config.JSON file.')


# Loading config and starting the program.
def main():
    load_config()
    sentry_sdk.init(os.environ['SENTRY_TOKEN'])

    while True:
        email_manager = EmailManager()
        try:
            email_manager.download_attachments()
        except Exception as e:
            LOGGER.info("ERROR")
            raise e
        time.sleep(int(os.environ['sleep_seconds']))  # wait


if __name__ == "__main__":
    main()
