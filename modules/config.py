import ConfigParser
import sys

conf = '/etc/crongi-cloud-users/cloud-users.conf'


def parse_config(logger=None):
    confopts = dict()

    try:
        config = ConfigParser.ConfigParser()
        if config.read(conf):
            for section in config.sections():
                if section.startswith('settings'):
                    confopts['settings'] = {'api': config.get(section, 'api')}

                    jsonextend = config.get(section, 'jsonextend').strip()
                    confopts['settings'].update({'jsonextend': jsonextend})

                    default_project = config.get(section, 'default_project').strip()
                    confopts['settings'].update({'default_project': default_project})

                    redir_unauthz = config.getboolean(section, 'redirect_to_unauthz')
                    confopts['settings'].update({'redirect_to_unauthz': redir_unauthz})

                if section.startswith('openstack'):
                    projectid = config.get(section, 'project_id').strip()
                    confopts['openstack'] = {'project_id': projectid}

                    projectdomainid = config.get(section, 'project_domain_id').strip()
                    confopts['openstack'].update({'project_domain_id': projectdomainid})

                    projectname = config.get(section, 'project_name').strip()
                    confopts['openstack'].update({'project_name': projectname})

                    userdomainid = config.get(section, 'user_domain_id').strip()
                    confopts['openstack'].update({'user_domain_id': userdomainid})

                    username = config.get(section, 'username').strip()
                    confopts['openstack'].update({'username': username})

                    password = config.get(section, 'password').strip()
                    confopts['openstack'].update({'password': password})

                    url = config.get(section, 'url').strip()
                    confopts['openstack'].update({'url': url})

                    member_role = config.get(section, 'member_role').strip()
                    confopts['openstack'].update({'member_role': member_role})

            return confopts

        else:
            if logger:
                logger.error('Missing %s' % conf)
            else:
                sys.stderr.write('Missing %s\n' % conf)
            raise SystemExit(1)

    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as e:
        if logger:
            logger.error(e)
        else:
            sys.stderr.write('%s\n' % e)
        raise SystemExit(1)

    except (ConfigParser.MissingSectionHeaderError, ConfigParser.ParsingError, SystemExit) as e:
        if getattr(e, 'filename', False):
            if logger:
                logger.error(e.filename + ' is not a valid configuration file')
                logger.error(' '.join(e.args))
            else:
                sys.stderr.write(e.filename + ' is not a valid configuration file\n')
                sys.stderr.write(' '.join(e.args) + '\n')
        raise SystemExit(1)

    return confopts
