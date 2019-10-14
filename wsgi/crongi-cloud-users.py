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


def redirect(start_response, target):
    status = '302 Redirect'
    output = b'Redirected to {0}'.format(target)
    response_headers = [('Location', target[0]),]
    start_response(status, response_headers)

    return output


def application(environ, start_response):
    target, output = None, None
    shibboleth_user = environ['REMOTE_USER']

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

    if not user_found_project and not conf['settings']['redirect_to_unauthz']:
        target = urlparse.parse_qs(environ['QUERY_STRING'])['target']
        client.update(conf['settings']['default_project'], shibboleth_user)
        output = redirect(start_response, target)

    elif user_found_project:
        target = urlparse.parse_qs(environ['QUERY_STRING'])['target']
        output = redirect(start_response, target)

    else:
        target = ['/crongiusers-unauthz']
        output = redirect(start_response, target)

    return [output]
