import urlparse

from crongi_cloud_users.config import parse_config
from crongi_cloud_users.external import JsonProjects, ProjectFeed
from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.log import Logger

logger = Logger('wsgi-crongi-cloud-users').get()
conf = parse_config(logger)


def admin_client():
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
    shibboleth_user = environ['REMOTE_USER']
    response_headers = [('Location', location[0]),]

    client = admin_client()
    projects = ProjectFeed(logger, conf['settings']['api'], 60).get()
    json_projects = JsonProjects(logger, conf['settings']['jsonextend']).get_projects()

    if projects and json_projects:
        projects.update(json_projects)

    user_found_project = None
    for id, users in projects.iteritems():
        for user in users:
            if shibboleth_user == user['uid']:
                client.update(id, shibboleth_user)
                user_found_project = True

    if not user_found_project:
        client.update(conf['settings']['default_project'], shibboleth_user)

    start_response(status, response_headers)

    return [output]
