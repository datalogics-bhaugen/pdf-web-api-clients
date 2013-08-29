import simplejson


def parse(logger, s, default=None):
    try:
        return simplejson.loads(s)
    except Exception: 
        logger.error('cannot parse %s' % s)
        return default

