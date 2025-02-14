# TODO:
# - build drivers (like with BUILD_DRIVER=ON, eventually DKMS; only x86_64, aarch64, s390x?)
# - system bs_threadpool
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Falco foundation libraries
Summary(pl.UTF-8):	Biblioteki podstawowe Falco
Name:		falcosecurity-libs
Version:	0.18.1
Release:	2
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/falcosecurity/libs/releases
Source0:	https://github.com/falcosecurity/libs/archive/%{version}/libs-%{version}.tar.gz
# Source0-md5:	f89553c9aba58f669deabdbe64d1d808
Patch0:		%{name}-syscalls.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-cmake.patch
Patch3:		%{name}-pc.patch
URL:		https://github.com/falcosecurity/libs
BuildRequires:	c-ares-devel
BuildRequires:	cmake >= 3.12
BuildRequires:	curl-devel
# libelf
BuildRequires:	elfutils-devel
BuildRequires:	grpc-devel
BuildRequires:	gtest-devel
BuildRequires:	jq-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	libbpf-devel
BuildRequires:	openssl-devel
BuildRequires:	protobuf-devel
BuildRequires:	re2-devel
BuildRequires:	tbb-devel
BuildRequires:	tinydir-devel
BuildRequires:	valijson-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# missing symbols from libscap and libsinsp
%define		skip_post_check_so	libscap_engine_kmod.so.*

%description
This package contains libsinsp, libscap and the eBPF probes.

These components are at the foundation of Falco
(<https://github.com/falcosecurity/falco>) and other projects that
work with the same kind of data.

%description -l pl.UTF-8
Ten pakiet zawiera libsinsp, libscap oraz sondy eBPF.

Te komponenty są podstawą Falco
(<https://github.com/falcosecurity/falco>) oraz innych projektów
działających z tym samym rodzajem danych.

%package devel
Summary:	Header files for Falco libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Falco
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Falco library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Falco.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n libs-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

cp -p /usr/include/uthash.h userspace/libscap/uthash.h

%build
install -d build
cd build
%cmake .. \
	-DBUILD_DRIVER=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_LIBSCAP_EXAMPLES=OFF \
	-DBUILD_LIBSINSP_EXAMPLES=OFF \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCREATE_TEST_TARGETS=OFF \
	-DFALCOSECURITY_LIBS_VERSION=%{version} \
	-DENABLE_DKMS=OFF \
	-DUSE_BUNDLED_DEPS=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NOTICES README.md
%attr(755,root,root) %{_libdir}/libscap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscap.so.0
%attr(755,root,root) %{_libdir}/libscap_engine_bpf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscap_engine_bpf.so.0
%attr(755,root,root) %{_libdir}/libscap_engine_kmod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscap_engine_kmod.so.0
%attr(755,root,root) %{_libdir}/libscap_engine_nodriver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscap_engine_nodriver.so.0
%attr(755,root,root) %{_libdir}/libscap_engine_source_plugin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libscap_engine_source_plugin.so.0
%attr(755,root,root) %{_libdir}/libsinsp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsinsp.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libscap.so
%attr(755,root,root) %{_libdir}/libscap_engine_bpf.so
%attr(755,root,root) %{_libdir}/libscap_engine_kmod.so
%attr(755,root,root) %{_libdir}/libscap_engine_nodriver.so
%attr(755,root,root) %{_libdir}/libscap_engine_source_plugin.so
%attr(755,root,root) %{_libdir}/libsinsp.so
%{_includedir}/falcosecurity
%{_pkgconfigdir}/libscap.pc
%{_pkgconfigdir}/libsinsp.pc
%{_prefix}/src/scap-0.0.0
