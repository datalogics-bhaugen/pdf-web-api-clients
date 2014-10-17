"enforce thumbnail usage limits"

import os
import platform
import time

import errors
import tmpdir

from sqlite3 import Connection


LINUX = (platform.system() == 'Linux')
DATABASE = os.path.join(tmpdir.ROOT_DIR, 'ThumbnailUsage.db')
DATABASE_TIMEOUT = 10  # seconds
THUMBNAIL_SERVERS = 2  # TODO: get this number dynamically

class UsageLimit(object):
    def __init__(self, max_requests, period_seconds):
        self._requests, self._seconds = max_requests, period_seconds
        self._servers = THUMBNAIL_SERVERS if LINUX else 1
    @property
    def max_requests_per_server(self): return self._requests / self._servers
    @property
    def seconds(self): return self._seconds

MINUTE = 60  # seconds
MONTH = 30 * 24 * 60 * MINUTE
USAGE_LIMITS = (UsageLimit(10, MINUTE), UsageLimit(1000, MONTH))

class ThumbnailUsage(Connection):
    def __init__(self, database=DATABASE, timeout=DATABASE_TIMEOUT):
        Connection.__init__(self, database, isolation_level='immediate',
                            timeout=timeout)
        self.execute('create table if not exists'
                     ' requests(network integer, timestamp integer)')
        self.execute('create index if not exists'
                     ' requests_network on requests(network)')
    def timestamps(self, network):
        sql = 'select timestamp from requests where network = ?'
        return [row[0] for row in self.execute(sql, (network,)).fetchall()]
    def update(self, network, timestamp):
        sql = 'delete from requests where network = ? and timestamp < ?'
        self.execute(sql, (network, timestamp - MONTH))
        sql = 'insert into requests values(?, ?)'
        self.execute(sql, (network, timestamp))

THUMBNAIL_USAGE = ThumbnailUsage()

class Usage(object):
    def __init__(self, remote_addr):
        self._network = remote_addr[1] + 256 * remote_addr[0]
        self._timestamp = int(time.time())
    def validate(self):
        with THUMBNAIL_USAGE:
            timestamps = THUMBNAIL_USAGE.timestamps(self.network)
            for usage_limit in USAGE_LIMITS:
                self._validate(timestamps, usage_limit)
            THUMBNAIL_USAGE.update(self.network, self.timestamp)
    def _validate(self, timestamps, usage_limit):
        min_timestamp = self.timestamp - usage_limit.seconds
        usage_timestamps = [t for t in timestamps if t >= min_timestamp]
        if len(usage_timestamps) >= usage_limit.max_requests_per_server:
            raise errors.USAGE_LIMIT_ERROR
    @property
    def network(self):
        "first two octets of the client's IP address (int)"
        return self._network
    @property
    def timestamp(self):
        "Unix time, i.e. #seconds since 1-jan-1970"
        return self._timestamp

def validate(request):
    remote_addr = [int(octet) for octet in request.remote_addr.split('.')]
    if LINUX:
        for private_network in ([127, 0, 0, 1], [10], [192, 168]):
            if private_network == remote_addr[:len(private_network)]:
                return  # monitor requests, etc.
        if remote_addr[0] == 172 and remote_addr[1] in range(16, 32):
            return  # AWS uses this range
    Usage(remote_addr).validate()
