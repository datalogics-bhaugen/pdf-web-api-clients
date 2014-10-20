"usage database"

import os

import tmpdir
from sqlite3 import Connection


DATABASE = os.path.join(tmpdir.ROOT_DIR, 'ThumbnailUsage.db')
DATABASE_TIMEOUT = 10  # seconds


class Database(Connection):
    def __init__(self, max_period,
                 database=DATABASE, timeout=DATABASE_TIMEOUT):
        Connection.__init__(self, database, isolation_level='immediate',
                            timeout=timeout)
        self.execute('create table if not exists'
                     ' requests(network integer, timestamp integer)')
        self.execute('create index if not exists'
                     ' requests_network on requests(network)')
        self._max_period = max_period
    def timestamps(self, network):
        sql = 'select timestamp from requests where network = ?'
        return [row[0] for row in self.execute(sql, (network,)).fetchall()]
    def update(self, network, timestamp):
        if self._max_period:
            sql = 'delete from requests where network = ? and timestamp < ?'
            self.execute(sql, (network, timestamp - self._max_period))
        sql = 'insert into requests values(?, ?)'
        self.execute(sql, (network, timestamp))
