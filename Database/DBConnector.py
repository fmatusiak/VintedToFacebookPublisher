import mysql.connector


class DBConnector:
    def __init__(self, config):
        self.config = config

    def getDB(self):
        return mysql.connector.connect(
            host=self.config.get('db_host'),
            user=self.config.get('db_user'),
            password=self.config.get('db_password'),
            database=self.config.get('db_name')
        )
