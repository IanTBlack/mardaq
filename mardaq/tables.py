class TABLES:
    class PUMP:
        write = f"INSERT INTO pump (serial_number, datetime, pump_relay_state, pump_on) VALUES (%s, %s, %s, %s)"
        setup = "CREATE TABLE IF NOT EXISTS pump (serial_number CHAR(10), datetime DATETIME, pump_relay_state BOOLEAN, pump_on BOOLEAN)"