#!/usr/bin/python

from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.log import Logger
from crongi_cloud_users.external import JsonOverride

import argparse
import sys

def update(logger, identity_client, newproject, newuser):
    project = identity_client.project_exist(newproject)
    if project:
        logger.info('Project exists {0}'.format(project.name))
        user = identity_client.user_exist(newuser)
        if user:
            logger.info('User exists {0}'.format(user.name))
            assigned = identity_client.is_user_assigned(project)
            if not assigned:
                identity_client.user_assigned(user, project)
                logger.info('User {0} assigned to project {1}'.format(user.name, project.name))
            else:
                logger.info('User {0} already assigned to project {1}'.format(user.name, project.name))
        else:
            newuser = identity_client.user_create(newuser, project)
            identity_client.user_assigned(newuser, project)
            logger.info('User {0} assigned to project {1}'.format(newuser.name, project.name))
    else:
        newproject = identity_client.project_create(newproject)
        user = identity_client.user_exist(newuser)
        if user:
            identity_client.user_assigned(user, newproject)
            logger.info('Existing user {0} assigned to project {1}'.format(user.name, newproject.name))
        else:
            newuser = identity_client.user_create(newuser, newproject)
            identity_client.user_assigned(newuser, newproject)
            logger.info('User {0} assigned to project {1}'.format(newuser.name, newproject.name))


def main():
    logger = Logger(sys.argv[0]).get()

    parser = argparse.ArgumentParser(description="crongi-cloud-users client")
    parser.add_argument('--admin-user', required=True, dest='user')
    parser.add_argument('--admin-password', required=True, dest='password')
    parser.add_argument('--admin-project', required=True, dest='project')
    parser.add_argument('--admin-projectid', required=True, dest='projectid')
    parser.add_argument('--admin-url', required=True, dest='url')
    parser.add_argument('--member-role', required=True, dest='memberrole')

    parser.add_argument('--new-user', dest='newuser')
    parser.add_argument('--new-project', dest='newproject')
    parser.add_argument('--json-override', dest='jsonoverride')
    args = parser.parse_args()

    identity_client = IdentityClient(args.user,
                                     args.password,
                                     args.project,
                                     args.projectid,
                                     args.url,
                                     args.memberrole)

    update(logger, identity_client, args.newproject, args.newuser)

    if args.jsonoverride:
        f = JsonOverride(logger, args.jsonoverride)
        js = f.get_projects()
        for pr in js:
            project_json = pr['sifra']
            for user_json in pr.get('users'):
                update(logger, identity_client, project_json, user_json['uid'])

main()
