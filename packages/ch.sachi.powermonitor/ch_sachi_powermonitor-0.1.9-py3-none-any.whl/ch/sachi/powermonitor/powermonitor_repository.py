import datetime
import logging
import os
import sqlite3
from typing import List

from victron_ble.devices import BatteryMonitorData


class MonitorRepository:
    def __init__(self, database=None):
        self.database = database

    def init(self) -> None:
        if os.path.isfile(self.database):
            logging.debug('Database ' + self.database + 'does exist already')
            return

        logging.debug('Initialize database ' + self.database)
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS powermon (
                    id INTEGER PRIMARY KEY,
                    created_at TIMESTAMP NOT NULL,
                    current real NOT NULL,
                    voltage real NOT NULL,
                    soc real NOT NULL,
                    consumed_ah real NOT NULL,
                    second_voltage real NOT NULL
                    )''')

    def write(self, data: BatteryMonitorData):
        if data is None:
            return
        logging.info('Save to database')
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            now = datetime.datetime.now()
            cur.execute('''INSERT INTO powermon(
                created_at, 
                current, 
                voltage, 
                soc, 
                consumed_ah, 
                second_voltage) 
                values(?, ?, ?, ?, ?, ?)
                ''',
                        (
                            now,
                            data.get_current(),
                            data.get_voltage(),
                            data.get_soc(),
                            data.get_consumed_ah(),
                            data.get_starter_voltage()
                        )
                        )

    def get_measures_after(self, last: str) -> List:
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT "
                "m.created_at, "
                "m.current, "
                "m.voltage, "
                "m.soc, "
                "m.consumed_ah, "
                "m.second_voltage "
                "from powermon m "
                "where m.created_at >= datetime(?, '+1 second')",
                last
            )
            records = cur.fetchall()
            measures_data = []
            for record in records:
                data = {
                    'created_at': record[0],
                    'current': str(record[1]),
                    'voltage': str(record[2]),
                    'soc': str(record[3]),
                    'consumed_ah': str(record[4]),
                    'second_voltage': str(record[5])
                }
                measures_data.append(data)
            return measures_data
