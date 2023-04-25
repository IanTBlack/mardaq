from mardaq.core import *

class MARDB():
    """
    A class for instantiating an issued database with tables for data logging.
    Functions for logging data to these tables are also provided.
    """
    def __init__(self, cruise_id):
        self.u, _, self.p = netrc(NETRC_LOC).authenticators('mardaq')
        self.connection = mysql.connector.connect(user = self.u, password = self.p, host = 'localhost')
        self.cursor = self.connection.cursor(buffered = True)
        self.setup_db(cruise_id)
        self.setup_tables()



    def setup_db(self, cruise_id):
        self.cruise_id = str(cruise_id).lower()
        statement = f"CREATE DATABASE IF NOT EXISTS {self.cruise_id}"
        self.cursor.execute(statement)
        self.connection = mysql.connector.connect(user=self.u, password=self.p, host='localhost',
                                                  database=self.cruise_id)
        self.cursor = self.connection.cursor(buffered = True)

    def setup_tables(self):
        self.setup_gps_table()
        self.setup_pump_table()
        self.setup_valve_table()
        self.setup_flow_table()
        self.setup_tsg_table()

    def setup_pump_table(self):
        statement = "CREATE TABLE IF NOT EXISTS pump (serial_number CHAR(10), datetime DATETIME, pump_relay_state BOOLEAN, pump_on BOOLEAN)"
        self.cursor.execute(statement)


    def write_pump(self, data_tuple):
        statement = f"INSERT INTO pump (serial_number, datetime, pump_relay_state, pump_on) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(statement, data_tuple)
        self.connection.commit()

    def read_pump(self,export_as = 'pandas'):
        columns = ['sn','datetime','pump_relay_state','pump_on']
        statement = f"SELECT * FROM pump"
        self.cursor.execute(statement)
        data = self.cursor.fetchall()

        if export_as == "list":
            return data
        elif export_as == 'pandas':
            df = pd.DataFrame(data,columns = columns)
            return df

    def setup_valve_table(self):
        statement = "CREATE TABLE IF NOT EXISTS valve (serial_number CHAR(10), datetime DATETIME, valve_relay_state BOOLEAN, seawater_state CHAR(3))"
        self.cursor.execute(statement)

    def write_valve(self, data_tuple):
        statement = f"INSERT INTO valve (serial_number, datetime, valve_relay_state, seawater_state) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(statement, data_tuple)
        self.connection.commit()

    def read_valve(self,export_as = 'pandas'):
        columns = ['sn','datetime','valve_relay_state','seawater_state']
        statement = f"SELECT * FROM valve"
        self.cursor.execute(statement)
        data = self.cursor.fetchall()

        if export_as == "list":
            return data
        elif export_as == 'pandas':
            df = pd.DataFrame(data,columns = columns)
            return df

    def setup_flow_table(self):
        statement = "CREATE TABLE IF NOT EXISTS flow (serial_number CHAR(10), datetime DATETIME, kfactor FLOAT, pulses INT, ml FLOAT, ml_per_min FLOAT)"
        self.cursor.execute(statement)

    def write_flow(self, data_tuple):
        statement = f"INSERT INTO flow (serial_number, datetime, kfactor, pulses, ml, ml_per_min) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(statement, data_tuple)
        self.connection.commit()

    def setup_gps_table(self):
        statement = "CREATE TABLE IF NOT EXISTS gps (serial_number CHAR(10), datetime DATETIME, raw_string VARCHAR(255), status CHAR(10), gps_datetime DATETIME, latitude FLOAT, longitude FLOAT, cog FLOAT, speed FLOAT)"
        self.cursor.execute(statement)

    def write_gps(self, data_tuple):
        statement = f"INSERT INTO gps (serial_number, datetime, raw_string, status, gps_datetime, latitude, longitude, cog, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(statement, data_tuple)
        self.connection.commit()


    def read_gps(self,export_as = 'pandas'):
        columns = ['sn','datetime','raw_string','status','gps_datetime','latitude','longitude','cog','speed']
        statement = f"SELECT * FROM gps"
        self.cursor.execute(statement)
        data = self.cursor.fetchall()

        if export_as == "list":
            return data
        elif export_as == 'pandas':
            df = pd.DataFrame(data,columns = columns)
            return df


    def setup_tsg_table(self):
        statement = "CREATE TABLE IF NOT EXISTS tsg (serial_number CHAR(10), datetime DATETIME, temperature FLOAT, conductivity FLOAT)"
        self.cursor.execute(statement)

    def write_tsg(self, data_tuple):
        statement = f"INSERT INTO tsg (serial_number, datetime, temperature, conductivity) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(statement, data_tuple)
        self.connection.commit()

    def read_tsg(self,export_as = 'pandas'):
        columns = ['sn','datetime','temperature','conductivity']
        statement = f"SELECT * FROM tsg"
        self.cursor.execute(statement)
        data = self.cursor.fetchall()

        if export_as == "list":
            return data
        elif export_as == 'pandas':
            df = pd.DataFrame(data,columns = columns)
            return df
