"enforce usage limits"

import platform
import requests
import time

import cfg
import errors
import logger
import tmpdir

from lxml import etree
from usage_database import Database


ADMIN_URL = 'https://datalogics-cloud-admin.3scale.net'
GET_LIMITS = '/admin/api/application_plans/{}/limits.xml'

# TODO: support 'eternity'
SECONDS = {'minute': 60,
           'hour': 60 * 60,
           'day': 60 * 60 * 24,
           'week': 60 * 60 * 24 * 7,
           'month': 60 * 60 * 24 * 30,
           'year': 60 * 60 * 24 * 365}

LINUX = (platform.system() == 'Linux')
THUMBNAIL_SERVERS = 2  # TODO: get this number dynamically

class UsageLimit(object):
    def __init__(self, max_requests, period):
        self._requests, self._period = max_requests, period
        self._servers = THUMBNAIL_SERVERS if LINUX else 1
    def __str__(self):
        return "UsageLimit({}, '{}')".format(self._requests, self._period)
    def validate(self, timestamp, timestamps):
        min_timestamp = timestamp - self.seconds
        usage_timestamps = [t for t in timestamps if t >= min_timestamp]
        if len(usage_timestamps) >= self.max_requests_per_server:
            raise errors.USAGE_LIMIT_ERROR
    @classmethod
    def get(cls, plan_id=cfg.Configuration.three_scale.public_plan_id):
        result = []
        url = ADMIN_URL + GET_LIMITS.format(plan_id)
        params = {'provider_key': cfg.Configuration.three_scale.provider_key}
        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:
            for limit in etree.fromstring(response.text.encode('utf-8')):
                value = limit.xpath('value')[0].text
                period = limit.xpath('period')[0].text
                usage_limit = UsageLimit(int(value), period)
                logger.debug('retrieved {}'.format(usage_limit))
                result.append(usage_limit)
        else:
            logger.error('cannot get usage limits for plan {}'.format(plan_id))
        return result
    @property
    def max_requests_per_server(self): return self._requests / self._servers
    @property
    def seconds(self): return SECONDS[self._period]

DEFAULT_USAGE_LIMITS = (UsageLimit(10, 'minute'), UsageLimit(1000, 'month'))
USAGE_LIMITS = UsageLimit.get() or DEFAULT_USAGE_LIMITS
THUMBNAIL_USAGE = Database(max([limit.seconds for limit in USAGE_LIMITS]))

class Usage(object):
    def __init__(self, remote_addr):
        self._network = remote_addr[1] + 256 * remote_addr[0]
        self._timestamp = int(time.time())
    def validate(self):
        with THUMBNAIL_USAGE:
            timestamps = THUMBNAIL_USAGE.timestamps(self.network)
            for usage_limit in USAGE_LIMITS:
                usage_limit.validate(self.timestamp, timestamps)
            THUMBNAIL_USAGE.update(self.network, self.timestamp)
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
