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
    def validate(self, request_timestamp, usage_timestamps):
        "Raise a usage limit error if appropriate."
        min_timestamp = request_timestamp - self.seconds if self.seconds else 0
        timestamps = [t for t in usage_timestamps if t >= min_timestamp]
        if len(timestamps) >= self.max_requests_per_server:
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
        self._timestamp = int(time.time())
        self._initialize_remote_addr(remote_addr)
    def validate(self):
        "Update the usage database or raise a usage limit error."
        with USAGE_DATABASE:
            timestamps = USAGE_DATABASE.timestamps(self.remote_addr)
            for rate_limit in RATE_LIMITS:
                rate_limit.validate(self.timestamp, timestamps)
            USAGE_DATABASE.update(self.remote_addr, self.timestamp)
    def _initialize_remote_addr(self, remote_addr):
        self._remote_addr = 0
        for octet in remote_addr.split('.'):
            self._remote_addr = (self._remote_addr << 8) + int(octet)
    @property
    def remote_addr(self):
        "The client's IP address (int)."
        return self._remote_addr
    @property
    def timestamp(self):
        "Unix time, i.e. #seconds since 1-jan-1970."
        return self._timestamp

def validate(request):
    "Raise a usage limit error for this *request* if appropriate."
    Usage(request.remote_addr).validate()
