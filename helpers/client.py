#!/usr/bin/python

from crongi_cloud_users.config import parse_config
from crongi_cloud_users.external import JsonProjects, ProjectFeed
from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.log import Logger

import argparse
import sys

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
    args = parser.parse_args()

    if args.loadconfig:
        conf = parse_config(logger)
        identity_client = IdentityClient(logger, conf['openstack']['username'],
                                         conf['openstack']['password'],
                                         conf['openstack']['project_name'],
                                         conf['openstack']['project_id'],
                                         conf['openstack']['url'],
                                         conf['openstack']['member_role'])
    elif not args.loadconfig:
        for a in ['user', 'password', 'project', 'projectid', 'url',
                  'memberrole']:
            if not getattr(args, a, False):
                logger.error('Missing {}'.format(a))
                raise SystemExit(1)

        identity_client = IdentityClient(logger, args.user, args.password,
                                         args.project, args.projectid,
                                         args.url, args.memberrole)

    if args.newproject and args.newuser:
        identity_client.update(args.newproject, args.newuser)

    if args.projectsurl:
        projects = ProjectFeed(logger, args.projectsurl, 60).get()

    if args.jsonextend:
        f = JsonProjects(logger, args.jsonextend)
        js = f.get_projects()
        for pr in js:
            project_json = pr['sifra']
            for user_json in pr.get('users'):
                identity_client.update(project_json, user_json['uid'])

main()
