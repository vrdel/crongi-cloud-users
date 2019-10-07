#!/usr/bin/python

import logging
from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session

import argparse


def project_create(client, name):
    new = client.projects.create(name, 'default')
    return new


def user_create(client, name, project):
    new = client.users.create(name, default_project=project)
    return new


def user_exist(client, user):
    found = filter(lambda u: u.name == user, client.users.list())
    return found[0] if found else None


def project_exist(client, project):
    found = filter(lambda p: p.name == project, client.projects.list())
    return found[0] if found else None


def main():
    parser = argparse.ArgumentParser(description="crongi-cloud-users client")
    parser.add_argument('--admin-user', required=True, dest='user')
    parser.add_argument('--admin-password', required=True, dest='password')
    parser.add_argument('--admin-project', required=True, dest='project')
    parser.add_argument('--admin-projectid', required=True, dest='projectid')
    parser.add_argument('--admin-url', required=True, dest='url')

    parser.add_argument('--new-user', dest='newuser')
    parser.add_argument('--new-project', dest='newproject')
    args = parser.parse_args()

    auth = v3.Password(auth_url=args.url,
                       username=args.user,
                       password=args.password,
                       user_domain_id='default',
                       project_id=args.projectid,
                       project_domain_id='Default',
                       project_name=args.project)
    sess = session.Session(auth=auth)
    cl = client.Client(session=sess, interface='public')

    if args.newproject:
        project = project_exist(cl, args.newproject)
        if project:
            print('Project exists {0}'.format(project.name))
            user = user_exist(cl, args.newuser)
            if user:
                print('User exists {0}'.format(user.name))
            else:
                print(user_create(cl, args.newuser, project))
        else:
            newproject = project_create(cl, args.newproject)
            print(user_create(cl, args.newuser, newproject))

main()
