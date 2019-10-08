#!/usr/bin/python

import logging
from crongi_cloud_users.identity import IdentityClient

import argparse


def main():
    parser = argparse.ArgumentParser(description="crongi-cloud-users client")
    parser.add_argument('--admin-user', required=True, dest='user')
    parser.add_argument('--admin-password', required=True, dest='password')
    parser.add_argument('--admin-project', required=True, dest='project')
    parser.add_argument('--admin-projectid', required=True, dest='projectid')
    parser.add_argument('--admin-url', required=True, dest='url')
    parser.add_argument('--member-role', required=True, dest='memberrole')

    parser.add_argument('--new-user', dest='newuser')
    parser.add_argument('--new-project', dest='newproject')
    args = parser.parse_args()

    identity_client = IdentityClient(args.user,
                                     args.password,
                                     args.project,
                                     args.projectid,
                                     args.url,
                                     args.memberrole)

    if args.newproject:
        project = identity_client.project_exist(args.newproject)
        if project:
            print('Project exists {0}'.format(project.name))
            user = identity_client.user_exist(args.newuser)
            if user:
                print('User exists {0}'.format(user.name))
                assigned = identity_client.is_user_assigned(project)
                if not assigned:
                    identity_client.user_assigned(user, project)
                    print('User {0} assigned to project {1}'.format(user.name, project.name))
                else:
                    print('User {0} already assigned to project {1}'.format(user.name, project.name))
            else:
                newuser = identity_client.user_create(args.newuser, project)
                identity_client.user_assigned(newuser, project)
                print('User {0} assigned to project {1}'.format(newuser.name, project.name))
        else:
            newproject = identity_client.project_create(args.newproject)
            user = identity_client.user_exist(args.newuser)
            if user:
                identity_client.user_assigned(user, newproject)
                print('Existing user {0} assigned to project {1}'.format(user.name, newproject.name))
            else:
                newuser = identity_client.user_create(args.newuser, newproject)
                identity_client.user_assigned(newuser, newproject)
                print('User {0} assigned to project {1}'.format(newuser.name, newproject.name))


main()
