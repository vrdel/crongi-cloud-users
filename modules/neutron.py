import openstack

from keystoneauth1.identity import v3
from keystoneauth1 import session


class NeutronClient(object):
    def __init__(self, logger, admin_user, admin_password, admin_project, url):
        self.logger = logger
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.admin_project = admin_project
        self.url = url
        self.os_conn = None
        self.neutron_client = None

        self.setup_client()

    def setup_client(self):
        os_conn = openstack.connect(auth_url=self.url,
                                    project_name=self.admin_project,
                                    username=self.admin_user,
                                    password=self.admin_password)
        self.os_conn = os_conn
        self.neutron_client = os_conn.network

    def get_default_securitygroups(self, project_id=None):
        if project_id:
            return self.neutron_client.find_security_group('default', project_id=project_id)
        else:
            return self.os_conn.list_security_groups()
