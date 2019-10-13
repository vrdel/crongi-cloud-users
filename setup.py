from distutils.core import setup
import glob

NAME='crongi-cloud-users'

def get_ver():
    try:
        for line in open(NAME+'.spec'):
            if "Version:" in line:
                return line.split()[1]
    except IOError:
        print "Make sure that %s is in directory"  % (NAME+'.spec')
        raise SystemExit(1)


setup(name=NAME,
      version=get_ver(),
      author='SRCE',
      author_email='dvrcic@srce.hr',
      description='WSGI application that assign HTC Cloud CRO-NGI users to Openstack projects',
      url='https://github.com/vrdel/crongi-cloud-users',
      package_dir={'crongi_cloud_users': 'modules/'},
      packages=['crongi_cloud_users'],
      data_files=[('/etc/%s' % NAME, ['config/cloud-users.conf', 'config/projects.json']),
                  ('/var/www/', ['wsgi/crongi-cloud-users.py'])])
