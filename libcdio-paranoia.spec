%define build_vcd 1
%{?_with_vcd: %{expand: %%global build_vcd 1}}
%{?_without_vcd: %{expand: %%global build_vcd 0}}

%define extver 10.2+
%define major 1
%define libname %mklibname cdio_paranoia %{major}
%define libcdda %mklibname cdio_cdda %{major}
%define devname %mklibname -d cdio_paranoia

Summary:	CD-ROM reading library
Name:		libcdio-paranoia
Version:	0.90
Release:	20
License:	GPLv3+
Group:		System/Libraries
URL:		http://www.gnu.org/software/libcdio/
Source0:	ftp://ftp.gnu.org/pub/gnu/libcdio/%{name}-%{extver}%{version}.tar.gz
Source1:	ftp://ftp.gnu.org/pub/gnu/libcdio/%{name}-%{extver}%{version}.tar.gz.sig
Source2:	libcdio-paranoia.rpmlintrc
Patch0:		libcdio-paranoia_includedir.patch

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
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcdda} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This is the libraries, include files and other resources you can use
to incorporate %{name} into applications.

%prep
%setup -qn %{name}-%{extver}%{version}

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

%make

%install
%makeinstall_std

# copy include files to an additional directory
# this will probably be the location for future releases see:
# https://github.com/rocky/libcdio-paranoia/commit/b2807f3c7a4126b6078d96adbd37c3760b9f41ab
mkdir -p %{buildroot}%{_includedir}/cdio/paranoia
cp -a %{buildroot}%{_includedir}/cdio/*.h %{buildroot}%{_includedir}/cdio/paranoia


%files apps
%{_bindir}/*
%{_mandir}/man1/*
%lang(jp) %{_mandir}/jp/man1/*

%files -n %{libname}
%{_libdir}/libcdio_paranoia.so.%{major}*

%files -n %{libcdda}
%{_libdir}/libcdio_cdda.so.%{major}*

%files -n %{devname}
%doc ChangeLog README AUTHORS NEWS INSTALL
%{_includedir}/cdio
%{_libdir}/*paranoia.so
# (tpg) needed for bug https://issues.openmandriva.org/show_bug.cgi?id=876
%{_libdir}/libcdio_cdda.so
%{_libdir}/pkgconfig/libcdio_paranoia.pc
%{_libdir}/pkgconfig/libcdio_cdda.pc

