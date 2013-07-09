import urllib

from oslo.config import cfg
from webob import exc

from neutron.common import constants
from neutron.common import exceptions
from neutron.openstack.common import log as logging


LOG = logging.getLogger(__name__)


def get_filters(request, attr_info, skips=[]):
    """Extracts the filters from the request string.

Returns a dict of lists for the filters:
check=a&check=b&name=Bob&
becomes:
{'check': [u'a', u'b'], 'name': [u'Bob']}
"""
    res = {}
    for key, values in request.GET.dict_of_lists().iteritems():
        if key in skips:
            continue
        values = [v for v in values if v]
        key_attr_info = attr_info.get(key, {})
        if 'convert_list_to' in key_attr_info:
            values = key_attr_info['convert_list_to'](values)
        elif 'convert_to' in key_attr_info:
            convert_to = key_attr_info['convert_to']
            values = [convert_to(v) for v in values]
        if values:
            res[key] = values
    return res
