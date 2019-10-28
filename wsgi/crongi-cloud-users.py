import urlparse

from crongi_cloud_users.config import parse_config
from crongi_cloud_users.external import JsonProjects, ProjectFeed
from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.neutron import NeutronClient
from crongi_cloud_users.log import Logger

logger = Logger('wsgi-crongi-cloud-users').get()
conf = parse_config(logger)

def neutron_client():
    neutron_client = NeutronClient(logger, conf['openstack']['username'],
                                   conf['openstack']['password'],
                                   conf['openstack']['project_name'],
                                   conf['openstack']['project_id'],
                                   conf['openstack']['url'])

    return neutron_client


def identity_client():
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

    keystone = identity_client()
    neutron = neutron_client()
    projects = ProjectFeed(logger, conf['settings']['api'], 60).get()
    json_projects = JsonProjects(logger, conf['settings']['jsonextend']).get_projects()

    if projects and json_projects:
        projects.update(json_projects)

    user_found_project = None
    for id, users in projects.iteritems():
        for user in users:
            if shibboleth_user == user['uid']:
                keystone.update(id, shibboleth_user)
                project_id = keystone.get_last_projectid()
                sec_group = neutron.get_default_securitygroup(project_id=project_id)
                if len(sec_group.security_group_rules) < 8:
                    neutron.create_default_rules(sec_group.id)
                user_found_project = True

    if not user_found_project and not conf['settings']['redirect_to_unauthz']:
        target = urlparse.parse_qs(environ['QUERY_STRING'])['target']
        keystone.update(conf['settings']['default_project'], shibboleth_user)
        project_id = keystone.get_last_projectid()
        sec_group = neutron.get_default_securitygroup(project_id=project_id)
        if len(sec_group.security_group_rules) < 8:
            neutron.create_default_rules(sec_group.id)
        output = redirect(start_response, target)

    elif user_found_project:
        target = urlparse.parse_qs(environ['QUERY_STRING'])['target']
        output = redirect(start_response, target)

    else:
        target = ['/crongiusers-unauthz']
        output = redirect(start_response, target)

    return [output]
