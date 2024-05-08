import psycopg2

class PostgresPilotHandler:
    def __init__(self):
        None


    def connection_to_postgresql(self, connection_url):
        try:
            self.db_connection = psycopg2.connect(connection_url)
            self.cursor = self.db_connection.cursor()
            self.db_connection.autocommit = True
        except psycopg2.Error as error:
            return error
    
    def create_postgresql_database(self, database_name):
        try:
            self.cursor.execute(f"CREATE DATABASE {database_name}")
        except psycopg2.Error as error:
            return error
    
    def delete_postgresql_database(self, database_name):
        try:
            self.cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        except psycopg2.Error as error:
            return error
