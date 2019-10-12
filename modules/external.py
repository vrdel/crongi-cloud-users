import requests
import json


class ProjectFeed(object):
    interested_user_fields = ['uid']
    interested_project_fields = ['sifra']

    def __init__(self, logger, url, timeout):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            response.raise_for_status()
            self.projects = response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            logger.error('requests error: %s' % e)

        except Exception as e:
            logger.error(e)

    def _filtered_projects(self):
        return filter(lambda p: bool(p['htc']) and bool(p['status_id']), self.projects)

    def _interested_fields(self, projects):
        projects_trim = list()

        for project in projects:
            project_trim = dict()

            projects_users = project['users']
            project_trim['users'] = list()

            for project_key in project.iterkeys():
                if project_key in self.interested_project_fields:
                    project_trim[project_key] = project[project_key]

            for project_user in projects_users:
                for project_user_key in project_user.iterkeys():
                    if project_user_key in self.interested_user_fields:
                        project_trim['users'].append({project_user_key: project_user[project_user_key]})

            projects_trim.append(project_trim)

        return projects_trim

    def get(self):
        return self._interested_fields((self._filtered_projects()))


class JsonProjects(object):
    def __init__(self, logger, jsonfile):
        self.projects = None

        try:
            with open(jsonfile) as fp:
                self.projects = json.load(fp)
        except IOError as e:
            pass

    def get_projects(self):
        return self.projects

