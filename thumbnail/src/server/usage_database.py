"The thumbnail server stores usage information in a database."

import os

import tmpdir
from sqlite3 import Connection


DATABASE = os.path.join(tmpdir.ROOT_DIR, 'thumbnail', 'usage.db')
DATABASE_TIMEOUT = 10  # seconds


class Database(Connection):
    "Each server has its own database."
    def __init__(self, max_period,
                 database=DATABASE, timeout=DATABASE_TIMEOUT):
        Connection.__init__(self, database, isolation_level='immediate',
                            timeout=timeout)
        self.execute('create table if not exists'
                     ' requests(network integer, timestamp integer)')
        self.execute('create index if not exists'
                     ' requests_network on requests(network)')
        self._max_period = max_period
    def timestamps(self, client_network):
        "Returns the usage timestamps for *client_network*."
        sql = 'select timestamp from requests where network = ?'
        rows = self.execute(sql, (client_network,)).fetchall()
        return [row[0] for row in rows]
    def update(self, client_network, timestamp):
        "Inserts a usage timestamp for *client_network*."
        if self._max_period:
            sql = 'delete from requests where network = ? and timestamp < ?'
            self.execute(sql, (client_network, timestamp - self._max_period))
        sql = 'insert into requests values(?, ?)'
        self.execute(sql, (client_network, timestamp))
