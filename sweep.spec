# TODO:
# - correct .po intl files (add charset/encoding fileds)
#
# Conditional build:
%bcond_without	mad		# build without mp3 support
%bcond_without	speex		# build without speex audio codec support
%bcond_without	vorbis		# build without oggvorbis audio codec
%bcond_with	alsa		# build with alsa support
#
Summary:	Audio editor and live playback tool
Summary(pl):	Edytor d¼wiêku i narzêdzie do odtwarzania na ¿ywo
Name:		sweep
Version:	0.8.3
Release:	1
License:	GPL
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/sweep/%{name}-%{version}.tar.gz
# Source0-md5:	2b9ee0529c666f80b362aeefae28b891
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-alsa10.patch
URL:		http://sweep.sourceforge.net/
%{?with_alsa:BuildRequires:	alsa-lib-devel >= 1.0.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	libsamplerate-devel >= 0.0.9
BuildRequires:	libsndfile-devel >= 1.0.0
BuildRequires:	libtool
%{?with_vorbis:BuildRequires:	libvorbis-devel}
%{?with_mad:BuildRequires:	libmad-devel}
%{?with_speex:BuildRequires:	speex-devel}
BuildRequires:	tdb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sweep is an editor for sound samples. It operates on files of various
formats and has multiple undo/redo levels and filters.
It supports audio filter plugins from the LADSPA project.

%description -l pl
Sweep jest edytorem próbek d¼wiêkowych. Operuje na plikach ró¿nych
formatów i posiada wielokrotne poziomy cofania/przywracania oraz
filtry. Obs³uguje wtyczki d¼wiêkowe z projektu LADSPA.

%package devel
Summary:	Sweep plugin development kit
Summary(pl):	Zestaw deweloperski dla wtyczek Sweepa
Group:		Applications/Sound
# doesn't seem to require base

%description devel
The sweep-devel package contains header files and documentation for
writing plugins for Sweep.

%description devel -l pl
Pakiet sweep-devel zawiera pliki nag³ówkowe i dokumentacjê do pisania
wtyczek dla Sweepa.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

%configure \
	--enable-experimental \
	%{?with_alsa:--enable-alsa} \
	%{!?with_mad:--disable-mad} \
	%{!?with_speex:--disable-speex} \
	%{!?with_vorbis:--disable-oggvorbis}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_applnkdir}/Multimedia

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	desktopdir=%{_applnkdir}/Multimedia

# useless (loaded through libgmodule by SONAME)
rm -f $RPM_BUILD_ROOT%{_libdir}/sweep/lib*.{la,a}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README ChangeLog README.ALSA
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/sweep
%{_libdir}/sweep/lib*.so
%{_mandir}/man1/*
%{_pixmapsdir}/sweep.png
%{_datadir}/sweep
%{_applnkdir}/Multimedia/%{name}.desktop

%files devel
%defattr(644,root,root,755)
%doc doc/plugin_writers_guide.txt
%{_includedir}/sweep
