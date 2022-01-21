# what it's called on pypi
%global srcname immutables
# what it's imported as
%global libname %{srcname}
# name of egg info directory
%global eggname %{srcname}
# package name fragment
%global pkgname %{srcname}

# Tests fail on 32-bit
# https://github.com/MagicStack/immutables/issues/50
%ifnarch %{ix86} %{arm32}
%bcond_without  tests
%endif

%global common_description %{expand:
An immutable mapping type for Python.

The underlying datastructure is a Hash Array Mapped Trie (HAMT) used in
Clojure, Scala, Haskell, and other functional languages. This implementation is
used in CPython 3.7 in the contextvars module (see PEP 550 and PEP 567 for more
details).

Immutable mappings based on HAMT have O(log N) performance for both set() and
get() operations, which is essentially O(1) for relatively small mappings.}


Name:           python-%{pkgname}
Version:        0.15
Release:        5%{?dist}
Summary:        Immutable Collections
License:        ASL 2.0 and MIT
URL:            https://github.com/MagicStack/immutables
Source0:        %pypi_source
# upstream is missing license for pythoncapi_compat.h
# https://github.com/MagicStack/immutables/pull/64
Source1:        https://raw.githubusercontent.com/pythoncapi/pythoncapi_compat/main/COPYING

BuildRequires:  gcc


%description %{common_description}


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
%endif


%description -n python3-%{pkgname} %{common_description}


%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{eggname}.egg-info

# copy second license file to builddir for %%license macro
cp %{SOURCE1} LICENSE.MIT

# don't install source files
sed -e '/include_package_data=/ s/True/False/' -i setup.py


%build
%py3_build


%install
%py3_install


%if %{with tests}
%check
%pytest --verbose
%endif


%files -n python3-%{pkgname}
%license LICENSE LICENSE.MIT
%doc README.rst
%{python3_sitearch}/%{libname}
%{python3_sitearch}/%{eggname}-%{version}-py%{python3_version}.egg-info


%changelog
* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.15-3
- Rebuilt for Python 3.10

* Wed Apr 21 2021 Carl George <carl@george.computer> - 0.15-2
- Include missing upstream license
- Disable package data in setup.py to avoid installing source files

* Wed Apr 21 2021 Carl George <carl@george.computer> - 0.15-1
- Initial package rhbz#1951868
