%global scl_name_base    perl
%global scl_name_version 516
%global scl %{scl_name_base}%{scl_name_version}
%scl_package %scl

%global install_scl 1

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary: Package that installs %scl
Name:    %scl_name
Version: 1.1
Release: 3%{?dist}
License: GPLv2+
Source0: macro-build
Source1: perl.prov.stack
Source2: perl.req.stack
Source3: perl.attr
Source4: perllib.attr
Source5: README
Source6: LICENSE
BuildRequires: help2man

%if 0%{?install_scl}
Requires: %{scl_prefix}perl
%endif
BuildRequires: scl-utils-build
BuildRequires: iso-codes

%description
This is the main package for %scl Software Collection.

%package runtime
Summary:  Package that handles %scl Software Collection
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary:  Package shipping basic build configuration
Requires: scl-utils-build
Requires: %{name}-scldevel = %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.

%prep
%setup -c -T

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE5})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE6} .

%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_scl_scripts}/root
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF
%scl_install

# Add the aditional macros to macros.%%{scl}-config
cat %{SOURCE0} >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config
sed -i 's|@SCL@|%{scl}|g' %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

install -D -m 755 %{SOURCE1} %{buildroot}%{_root_prefix}/lib/rpm/perl.prov.stack
install -D -m 755 %{SOURCE2} %{buildroot}%{_root_prefix}/lib/rpm/perl.req.stack
sed -i 's|__SCL_NAME__|%{scl}-perl|g' %{buildroot}%{_root_prefix}/lib/rpm/perl.prov.stack
sed -i 's|__SCL_NAME__|%{scl}-perl|g' %{buildroot}%{_root_prefix}/lib/rpm/perl.req.stack

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
mkdir -p %{buildroot}/usr/lib/rpm/fileattrs/
install -m 644 %{SOURCE3} %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/perl.attr
install -m 644 %{SOURCE4} %{buildroot}%{_root_prefix}/lib/rpm/fileattrs/perllib.attr
%endif

# install generated man page
mkdir -p %{buildroot}%{_mandir}/man7/
install -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%files

%files runtime -f filesystem
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
%{_root_prefix}/lib/rpm/perl.req.stack
%{_root_prefix}/lib/rpm/perl.prov.stack
%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%{_root_prefix}/lib/rpm/fileattrs/perl.attr
%{_root_prefix}/lib/rpm/fileattrs/perllib.attr
%endif

%changelog
* Fri Mar 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-3
- Wrong macro in README
- Resolves: rhbz#1061453

* Tue Mar 25 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-2
- Use "-f filesystem" for files section of -runtime on RHEL 7
- Resolves: rhbz#1079938

* Mon Feb 17 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.1-1
- Introduce README and LICENSE.
- Change version to 1.1.
- Resolves: rhbz#1061453

* Wed Feb 05 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-21
- Update dependencies of sub-package build
- Resolves: rhbz#1063206

* Mon Jan 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-20
- Changed name of sub-package devel to scldevel
- Added the file macros.%%{scl_name_base}-scldevel
- Resolves: rhbz#1055580

* Mon Jan 20 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-19
- Rebuilt against new scl-utils
- Resolves: rhbz#1054726

* Tue Jan 14 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-18
- Moved perl.(prov|req).stack and file*.attr to sub-package devel
- Resolves: rhbz#1052183

* Wed Jan 08 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1-17
- Define macros for tests sub-package
- Resolves: rhbz#1049366

* Mon Nov 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-16
- Disable macro perl_bootstrap

* Tue Nov 12 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-15
- Enable macro perl_bootstrap

* Mon Nov 04 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-14
- Override %%__pkgconfig_path to solve problems with invalid perl provides

* Wed Oct 30 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-13
- Update %%scl_package_override

* Wed Oct 30 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-12
- Define %%prep section
- Create macro-build

* Mon Jun 17 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-11
- Disable macro perl_bootstrap

* Thu May 23 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-10
- Update definition of MANPATH (rhbz#966388)

* Tue May 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-9
- Do not remove /opt/rh/perl516 to prevent removing of any user data

* Mon May 13 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-8
- Remove the directory /opt/rh/perl516 after uninstalling rpm (rhbz#956215)

* Sun Apr 28 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-7
- Remove extra colon from path definition

* Thu Apr 25 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1-6
- Update setting of environment variable in the script enable

* Wed Feb  6 2013 Jitka Plesnikova <jplesnik@redhat.com> 1-5
- enable macro perl_bootstrap

* Fri Oct  5 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-4
- update to new version of Perl 5.16
- package perl.{prov,req}.stack as executables

* Mon Jul 23 2012 Marcela Mašláňová <mmaslano@redhat.com> 1-3
- change permission from 700 to 644 on perl.{prov,req}

* Tue Mar  6 2012 Marcela Mašláňová <mmaslano@redhat.com> 1.2
- fix dependency on collection *-runtime

* Tue Dec 06 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.1
- initial packaging of meta perl514 package
