from openstack import connection

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
        self.os_conn = None
        self.neutron_client = None

        self.setup_client()

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.admin_user,
                           password=self.admin_password,
                           user_domain_id='default',
                           project_id=self.admin_project_id,
                           project_domain_id='Default',
                           project_name=self.admin_project)
        sess = session.Session(auth=auth)
        os_conn = connection.Connection(session=sess,
                                        identity_interface='public')
        self.os_conn = os_conn
        self.neutron_client = os_conn.network

    def get_default_securitygroup(self, project_id=None):
        if project_id:
            return self.neutron_client.find_security_group('default', project_id=project_id)
        else:
            return self.os_conn.list_security_groups()

    def create_default_rules(self, security_group_id):
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=3389,
            port_range_min=3389,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=22,
            port_range_min=22,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='icmp',
            ethertype='IPv4',
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=443,
            port_range_min=443,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=8443,
            port_range_min=8443,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=8000,
            port_range_min=8000,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=53,
            port_range_min=53,
        )
        rule = self.neutron_client.create_security_group_rule(
            security_group_id=security_group_id,
            direction='ingress',
            remote_ip_prefix='0.0.0.0/0',
            protocol='tcp',
            ethertype='IPv4',
            port_range_max=80,
            port_range_min=80,
        )
