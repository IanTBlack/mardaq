from datetime import datetime, timezone, timedelta
import numpy as np
import psycopg2 as pg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, register_adapter, AsIs
register_adapter(np.uint16, AsIs)
register_adapter(np.int64, AsIs)
register_adapter(np.float64, AsIs)

from mardaq.core import console_logger

class PGDB():
    def __init__(self, deployment, user, password):
        self.console_log = console_logger(1)
        self.deployment = deployment.lower()
        self.__u, self.__p = (user, password)
        self.connect2pg()
        self.setup_database()
        self.connect2db()

    def __enter__(self):
        return self

    def __exit__(self, et, ev, etb):
        self._pgcon.close()
        self._dbcon.close()
        self.console_log.debug("Closed out of all connections.")

    def connect2pg(self):
        """Connect to the maintenance database."""
        self._pgcon = pg2.connect(f"dbname=postgres user={self.__u} password={self.__p}") # Maintenance connection.
        self._pgcon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.console_log.debug("Connected to maintenance database 'postgres'.")
        self._pgcur = self._pgcon.cursor() # Maintenance cursor.
        self.console_log.debug("Maintenance cursor created.")

    def setup_database(self):
        statement = f"CREATE DATABASE {self.deployment}"
        try:  # A try-except is needed because PostgreSQL does not yet support 'IF NOT EXISTS' for database creation.
            self._pgcur.execute(statement)
            self.console_log.info(f"Created database {self.deployment}.")
        except:
            if self.database_exists():
                self.console_log.debug(f"Database '{self.deployment}' already exists. Skipping setup.")
            else:
                self.console_log.critical(f"There was an error when trying to create database '{self.deployment}'.")

    def connect2db(self):
        """Connect to the deployment database."""
        self._dbcon = pg2.connect(f"dbname={self.deployment} user={self.__u} password={self.__p}") # Database connection.
        self._dbcon.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.console_log.debug(f"Connected to database '{self.deployment}'.")
        self._dbcur = self._dbcon.cursor() # Database cursor.
        self.console_log.debug("Database cursor created.")

    def setup_table(self, table_name, fields_dtypes: dict, pk = 'time'):
        fields_dtypes_str = ', '.join([' '.join([k, v]) for k, v in fields_dtypes.items()]) + f", PRIMARY KEY ({pk})"
        statement = f"CREATE TABLE IF NOT EXISTS {table_name}({fields_dtypes_str})"
        self._dbcur.execute(statement)
        if self.table_exists(table_name):
            self.console_log.debug(f"Table '{table_name}' created.")
            self.console_log.debug(f"Primary key for table '{table_name}' is '{pk}'.")
        else:
            self.console_log.error(f"Error creating table '{table_name}' in '{self.deployment}'.")

    def insert_data(self, table_name, fields_data):
        fields = ', '.join(list(fields_data.keys()))
        data = list(fields_data.values())
        values = ', '.join(['%s'] * len(data))
        statement = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
        self._dbcur.execute(statement, data)
        self.console_log.debug(f"Data inserted into table '{table_name}'.")

    def get_data(self, table_name):
        statement = f"SELECT * FROM {table_name}"
        self._dbcur.execute(statement)
        data = self._dbcur.fetchall()
        return data


    def get_last_day(self,table_name):
        dt_new = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        dt_old = (datetime.now(timezone.utc)).strftime('%Y-%m-%d')
        statement = f"SELECT * FROM {table_name} WHERE time BETWEEN '{dt_old}' AND '{dt_new}'"
        self._dbcur.execute(statement)
        data = self._dbcur.fetchall()
        return data

    def get_last_hour(self,table_name):
        dt = datetime.now(timezone.utc)
        dt_new = dt.strftime('%Y-%m-%d %H:%M:%S')
        dt_old = dt - timedelta(hours = 1)
        statement = f"SELECT * FROM {table_name} WHERE time BETWEEN '{dt_old}' AND '{dt_new}'"
        self._dbcur.execute(statement)
        data = self._dbcur.fetchall()
        return data



#----------------------------------------------Helper Functions-------------------------------------------------------#
    def list_databases(self):
        self._pgcur.execute("SELECT datname FROM pg_database")
        databases = [dbinfo[0] for dbinfo in self._pgcur.fetchall()]
        return databases

    def database_exists(self):
        databases = self.list_databases()
        if self.deployment in databases:
            return True
        else:
            return False

    def list_database_tables(self):
        self._dbcur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [table_info[0] for table_info in self._dbcur.fetchall()]
        return tables

    def table_exists(self,table_name):
        tables = self.list_database_tables()
        if table_name in tables:
            return True
        else:
            return False

