import requests
import json


class ProjectFeed(object):
    def __init__(self, logger, url, timeout):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            response.raise_for_status()
            self.projects = response.json()

        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            logger.error('requests error: %s' % e)

        except Exception as e:
            logger.error(e)

    def get(self):
        return filter(lambda p: bool(p['htc']), self.projects)


class JsonExtend(object):
    def __init__(self, logger, jsonfile):
        self. projects = None

        try:
            with open(jsonfile) as fp:
                self.projects = json.load(fp)
        except IOError as e:
            pass

    def get_projects(self):
        return self.projects
