from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session


class IdentityClient(object):
    def __init__(self, admin_user, admin_password, admin_project,
                 admin_project_id, url, member_role):
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.admin_project = admin_project
        self.admin_project_id = admin_project_id
        self.url = url
        self.member_role = member_role

        self.setup_client()

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.admin_user,
                           password=self.admin_password,
                           user_domain_id='default',
                           project_id=self.admin_project_id,
                           project_domain_id='Default',
                           project_name=self.admin_project)
        sess = session.Session(auth=auth)
        self.admin_client = client.Client(session=sess, interface='public')
        self.role = self.get_role(self.member_role)

    def get_role(self, name):
        found = filter(lambda r: r.name == name,
                       self.admin_client.roles.list())
        return found[0] if found else None

    def is_user_assigned(self, project):
        users = self.admin_client.users.list(domain='default')
        found = list()
        for u in users:
            # admin does not have primary project
            if u.name == 'admin':
                continue
            if u.default_project_id == project.id:
                found.append(u)
        return bool(found)

    def user_assigned(self, user, project):
        self.admin_client.roles.grant(self.role, user=user, project=project)
        self.admin_client.users.update(user, default_project=project)

    def project_create(self, name):
        new = self.admin_client.projects.create(name, 'default')
        return new

    def user_create(self, name, project):
        new = self.admin_client.users.create(name, default_project=project)
        return new

    def user_exist(self, user):
        found = filter(lambda u: u.name == user, self.admin_client.users.list())
        return found[0] if found else None

    def project_exist(self, project):
        found = filter(lambda p: p.name == project,
                       self.admin_client.projects.list())
        return found[0] if found else None
