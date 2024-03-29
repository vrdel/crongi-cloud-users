from keystoneclient.v3 import client
from keystoneauth1.identity import v3
from keystoneauth1 import session


class IdentityClient(object):
    def __init__(self, logger, admin_user, admin_password, admin_project,
                 admin_project_id, url, member_role):
        self.logger = logger
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.admin_project = admin_project
        self.admin_project_id = admin_project_id
        self.url = url
        self.member_role = member_role
        self.project_id = None

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

    def is_user_assigned(self, user, project):
        return bool(self.admin_client.\
                    role_assignments.list(project=project.id,
                                          user=user.id,
                                          role=self.role))

    def user_assigned(self, user, project):
        self.admin_client.roles.grant(self.role, user=user, project=project)
        self.admin_client.users.update(user, default_project=project)

    def project_create(self, name):
        new = self.admin_client.projects.create(name, 'default')
        self.project_id = new.id
        return new

    def set_default_project(self, user, project):
        self.admin_client.users.update(user, default_project=project)
        self.logger.info('User {0} default project {1}'.format(user.name, project.name))

    def user_create(self, name, project):
        new = self.admin_client.users.create(name, default_project=project)
        return new

    def get_last_projectid(self):
        return self.project_id

    def user_exist(self, user):
        found = filter(lambda u: u.name == user, self.admin_client.users.list())
        return found[0] if found else None

    def project_exist(self, project):
        found = filter(lambda p: p.name == project,
                       self.admin_client.projects.list())
        if found:
            self.project_id = found[0].id
        return found[0] if found else None

    def update(self, newproject, newuser, last_project=False):
        project = self.project_exist(newproject)
        if project:
            self.logger.info('Project exists {0}'.format(project.name))
            user = self.user_exist(newuser)
            if user:
                self.logger.info('User exists {0}'.format(user.name))
                assigned = self.is_user_assigned(user, project)
                if not assigned:
                    self.user_assigned(user, project)
                    self.logger.info('User {0} assigned to project {1}'.format(user.name, project.name))
                else:
                    self.logger.info('User {0} already assigned to project {1}'.format(user.name, project.name))

                if last_project:
                    self.set_default_project(user, project)
            else:
                newuser = self.user_create(newuser, project)
                self.user_assigned(newuser, project)
                self.logger.info('User {0} assigned to project {1}'.format(newuser.name, project.name))
                if last_project:
                    self.set_default_project(newuser, project)
        else:
            newproject = self.project_create(newproject)
            user = self.user_exist(newuser)
            if user:
                self.user_assigned(user, newproject)
                self.logger.info('Existing user {0} assigned to project {1}'.format(user.name, newproject.name))
                if last_project:
                    self.set_default_project(user, newproject)
            else:
                newuser = self.user_create(newuser, newproject)
                self.user_assigned(newuser, newproject)
                self.logger.info('User {0} assigned to project {1}'.format(newuser.name, newproject.name))
                if last_project:
                    self.set_default_project(newuser, newproject)
