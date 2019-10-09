import urlparse

from crongi_cloud_users.config import parse_config
from crongi_cloud_users.external import JsonExtend
from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.log import Logger

logger = Logger('wsgi-crongi-cloud-users').get()


def admin_client():
    conf = parse_config(logger)
    identity_client = IdentityClient(logger, conf['openstack']['username'],
                                     conf['openstack']['password'],
                                     conf['openstack']['project_name'],
                                     conf['openstack']['project_id'],
                                     conf['openstack']['url'],
                                     conf['openstack']['member_role'])
    return identity_client


def application(environ, start_response):
    location = urlparse.parse_qs(environ['QUERY_STRING'])['target']
    status = '302 Redirect'
    output = b'Redirected to {0}'.format(location)
    client = admin_client()
    user = environ['REMOTE_USER']
    response_headers = [('Location', location[0]),]

    start_response(status, response_headers)

    return [output]
