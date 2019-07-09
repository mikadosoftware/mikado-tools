from sphinx.ext import intersphinx
import warnings
from pprint import pprint as pp

#taken from: https://stackoverflow.com/questions/30939867/how-to-properly-write-cross-references-to-external-documentation-with-intersphin

def fetch_inventory(uri):
    """Read a Sphinx inventory file into a dictionary."""
    class MockConfig(object):
        intersphinx_timeout = None  # type: int
        tls_verify = False

    class MockApp(object):
        srcdir = ''
        config = MockConfig()

        def warn(self, msg):
            warnings.warn(msg)

    return intersphinx.fetch_inventory(MockApp(), '', uri)


uri = '/home/pbrian/projects/weaver/docs/_build/html/objects.inv'

# Read inventory into a dictionary
inv = fetch_inventory(uri)
pp(inv)
