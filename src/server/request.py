import simplejson

from errors import Error, ErrorCode


class JSON:
    "JSON encoding and parsing utilities."
    class RequestData(dict):
        "Extract request form data (supports jQuery form data encoding)."
        def parse(self, request_form, part_name):
            prefix = u'{}['.format(part_name)
            for key, value in request_form.items():
                if key.startswith(prefix): self[key[len(prefix):-1]] = value
            self.update(JSON.loads(request_form.get(part_name, u'{}')))
    @classmethod
    def request_data(cls, request_form, part_name):
        result = JSON.RequestData()
        result.parse(request_form, part_name)
        return result
    @classmethod
    def dumps(cls, obj):
        try:
            return simplejson.dumps(obj, sort_keys=True)
        except Exception:
            error = u'cannot encode {}'.format(obj)
            raise Error(ErrorCode.InvalidSyntax, error)
    @classmethod
    def loads(cls, s):
        try:
            return simplejson.loads(s)
        except Exception:
            error = u'cannot parse {}'.format(s)
            raise Error(ErrorCode.InvalidSyntax, error)
