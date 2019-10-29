#!/usr/bin/python

from crongi_cloud_users.config import parse_config
from crongi_cloud_users.external import JsonProjects, ProjectFeed
from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.neutron import NeutronClient
from crongi_cloud_users.log import Logger

import argparse
import sys
import pprint


def main():
    logger = Logger(sys.argv[0]).get()

    parser = argparse.ArgumentParser(description="crongi-cloud-users client")
    parser.add_argument('--load-config', action='store_true', default=False, dest='loadconfig')

    parser.add_argument('--admin-user', dest='user')
    parser.add_argument('--admin-password', dest='password')
    parser.add_argument('--admin-project', dest='project')
    parser.add_argument('--admin-projectid', dest='projectid')
    parser.add_argument('--admin-url', dest='url')
    parser.add_argument('--member-role', dest='memberrole')

    parser.add_argument('--new-user', dest='newuser')
    parser.add_argument('--new-project', dest='newproject')
    parser.add_argument('--projects-url', dest='projectsurl')
    parser.add_argument('--json-extend', dest='jsonextend')

    parser.add_argument('--find-user', dest='finduser')

    args = parser.parse_args()

    projects = None

    if args.loadconfig:
        conf = parse_config(logger)
        identity_client = IdentityClient(logger, conf['openstack']['username'],
                                         conf['openstack']['password'],
                                         conf['openstack']['project_name'],
                                         conf['openstack']['project_id'],
                                         conf['openstack']['url'],
                                         conf['openstack']['member_role'])
        neutron_client = NeutronClient(logger, conf['openstack']['username'],
                                       conf['openstack']['password'],
                                       conf['openstack']['project_name'],
                                       conf['openstack']['project_id'],
                                       conf['openstack']['url'])
    elif not args.loadconfig:
        for a in ['user', 'password', 'project', 'projectid', 'url',
                  'memberrole']:
            if not getattr(args, a, False):
                logger.error('Missing {}'.format(a))
                raise SystemExit(1)

        identity_client = IdentityClient(logger, args.user, args.password,
                                         args.project, args.projectid,
                                         args.url, args.memberrole)
        neutron_client = NeutronClient(logger, args.user, args.password,
                                       args.project, args.projectid, args.url)

    project_feed = ProjectFeed(logger, args.projectsurl, 60)

    if args.projectsurl:
        projects = project_feed.get_projects()

    users_lastpr = project_feed.get_userlastprojects()

    if args.newproject and args.newuser:
        identity_client.update(args.newproject, args.newuser, True)
        project_id = identity_client.get_last_projectid()
        sec_group = neutron_client.get_default_securitygroup(project_id=project_id)
        if len(sec_group.security_group_rules) < 8:
            neutron_client.create_default_rules(sec_group.id)

    if args.jsonextend:
        f = JsonProjects(logger, args.jsonextend)
        js = f.get_projects()
        if projects and js:
            projects.update(js)
            for id, users in projects.iteritems():
                for user in users:
                    lastpr = users_lastpr[user['uid']]
                    identity_client.update(id, user['uid'], lastpr == id)
                    project_id = identity_client.get_last_projectid()
                    sec_group = neutron_client.get_default_securitygroup(project_id=project_id)
                    if len(sec_group.security_group_rules) < 8:
                        neutron_client.create_default_rules(sec_group.id)
        elif js:
            for id, users in js.iteritems():
                for user in users:
                    identity_client.update(id, user['uid'])
                    project_id = identity_client.get_last_projectid()
                    sec_group = neutron_client.get_default_securitygroup(project_id=project_id)
                    if len(sec_group.security_group_rules) < 8:
                        neutron_client.create_default_rules(sec_group.id)

    if args.finduser:
        for id, users in projects.iteritems():
            for user in users:
                if args.finduser == user['uid']:
                    print("User {0} found in {1} project".format(args.finduser, id))
main()
