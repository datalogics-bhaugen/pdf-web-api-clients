"JSON utilities. (The built-in JSON module complicates naming this module.)"

import simplejson

from errors import Error, ErrorCode


class JSON:
    "JSON encoding and parsing utilities."
    class RequestData(dict):
        "Extract request form data (supports jQuery form part encoding)."
        def parse(self, request_form, part_name):
            "Initialize with *part_name* data."
            prefix = u'{}['.format(part_name)
            for key, value in request_form.items():
                if key.startswith(prefix): self[key[len(prefix):-1]] = value
            self.update(JSON.loads(request_form.get(part_name, u'{}')))
    @classmethod
    def request_data(cls, request_form, part_name):
        "Return :py:class:`RequestData` for *part_name* from *request_form*."
        result = JSON.RequestData()
        result.parse(request_form, part_name)
        return result
    @classmethod
    def dumps(cls, obj):
        "Return JSON encoding for *obj*, raise :py:class:`~.Error` if unable."
        try:
            return simplejson.dumps(obj, sort_keys=True)
        except Exception:
            error = u'cannot encode {}'.format(obj)
            raise Error(ErrorCode.InvalidSyntax, error)
    @classmethod
    def loads(cls, s):
        "Return object for decoded JSON, raise :py:class:`~.Error` if unable."
        try:
            return simplejson.loads(s)
        except Exception:
            error = u'cannot parse {}'.format(s)
            raise Error(ErrorCode.InvalidSyntax, error)
