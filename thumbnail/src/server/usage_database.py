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
                     ' requests(remote_addr integer, timestamp integer)')
        self.execute('create index if not exists'
                     ' requests_remote_addr on requests(remote_addr)')
        self._max_period = max_period
    def timestamps(self, remote_addr):
        "Returns the usage timestamps for *remote_addr*."
        sql = 'select timestamp from requests where remote_addr = ?'
        rows = self.execute(sql, (remote_addr,)).fetchall()
        return [row[0] for row in rows]
    def update(self, remote_addr, timestamp):
        "Inserts a usage timestamp for *remote_addr*."
        if self._max_period:
            sql =\
                'delete from requests where remote_addr = ? and timestamp < ?'
            self.execute(sql, (remote_addr, timestamp - self._max_period))
        sql = 'insert into requests values(?, ?)'
        self.execute(sql, (remote_addr, timestamp))
