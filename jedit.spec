%define name    jedit
%define version 4.3.1
%define release %mkrel 2

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
BuildRequires:  xsltproc 
Requires:       java >= 1.5

%description
jEdit is an Open Source, cross platform text editor written in Java. It
has an extensive feature set that includes syntax highlighting, auto indent,
folding, word wrap, abbreviation expansion, multiple clipboards, powerful 
search and replace, and much more.

jEdit is extremely customizable, and extensible, using either macros
written in the BeanShell scripting language, or plugins written in Java.

%files
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-server
%defattr(-,root,root,-)
%{_datadir}/%{name}/%{version}/*
%{_mandir}/man1/jedit.1*
%{_datadir}/pixmaps/%{name}.png
%{_desktopdir}/%{name}.desktop

#--------------------------------------------------------------------

%package javadoc
Summary: Javadoc for jEdit
Group: Development/Java

%description javadoc
Javadoc for jEdit.

%files javadoc
%defattr(-,root,root,-)
%_javadocdir/*

#--------------------------------------------------------------------

%prep
%setup -q -n jEdit
%patch0 -p1
%patch1 -p0

%build
export CLASSPATH="."
%ant build userdocs

%install
rm -rf %{buildroot}

# javadoc
%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
mv  build/doc/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%_javadocdir/%{name}

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/%{version}/
# some cleanin'
rm -rf build/classes/
# install
cp -r build/* %{buildroot}%{_datadir}/%{name}/%{version}/

# script
%__install -dm 755 %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh
java -jar %{_datadir}/%{name}/%{version}/jedit.jar
EOF

# script server
cat > %{buildroot}%{_bindir}/%{name}-server <<EOF
#!/bin/sh
jedit -nogui -background
EOF

# icons
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 icons/%{name}-icon48.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

# desktopfile
%__install -dm 755 %{buildroot}%{_desktopdir}
cat > %{buildroot}%{_desktopdir}/%{name}.desktop << EOF
[Desktop Entry]
Name=jEdit Text Editor
Comment=Edit text files
GenericName=Text Editor
Exec=%{name} %U
Icon=%{name}
Terminal=false
Type=Application
Categories=Development;TextEditor;
EOF

# manpage
%__install -dm 755 %{buildroot}%{_mandir}/man1/
%__install -m 644 package-files/linux/%{name}.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

