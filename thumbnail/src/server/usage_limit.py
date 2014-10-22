"This module enforces our public plan's rate limits."

import platform
import requests
import time

import cfg
import errors
import logger
import tmpdir

from lxml import etree
from usage_database import Database


LINUX = (platform.system() == 'Linux')
SERVERS = 2  # TODO: get this number dynamically

SECONDS = {'minute': 60,
           'hour': 60 * 60,
           'day': 60 * 60 * 24,
           'week': 60 * 60 * 24 * 7,
           'month': 60 * 60 * 24 * 30,
           'year': 60 * 60 * 24 * 365,
           'eternity': None}

class RateLimit(object):
    "We limit usage on a per-period basis."
    def __init__(self, max_requests, period):
        self._requests, self._period = max_requests, period
        self._servers = SERVERS if LINUX else 1
    def __str__(self):
        return "RateLimit({}, '{}')".format(self._requests, self._period)
    def validate(self, timestamp, timestamps):
        "Raise a usage limit error if appropriate."
        min_timestamp = timestamp - self.seconds if self.seconds else 0
        usage_timestamps = [t for t in timestamps if t >= min_timestamp]
        if len(usage_timestamps) >= self.max_requests_per_server:
            raise errors.USAGE_LIMIT_ERROR
    @classmethod
    def max_period(cls, rate_limits):
        "The longest period in *rate_limits* (None if it is 'eternity')."
        periods = [rate_limit.seconds for rate_limit in rate_limits]
        return None if None in periods else max(periods)
    @property
    def max_requests_per_server(self):
        "The usage limit for one server (assumes #servers = 2)."
        return self._requests / self._servers
    @property
    def seconds(self):
        "This rate limit's period (None if it is 'eternity')."
        return SECONDS[self._period]

class PlanLimit(object):
    "A 3scale plan's rate limits retrieved via 3scale's API."
    ADMIN_URL = 'https://datalogics-cloud-admin.3scale.net'
    GET_LIMITS = '/admin/api/application_plans/{}/limits.xml'
    def __init__(self, plan_id=cfg.Configuration.three_scale.public_plan_id):
        url = PlanLimit.ADMIN_URL + PlanLimit.GET_LIMITS.format(plan_id)
        params = {'provider_key': cfg.Configuration.three_scale.provider_key}
        response = requests.get(url, params=params)
        if response.status_code == requests.codes.ok:
            self._rate_limits = self._parse_response(response)
        else:
            self._rate_limits = None
            logger.error('cannot get rate limits for plan {}'.format(plan_id))
    def _parse_response(self, response):
        result = []
        for limit in etree.fromstring(response.text.encode('utf-8')):
            value = limit.xpath('value')[0].text
            period = limit.xpath('period')[0].text
            result.append(RateLimit(int(value), period))
        return result
    @property
    def rate_limits(self):
        "This plan's rate limits."
        return self._rate_limits

DEFAULT_RATE_LIMITS = [RateLimit(10, 'minute'), RateLimit(1000, 'month')]
RATE_LIMITS = PlanLimit().rate_limits or DEFAULT_RATE_LIMITS
USAGE_DATABASE = Database(RateLimit.max_period(RATE_LIMITS))

class Usage(object):
    "This class validates thumbnail server usage."
    def __init__(self, remote_addr):
        self._network = remote_addr[1] + 256 * remote_addr[0]
        self._timestamp = int(time.time())
    def validate(self):
        "Update the usage database or raise a usage limit error."
        with USAGE_DATABASE:
            timestamps = USAGE_DATABASE.timestamps(self.network)
            for rate_limit in RATE_LIMITS:
                rate_limit.validate(self.timestamp, timestamps)
            USAGE_DATABASE.update(self.network, self.timestamp)
    @property
    def network(self):
        "A 'network' is the first two octets of the client's IP address (int)."
        return self._network
    @property
    def timestamp(self):
        "Unix time, i.e. #seconds since 1-jan-1970."
        return self._timestamp

def validate(request):
    "Raise a usage limit error for this *request* if appropriate."
    remote_addr = [int(octet) for octet in request.remote_addr.split('.')]
    if LINUX:
        for private_network in ([127, 0, 0, 1], [10], [192, 168]):
            if private_network == remote_addr[:len(private_network)]:
                return  # monitor requests, etc.
        if remote_addr[0] == 172 and remote_addr[1] in range(16, 32):
            return  # AWS uses this range
    Usage(remote_addr).validate()
