"lxml wrapper supports subset of libxml2 interface used by ThreeScalePY"

from lxml import etree


parserError = etree.Error

class Element(object):
    def __init__(self, element):
        self._element = element
    def getContent(self):
        return self._element.text

class Root(object):
    def __init__(self, root):
        self._root = root
    def xpathEval(self, path):
        return [Element(element) for element in self._root.xpath(path)]

def parseDoc(xml):
    return Root(etree.fromstring(xml))

