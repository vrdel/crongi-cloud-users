#!/usr/bin/python

from crongi_cloud_users.identity import IdentityClient
from crongi_cloud_users.log import Logger
from crongi_cloud_users.external import JsonExtend

import argparse
import sys

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
    parser.add_argument('--json-extend', dest='jsonextend')
    args = parser.parse_args()

    identity_client = IdentityClient(logger,
                                     args.user,
                                     args.password,
                                     args.project,
                                     args.projectid,
                                     args.url,
                                     args.memberrole)

    if args.newproject and args.newuser:
        identity_client.update(args.newproject, args.newuser)

    if args.jsonextend:
        f = JsonExtend(logger, args.jsonoverride)
        js = f.get_projects()
        for pr in js:
            project_json = pr['sifra']
            for user_json in pr.get('users'):
                identity_client.update(project_json, user_json['uid'])

main()
