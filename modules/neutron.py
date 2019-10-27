from neutronclient.v2_0 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session


class NeutronClient(object):
    def __init__(self, logger, admin_user, admin_password, admin_project,
                 admin_project_id, url):
        self.logger = logger
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.admin_project = admin_project
        self.admin_project_id = admin_project_id
        self.url = url

        self.setup_client()

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.admin_user,
                           password=self.admin_password,
                           user_domain_id='default',
                           project_id=self.admin_project_id,
                           project_domain_id='Default',
                           project_name=self.admin_project)
        sess = session.Session(auth=auth)
        self.neutron_client = client.Client(session=sess, interface='public')

    def create_default_securitygroup(self, project_id):
        body = dict()
        body['name'] = 'default'
        body['description'] = 'Default security group'
        body['tenant_id'] = project_id
        self.neutron_client.create_security_group(body)

    def get_securitygroups(self, project_id=None):
        if project_id:
            return self.neutron_client.list_security_groups(project_id=project_id)['security_groups']
        else:
            return self.neutron_client.list_security_groups()['security_groups']
