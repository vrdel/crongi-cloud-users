%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%define underscore() %(echo %1 | sed 's/-/_/g')
%define stripc() %(echo %1 | sed 's/el7.centos/el7/')
%define mydist %{stripc %{dist}}

Name:           crongi-cloud-users
Version:        0.1.4
Release:        1%{?mydist}.srce
Summary:        WSGI application that assign HTC Cloud CRO-NGI users to Openstack projects 
Group:          Applications/System
License:        GPL
URL:            https://github.com/vrdel/crongi-cloud-users
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch 
BuildRequires:  python2-devel
Requires:       python2-keystoneclient


%description
WSGI application that assign HTC Cloud CRO-NGI users to Openstack projects

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory --mode 755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%dir %{_sysconfdir}/%{name}/
%{python_sitelib}/%{underscore %{name}}/*.pyo
%attr(0755,keystone,kolla) %dir %{_localstatedir}/log/%{name}/
%{_localstatedir}/www/crongi-cloud-users.py[oc]

%changelog
* Tue Oct 29 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.4-1%{?dist}
- fix associations of users with multiple projects
- last submitted project for user is default_project
- explicit project_id for default security group rules
* Tue Oct 29 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.3-3%{?dist}
- add slipped neutron module changes 
* Mon Oct 28 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.3-2%{?dist}
- fix NeutronClient import
* Mon Oct 28 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.3-1%{?dist}
- create default security rules for new projects
- consider also projects with htc=2
* Mon Oct 14 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.2-2%{?dist}
- fix parsing of active users and projects
* Mon Oct 14 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.2-1%{?dist}
- selective redirect to unauthz page 
* Sat Oct 12 2019 Daniel Vrcic <dvrcic@srce.hr> - 0.1.1-1%{?dist}
- initial version
