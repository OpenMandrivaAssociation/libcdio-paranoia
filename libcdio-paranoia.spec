%define build_vcd 0
%{?_with_vcd: %{expand: %%global build_vcd 1}}
%{?_without_vcd: %{expand: %%global build_vcd 0}}

%define extver 10.2+
%define major 2
%define libname %mklibname cdio_paranoia %{major}
%define libcdda %mklibname cdio_cdda %{major}
%define devname %mklibname -d cdio_paranoia

Summary:	CD-ROM reading library
Name:		libcdio-paranoia
Version:	2.0.2
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		https://github.com/libcdio/libcdio-paranoia
Source0:	https://github.com/libcdio/libcdio-paranoia/releases/download/release-%{extver}%{version}/%{name}-%{extver}%{version}.tar.bz2
Source2:	libcdio-paranoia.rpmlintrc
Patch0:		libcdio-paranoia_includedir.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	pkgconfig(libcddb)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(libcdio)
#gw only if we change the man pages
#BuildRequires: help2man
%if %build_vcd
BuildRequires:	pkgconfig(libvcdinfo)
%endif

%description
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

%package apps
Summary:	Example tool from %{name}
Group:		Sound

%description apps
This CDDA reader distribution ('libcdio-cdparanoia') reads audio from the
CDROM directly as data, with no analog step between, and writes the
data to a file or pipe as .wav, .aifc or as raw 16 bit linear PCM.

%package -n %{libname}
Summary:	Library from %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the library for libcdio-paranoia.

%package -n %{libcdda}
Summary:	Libraries from %{name}
Group:		System/Libraries

%description -n %{libcdda}
This package contains the library for libcdio-cdda.

%package -n %{devname}
Summary:	Devel files from %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libcdda} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This is the libraries, include files and other resources you can use
to incorporate %{name} into applications.

%prep
%autosetup -qn %{name}-%{extver}%{version} -p1

# fix pkgconfig files
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_paranoia.pc.in
sed -i -e 's,-I${includedir},-I${includedir}/cdio,g' libcdio_cdda.pc.in

%build
%configure \
	--disable-static \
	--disable-rpath \
	--without-versioned-libs \
%if ! %build_vcd
	--disable-vcd-info
%endif

%make_build

%install
%make_install

%files apps
%{_bindir}/*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*

%files -n %{libname}
%{_libdir}/libcdio_paranoia.so.%{major}*
# (tpg) needed for bug https://issues.openmandriva.org/show_bug.cgi?id=876
%{_libdir}/*paranoia.so

%files -n %{libcdda}
%{_libdir}/libcdio_cdda.so.%{major}*
# (tpg) needed for bug https://issues.openmandriva.org/show_bug.cgi?id=876
%{_libdir}/libcdio_cdda.so

%files -n %{devname}
%doc ChangeLog AUTHORS NEWS.md README.md
%{_includedir}/cdio
%{_libdir}/pkgconfig/libcdio_paranoia.pc
%{_libdir}/pkgconfig/libcdio_cdda.pc
