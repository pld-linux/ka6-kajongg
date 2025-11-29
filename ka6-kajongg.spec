#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.3
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kajongg
Summary:	Mah Jongg for four players
Name:		ka6-%{kaname}
Version:	25.08.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications/Games
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	c640e7ce9f1c2613c30d2bd8a1d49bc0
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Svg-devel
BuildRequires:	Qt6Widgets-devel >= 5.8.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	ka6-libkdegames-devel >= %{kdeappsver}
BuildRequires:	ka6-libkmahjongg-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	python3
BuildRequires:	python3-twisted >= 16.6.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires:	python3-twisted >= 16.6.0
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%global         debug_package   %{nil}

%description
Kajongg - the classical Mah Jongg for four players. If you are looking
for the Mah Jongg solitaire please use the application KMahjongg.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DCMAKE_INSTALL_PREFIX=/
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

sed -i -e 's|!/usr/bin/env python3|!/usr/bin/python3|' $RPM_BUILD_ROOT%{_datadir}/kajongg/kajongg*py

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README README.packagers README.windows
%{_desktopdir}/org.kde.kajongg.desktop
%{_iconsdir}/hicolor/*x*/apps/kajongg.png
%{_iconsdir}/hicolor/scalable/actions/games-kajongg-law.svgz
%{_iconsdir}/hicolor/scalable/apps/kajongg.svgz
%dir %{_datadir}/kajongg
%{_datadir}/kajongg/__pycache__
%attr(755,root,root) %{_datadir}/kajongg/*.py
%{_datadir}/kajongg/kajonggui.rc
%{_datadir}/kajongg/voices
%{_datadir}/metainfo/org.kde.kajongg.appdata.xml
%attr(755,root,root) %{_bindir}/kajongg
%attr(755,root,root) %{_bindir}/kajonggserver
