%define url_ver %(echo %{version} | cut -d. -f1,2)

%bcond docs 0

Name:    libdex
Version: 1.2.0
Release: 2
Summary: a library supporting "Deferred Execution" for GNOME and GTK
Group:   System/Libraries

License: LGPL-2.1-or-later
URL:     https://gitlab.gnome.org/GNOME/libdex
Source0: https://download.gnome.org/sources/libdex/%{url_ver}//%{name}-%{version}.tar.xz

BuildRequires: pkgconfig(vapigen)
%if %{with docs}
BuildRequires: gi-docgen
%endif
BuildRequires: atomic-devel
BuildRequires: meson
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(liburing)
# The split capture library satisfies this. lib64sysprof-devel pulls this
# package back in, which still required Python 3.14.
BuildRequires: sysprof-capture
BuildRequires: pkgconfig(sysprof-capture-4)

%description
Dex is a library supporting "Deferred Execution" with the explicit goal
of integrating with GNOME and GTK-based applications.
It provides primatives for supporting futures in a variety of ways with both
read-only and writable views. Additionally, integration with existing
asynchronous-based APIs is provided through the use of wrapper promises.
"Fibers" are implemented which allows for writing synchronous looking code
which calls asynchronous APIs from GIO underneath.

%package  devel
Summary:  Development files for libdex
Group:    Development/C
Requires: %{name}%{?_isa} = %{EVRD}

%description devel
This package contains the libraries and header files that are needed for
writing applications with libdex.

%if %{with docs}
%package   devel-docs
Summary:   Developer documentation for libdex
Group:     Documentation
BuildArch: noarch
Requires:  %{name} = %{EVRD}

%description devel-docs
This package contains developer documentation for writing applications with
libdex.
%endif

%prep
%autosetup -p1

%build
%meson \
%if %{with docs}
  -Ddocs=true \
%else
  -Ddocs=false \
%endif
  -Dexamples=false \
  -Dsysprof=true
%meson_build

%install
%meson_install

%files
%license COPYING
%doc NEWS README.md
%{_libdir}/libdex-1.so.1{,.*}
%{_libdir}/girepository-1.0/
%{_libexecdir}/libdex-1/dex-gdbus-codegen-extension.py
%{python_sitelib}/gi/overrides/Dex.py
%{python_sitelib}/gi/overrides/__pycache__/Dex.cpython-*.pyc

%files devel
%{_datadir}/gir-1.0/
%{_datadir}/vala/
%{_includedir}/libdex-1/
%{_libdir}/libdex-1.so
%{_libdir}/pkgconfig/libdex-1.pc

%if %{with docs}
%files devel-docs
%doc %{_docdir}/libdex-1/
%endif
