# TODO:
# - correct .po intl files (add charset/encoding fileds)
#
# Conditional build:
%bcond_without	mad		# build without MP3 support
%bcond_without	speex		# build without speex audio codec support
%bcond_without	vorbis		# build without OggVorbis audio codec
%bcond_without	alsa		# build with alsa support
#
Summary:	Audio editor and live playback tool
Summary(pl.UTF-8):	Edytor dźwięku i narzędzie do odtwarzania na żywo
Name:		sweep
Version:	0.9.2
Release:	1
License:	GPL v2
Group:		X11/Applications/Sound
Source0:	http://dl.sourceforge.net/sweep/%{name}-%{version}.tar.bz2
# Source0-md5:	285e04b950dda85639f13aaac86153a0
Patch0:		%{name}-desktop.patch
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

%description -l pl.UTF-8
Sweep jest edytorem próbek dźwiękowych. Operuje na plikach różnych
formatów i posiada wielokrotne poziomy cofania/przywracania oraz
filtry. Obsługuje wtyczki dźwiękowe z projektu LADSPA.

%package devel
Summary:	Sweep plugin development kit
Summary(pl.UTF-8):	Zestaw deweloperski dla wtyczek Sweepa
Group:		Applications/Sound
# doesn't seem to require base

%description devel
The sweep-devel package contains header files and documentation for
writing plugins for Sweep.

%description devel -l pl.UTF-8
Pakiet sweep-devel zawiera pliki nagłówkowe i dokumentację do pisania
wtyczek dla Sweepa.

%prep
%setup -q
%patch0 -p1

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
install -d $RPM_BUILD_ROOT%{_desktopdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	desktopdir=%{_desktopdir}

mv -f $RPM_BUILD_ROOT%{_localedir}/es{_ES,}
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
%{_pixmapsdir}/sweep.svg
%{_datadir}/sweep
%{_desktopdir}/%{name}.desktop

%files devel
%defattr(644,root,root,755)
%doc doc/plugin_writers_guide.txt
%{_includedir}/sweep
