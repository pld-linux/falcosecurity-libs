# TODO:
# - build drivers (like with BUILD_DRIVER=ON, eventually DKMS; only x86_64, aarch64, s390x?)
# - system bs_threadpool
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
%bcond_without	gvisor		# gvisor engine
#
%ifnarch %{x8664} x32
%undefine	with_gvisor
%endif
Summary:	Falco foundation libraries
Summary(pl.UTF-8):	Biblioteki podstawowe Falco
Name:		falcosecurity-libs
Version:	0.22.1
Release:	3
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/falcosecurity/libs/releases
Source0:	https://github.com/falcosecurity/libs/archive/%{version}/libs-%{version}.tar.gz
# Source0-md5:	60567f6c088e5da7941c5b3c7862cda7
Patch0:		%{name}-syscalls.patch
Patch1:		%{name}-link.patch
Patch3:		%{name}-pc.patch
URL:		https://github.com/falcosecurity/libs
BuildRequires:	cmake >= 3.12
# libelf
BuildRequires:	elfutils-devel
BuildRequires:	jsoncpp-devel
%{?with_gvisor:BuildRequires:	protobuf-devel}
BuildRequires:	re2-devel
BuildRequires:	tbb-devel
BuildRequires:	valijson-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# cyclic symbol dependency with libscap.so.*
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
%{?with_gvisor:Requires:	protobuf-devel}
Requires:	elfutils-devel
Requires:	jsoncpp-devel
Requires:	re2-devel
Requires:	tbb-devel
Requires:	zlib-devel

%description devel
Header files for Falco library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Falco.

%prep
%setup -q -n libs-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1

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
%{_libdir}/libscap.so.*.*.*
%ghost %{_libdir}/libscap.so.0
%{_libdir}/libscap_engine_bpf.so.*.*.*
%ghost %{_libdir}/libscap_engine_bpf.so.0
%if %{with gvisor}
%{_libdir}/libscap_engine_gvisor.so.*.*.*
%ghost %{_libdir}/libscap_engine_gvisor.so.0
%endif
%{_libdir}/libscap_engine_kmod.so.*.*.*
%ghost %{_libdir}/libscap_engine_kmod.so.0
%{_libdir}/libscap_engine_nodriver.so.*.*.*
%ghost %{_libdir}/libscap_engine_nodriver.so.0
%{_libdir}/libscap_engine_source_plugin.so.*.*.*
%ghost %{_libdir}/libscap_engine_source_plugin.so.0
%{_libdir}/libsinsp.so.*.*.*
%ghost %{_libdir}/libsinsp.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libscap.so
%{_libdir}/libscap_engine_bpf.so
%if %{with gvisor}
%{_libdir}/libscap_engine_gvisor.so
%endif
%{_libdir}/libscap_engine_kmod.so
%{_libdir}/libscap_engine_nodriver.so
%{_libdir}/libscap_engine_source_plugin.so
%{_libdir}/libsinsp.so
%{_includedir}/falcosecurity
%{_pkgconfigdir}/libscap.pc
%{_pkgconfigdir}/libsinsp.pc
%{_prefix}/src/scap-0.0.0
