import json


def loadConfig():
    try:
        with open('config.json', 'r') as file:
            configData = json.load(file)

            return configData
    except Exception as e:
        raise Exception(f'Failed to read config file. Error: {str(e)}')
