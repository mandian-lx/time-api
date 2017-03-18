%{?_javapackages_macros:%_javapackages_macros}

%global oname threeten
Name:          time-api
Version:       0.6.4
Release:       9
Summary:       JSR-310 - Date and Time API
# GPLv2: src-openjdk/main/java/java/util/GregorianCalendar.java
#        src-openjdk/main/java/java/util/Calendar.java
#        src-openjdk/main/java/java/util/Date.java
# Public Domain:  src/main/tzdata/tzdata200*.tar.gz
License:       BSD and GPLv2+ and Public Domain
URL:           http://threeten.github.com/
Source0:       https://github.com/ThreeTen/%{oname}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       %{name}-template-pom.xml
Patch0:        %{name}-0.6.4-dont-compile-openjdk-classes.patch
BuildRequires: java-devel
BuildRequires: jpackage-utils
BuildRequires: javapackages-tools
BuildRequires: maven-local

BuildRequires: ant
BuildRequires: emma
BuildRequires: testng

Requires:      jpackage-utils
BuildArch:     noarch

# https://fedorahosted.org/fpc/ticket/365
#Provides:      bundled(openjdk8-javax-time) = %{version}-%{release}

%description
This JSR will provide a new and improved date and
time API for Java.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{oname}-%{version}

# Use system libraries
sed -i 's|src="${maven.ibiblio.url}/@{group}/@{artifact}/@{version}/@{artifact}-@{version}@{variant}.jar"|src="file:///usr/share/java/@{artifact}.jar"|' build.xml

%patch0 -p0

cp -p %{SOURCE1} pom.xml
sed -i "s|@VERSION@|%{version}|" pom.xml

sed -i 's/\r//' COPYRIGHT-ASSIGN.txt LICENSE.txt LICENSE_OpenJDK.txt LICENSE_Oracle.txt \
 OpenJDKChallenge.txt README.txt RELEASE-NOTES.txt TODO.txt

%build

%mvn_build -f -- -Dproject.build.sourceEncoding=UTF-8


%install

%mvn_install

# https://fedoraproject.org/wiki/Packaging:Java#Packages_providing_APIs
mkdir -p %{buildroot}%{_javadir}/javax.time
ln -sf %{_javadir}/%{name}/%{name}.jar %{buildroot}%{_javadir}/javax.time/

%files -f .mfiles
%{_javadir}/javax.time/%{name}.jar
%doc COPYRIGHT-ASSIGN.txt LICENSE.txt LICENSE_OpenJDK.txt LICENSE_Oracle.txt
%doc OpenJDKChallenge.txt README.txt RELEASE-NOTES.txt TODO.txt

%files javadoc -f .mfiles-javadoc
%doc COPYRIGHT-ASSIGN.txt LICENSE.txt LICENSE_OpenJDK.txt LICENSE_Oracle.txt

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 10 2014 Pete MacKinnon <pmackinn@redhat.com> 0.6.4-6
- changes for xmvn 2.0
- add javapackages-tools, maven-local

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.6.4-4
- Use Requires: java-headless rebuild (#1067528)

* Tue Nov 19 2013 Pete MacKinnon <pmackinn@redhat.com> 0.6.4-3
- add API symlink per review
- added version-release for bundled provides

* Mon Nov 18 2013 Pete MacKinnon <pmackinn@redhat.com> 0.6.4-2
- add fpc notes and virtual provide

* Thu Sep 19 2013 gil cattaneo <puntogil@libero.it> 0.6.4-1
- initial rpm
