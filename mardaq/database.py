import mysql.connector
from netrc import netrc
import os

from mardaq.core import initialize_logger



class MARDB():
    def __init__(self, database_name):
        self.dbname = database_name.lower()
        self._log = initialize_logger()
        self._get_db_creds()
        self.create_db()
        self.select_db()

    def _get_db_creds(self):
        drives = os.listdir(f"/media/{os.getlogin()}/")
        if len(drives) == 0:
            self._log.debug('No external drive detected.')
            raise NotADirectoryError('No external drive detected.')
        elif len(drives) == 1:
            [drive] = drives
            netrc_path = f"/media/{os.getlogin()}/{drive}/config/.netrc"
            self.__u, _, self.__p = netrc(netrc_path).authenticators('mardaq')
            self._log.info('Database credentials acquired.')
        elif len(drives) >= 2:
            raise NotImplementedError('Support for multiple data drives has not been implemented.')

    def create_db(self):
        self.mysqlcon = mysql.connector.connect(host = 'localhost', user = self.__u, password = self.__p) #localhost
        self.mysqlcur = self.mysqlcon.cursor(buffered = True)
        statement = f"CREATE DATABASE IF NOT EXISTS {self.dbname}"
        self.mysqlcur.execute(statement)
        self.mysqlcon.commit()
        self._log.info(f"{self.dbname} created as database if it did not exist.")

    def select_db(self):
        self.dbcon = mysql.connector.connect(host = 'localhost',user = self.__u, password = self.__p,
                                             database = self.dbname)
        self.dbcur = self.dbcon.cursor(buffered=True)
        self._log.info(f"{self.dbname} set as active deployment database.")


    def create_table(self, table_name, fields_dtypes):
        fields_dtypes = ', '.join([' '.join([k,v]) for k, v in fields_dtypes.items()])
        fields_dtypes = fields_dtypes + ', PRIMARY KEY (time)'
        statement = f"CREATE TABLE IF NOT EXISTS {table_name}({fields_dtypes})"
        self.dbcur.execute(statement)
        self._log.info(f"Created table {table_name} for database {self.dbname} if it did not exist.")


    def insert_table(self, table_name, fields_dtypes, data):
        fields = ', '.join(list(fields_dtypes.keys()))
        values = ', '.join(['%s'] * len (data))
        statement = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
        self.dbcur.execute(statement, data)
        self.dbcon.commit()
        self._log.info(f"Inserted data into table {table_name}.")


    def get_data(self,table_name, method = 'all'):
        if method == 'all':
            statement = f"SELECT * FROM {table_name}"
            self.dbcur.execute(statement)
        self._log.info(f'Acquired data from table {table_name}.')
        return self.dbcur.fetchall()


    def __enter__(self):
        return self


    def __exit__(self,et,ev,tb):
        self.mysqlcon.close()
        self.dbcon.close()
        self._log.info(f"Closed out database.")
