%define build_vcd 1
%{?_with_vcd: %{expand: %%global build_vcd 1}}
%{?_without_vcd: %{expand: %%global build_vcd 0}}

%define extver	10.2+
%define major	1
%define libname %mklibname cdio_paranoia %{major}
%define libcdda %mklibname cdio_cdda %{major}
%define devname %mklibname -d cdio_paranoia

Summary:	CD-ROM reading library
Name:		libcdio-paranoia
Version:	0.90
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		http://www.gnu.org/software/libcdio/
Source0:	ftp://ftp.gnu.org/pub/gnu/libcdio/%{name}-%{extver}%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/pub/gnu/libcdio/%{name}-%{extver}%{version}.tar.gz.sig

BuildRequires:	pkgconfig(libcddb)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
#gw only if we change the man pages
#BuildRequires: help2man
%if %build_vcd
BuildRequires:	pkgconfig(libvcdinfo)
%endif

%description
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
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcdda} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This is the libraries, include files and other resources you can use
to incorporate %{name} into applications.

%prep
%setup -qn %{name}-%{extver}%{version}

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--without-versioned-libs \
%if ! %build_vcd
	--disable-vcd-info
%endif

%make

%install
%makeinstall_std

%files apps
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libcdio-paranoia.so.%{major}*

%files -n %{libcdda}
%{_libdir}/libcdio-cdda.so.%{major}*

%files -n %{devname}
%doc ChangeLog README AUTHORS NEWS INSTALL TODO
%{_includedir}/cdio
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcdio-paranoia.pc
%{_libdir}/pkgconfig/libcdio-cdda.pc

