#!/usr/bin/python

import logging
from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session

import argparse

def main():

    parser = argparse.ArgumentParser(description="crongi-cloud-users client")
    parser.add_argument('--keystone-user', required=True, dest='user')
    parser.add_argument('--keystone-password', required=True, dest='password')
    parser.add_argument('--keystone-project', required=True, dest='project')
    parser.add_argument('--keystone-url', required=True, dest='url')
    args = parser.parse_args()

    auth = v3.Password(auth_url=args.url,
                       username=args.user,
                       password=args.password,
                       user_domain_id='default',
                       project_id='5f7439af65e44171aa18a205cd90e5b9',
                       project_domain_id='Default',
                       project_name=args.project)
    sess = session.Session(auth=auth)
    print(sess.get_token())
    print(sess.get_user_id())
    cl = client.Client(session=sess, interface='public')
    print(cl.projects.list())
    print(cl.users.list())

main()
