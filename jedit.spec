%define name    jedit
%define version 4.3.1
%define release %mkrel 1

Name:           %{name}
Version:        %{version}
Release:        %{release}

Summary:        Programmer's Text Editor Written in Java
URL:            http://www.jedit.org
Group:          Editors

Source0:        %{name}%{version}source.tar.bz2
# compressed jar to avoid a warning with rpmlint
Patch0:         compressed-jars.patch
Patch1:         fix-doc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        GPLv2+

BuildArch:      noarch

BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-nodeps
# to build the docs-html target
BuildRequires:  docbook-dtd44-xml
BuildRequires:  docbook-style-xsl

Requires:       java >= 1.5

%description
jEdit is an Open Source, cross platform text editor written in Java. It
has an extensive feature set that includes syntax highlighting, auto indent,
folding, word wrap, abbreviation expansion, multiple clipboards, powerful 
search and replace, and much more.

jEdit is extremely customizable, and extensible, using either macros
written in the BeanShell scripting language, or plugins written in Java.

%prep
%setup -q -n jEdit
%patch0 -p1
%patch1 -p0

%build
export CLASSPATH="."
%ant build dist-java

%install
rm -rf $RPM_BUILD_ROOT

# Automatic mode
cd dist
java -jar %{name}%{version}install.jar auto $RPM_BUILD_ROOT%{_datadir}/%{name}/%{version} unix-script=. unix-man=$RPM_BUILD_ROOT%{_mandir}/man1/
cd ..

%__install -d $RPM_BUILD_ROOT%{_bindir}

cat > $RPM_BUILD_ROOT%{_bindir}/%{name} <<EOF
#!/bin/sh

java -jar %{_datadir}/%{name}/%{version}/jedit.jar

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files

%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/%{name}/%{version}/*
%{_mandir}/man1/jedit.1*

