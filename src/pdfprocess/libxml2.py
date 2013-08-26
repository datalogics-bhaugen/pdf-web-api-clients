'''
this lxml wrapper implements the subset of libxml2 used by ThreeScalePY,
because libxml2 is (a) quite old, and (b) not buildout-friendly.
'''


from lxml import etree


parserError = etree.Error

class Element(object):
    def __init__(self, impl):
        self._impl = impl
    def getContent(self):
        try: return self._impl.text
        except AttributeError: return str(self._impl)
    def xpathEval(self, path):
        return [Element(impl) for impl in self._impl.xpath(path)]

def parseDoc(xml):
    return Element(etree.fromstring(xml))

