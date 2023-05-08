# Supported tagrets: el9
# SPEC file based on Fedora 38
# Note: wordview is packaged in /usr/share/catdoc to avoid a dependency on tk

Name: catdoc
Version: 0.95
Release: 1%{?dist}.zenetys
Summary: A program which converts Microsoft office files to plain text
License: GPLv2
URL: http://www.wagner.pp.ru/~vitus/software/catdoc/
Source0: http://ftp.wagner.pp.ru/pub/catdoc/%{name}-%{version}.tar.gz

Patch0: https://src.fedoraproject.org/rpms/catdoc/raw/36561c9a150c2b31c27f4ce0a5a24676c5206903/f/makefilefix.patch
Patch1: https://sources.debian.org/data/main/c/catdoc/1%3A0.95-4.1/debian/patches/01-amd64_fixes.patch
Patch2: https://sources.debian.org/data/main/c/catdoc/1%3A0.95-4.1/debian/patches/03-Type_fixes.patch
Patch3: https://sources.debian.org/data/main/c/catdoc/1%3A0.95-4.1/debian/patches/04-XLS_parsing_improvements.patch
Patch4: https://sources.debian.org/data/main/c/catdoc/1%3A0.95-4.1/debian/patches/05-CVE-2017-11110.patch
Patch5: https://sources.debian.org/data/main/c/catdoc/1%3A0.95-4.1/debian/patches/06-Fix_OLENAMELENGTH.patch

BuildRequires:  gcc
BuildRequires: make

%description
catdoc is program which reads one or more Microsoft word files
and outputs text, contained insinde them to standard output.
Therefore it does same work for.doc files, as unix cat
command for plain ASCII files.
It is now accompanied by xls2csv - program which converts
Excel spreadsheet into comma-separated value file,
and catppt - utility to extract textual information
from Powerpoint files

%prep
(cd %{_sourcedir} && sha512sum -c --strict checksums)
%setup
%patch0 -p1 -b .makefilefix
%patch1 -p1 -b .debian-01
%patch2 -p1 -b .debian-03
%patch3 -p1 -b .debian-04
%patch4 -p1 -b .debian-05
%patch5 -p1 -b .debian-06

%build
%configure
%make_build

%install
make install DESTDIR=$RPM_BUILD_ROOT

# keep wordview which depends on tk, but move it to share dir
install -d -m 0755 %{buildroot}/%{_datadir}/catdoc/wordview
mv %{buildroot}/%{_bindir}/wordview %{buildroot}/%{_datadir}/catdoc/wordview/wordview.tcl
sed '1c#!/usr/bin/wish' %{buildroot}/%{_datadir}/catdoc/wordview/wordview.tcl
chmod 644 %{buildroot}/%{_datadir}/catdoc/wordview/wordview.tcl
mv %{buildroot}/%{_mandir}/man1/wordview.1 %{buildroot}/%{_datadir}/catdoc/wordview/

%files
%doc NEWS README TODO
%license COPYING
%{_bindir}/catdoc
%{_bindir}/catppt
%{_bindir}/xls2csv
%{_mandir}/man1/catdoc.1.*
%{_mandir}/man1/catppt.1.*
%{_mandir}/man1/xls2csv.1.*
%{_datadir}/catdoc
