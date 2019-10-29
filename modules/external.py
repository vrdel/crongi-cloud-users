from collections import OrderedDict
from datetime import datetime

import requests
import json


class ProjectFeed(object):
    interested_user_fields = ['uid']
    interested_project_fields = ['sifra', 'date_from']

    def __init__(self, logger, url, timeout):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            response.raise_for_status()
            self.projects = response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            logger.error('requests error: %s' % e)

        except Exception as e:
            logger.error(e)

    def _filtered_projects(self, projects):
        return filter(lambda p: (p['htc'] == 1 or p['htc'] == 2) and p['status_id'] == 1, projects)

    def _interested_fields(self, projects):
        projects_unsorted = list()

        for project in projects:
            project_trim = dict()

            projects_users = project['users']
            project_trim['users'] = list()

            for project_key in project.iterkeys():
                if project_key in self.interested_project_fields:
                    project_trim[project_key] = project[project_key]

            for project_user in projects_users:
                for project_user_key in project_user.iterkeys():
                    if (project_user_key in self.interested_user_fields
                        and project_user['status_id'] == 1):
                        project_trim['users'].append({project_user_key: project_user[project_user_key]})

            project_trim['date_from'] = datetime.strptime(project_trim['date_from'], '%Y-%m-%d')

            projects_unsorted.append(project_trim)

        return projects_unsorted

    def _sort(self, projects):
        return sorted(projects, key=lambda p: p['date_from'])

    def get_projects(self):
        flat = OrderedDict()
        for d in self._sort(self._interested_fields((self._filtered_projects(self.projects)))):
            flat[d['sifra']] = d['users']
        return flat

    def get_userlastprojects(self):
        users = dict()
        projects = self.get_projects()
        for k, v in projects.iteritems():
            for u in v:
                users[u['uid']] = k
        return users


class JsonProjects(object):
    def __init__(self, logger, jsonfile):
        self.projects = None

        try:
            with open(jsonfile) as fp:
                self.projects = json.load(fp)
        except IOError as e:
            pass

    def get_projects(self):
        projects_d = dict()

        for project in self.projects:
            projects_d[project['sifra']] = project['users']

        return projects_d
