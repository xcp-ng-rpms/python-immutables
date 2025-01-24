%global package_speccommit df2f29fbadd0e995ff5bb90100b5aa01c265cd0d
%global usver 0.19
%global xsver 5
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global srcname immutables

%bcond_with tests

%global common_description %{expand:
An immutable mapping type for Python.

The underlying datastructure is a Hash Array Mapped Trie (HAMT) used in
Clojure, Scala, Haskell, and other functional languages. This implementation is
used in CPython 3.7 in the contextvars module (see PEP 550 and PEP 567 for more
details).

Immutable mappings based on HAMT have O(log N) performance for both set() and
get() operations, which is essentially O(1) for relatively small mappings.}


Name:           python-%{srcname}
Version:        0.19
Release:        %{?xsrel}%{?dist}
Summary:        Immutable Collections
# The entire source code is Apache-2.0, except pythoncapi_compat.h, which is
# 0BSD. While this file is unbundled, it is a header-only library; its entire
# contents are compiled into the binary RPM, and packaging guidelines treat it
# as a static library. Its license therefore contributes to the license of the
# binary RPM. See discussion in
# https://src.fedoraproject.org/rpms/python-immutables/pull-request/2, and the
# (Rust-specific but relevant) policy
# https://docs.fedoraproject.org/en-US/legal/license-field/#_rust_packages.
License:        Apache-2.0 AND 0BSD
URL:            https://github.com/MagicStack/immutables
Source0: immutables-0.19.tar.gz

Source1: pyproject_wheel.py

BuildRequires:  gcc


%description %{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-wheel

%if %{with tests}
BuildRequires:  python3-pytest
%endif

%if 0%{?xenserver} >= 9
BuildRequires:  pip
BuildRequires:  python3-setuptools
%endif

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_packaging_header_only_libraries
%if 0
BuildRequires:  pythoncapi-compat-static
%endif

%description -n python3-%{srcname} %{common_description}


%prep
%autosetup -n %{srcname}-%{version}

# don't install source files
sed -e '/include_package_data=/ s/True/False/' -i setup.py

# delete mypy tests to avoid that dependency
rm tests/conftest.py tests/test_mypy.py

# remove bundled pythoncapi-compat
%if 0
rm -vf immutables/pythoncapi_compat.h
%endif


%if 0%{?xenserver} >= 9
%generate_buildrequires
%pyproject_buildrequires
%endif


%build
%if 0%{?xenserver} < 9
echo "from setuptools import setup

setup(name=\"%{name}\",
      version='%{version}',
     )" > ./setup.py
/usr/bin/python3 -Bs %{SOURCE1} %{_builddir}/%{srcname}-%{version}/pyproject-wheeldir
%else
%pyproject_wheel
%endif


%install
%if 0%{?xenserver} < 9
/usr/bin/python3 -m pip install --root %{buildroot} --prefix /usr --no-deps --disable-pip-version-check --verbose --ignore-installed --no-index --no-cache-dir --find-links %{_builddir}/%{srcname}-%{version}/pyproject-wheeldir
%else
%pyproject_install
%pyproject_save_files %{srcname}
%endif

%if 0%{?xenserver} < 9
# Copy source files to buildroot manually
mkdir -p %{buildroot}%{python3_sitelib}/immutables
cp -r %{_builddir}/%{srcname}-%{version}/%{srcname} %{buildroot}%{python3_sitelib}/
find %{buildroot}%{python3_sitelib}/%{srcname}
%endif

%check
%if %{with tests}
%pytest --verbose
%else
%if 0%{?xenserver} >= 9
%pyproject_check_import
%endif
%endif

%if 0%{?xenserver} < 9
%files -n python3-%{srcname}
%dir %{python3_sitelib}/%{srcname}
%dir %{python3_sitelib}/%{srcname}/__pycache__
%{python3_sitelib}/%{srcname}/__init__.py
%{python3_sitelib}/%{srcname}/_map.c
%{python3_sitelib}/%{srcname}/_map.h
%{python3_sitelib}/%{srcname}/pythoncapi_compat.h
%{python3_sitelib}/%{srcname}/__pycache__/__init__.cpython-*.pyc
%{python3_sitelib}/%{srcname}/__pycache__/_protocols.cpython-*.pyc
%{python3_sitelib}/%{srcname}/__pycache__/_testutils.cpython-*.pyc
%{python3_sitelib}/%{srcname}/__pycache__/_version.cpython-*.pyc
%{python3_sitelib}/%{srcname}/__pycache__/map.cpython-*.pyc
%{python3_sitelib}/%{srcname}/_map.pyi
%{python3_sitelib}/%{srcname}/_protocols.py
%{python3_sitelib}/%{srcname}/_testutils.py
%{python3_sitelib}/%{srcname}/_version.py
%{python3_sitelib}/%{srcname}/map.py
%{python3_sitelib}/%{srcname}/py.typed
%doc README.rst
%else
%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%endif


%changelog
* Mon Aug 19 2024 Marcus Granado <marcus.granado@cloud.com> - 0.19-5
- Bump release and rebuild

* Fri Aug 09 2024 Marcus Granado <marcus.granado@cloud.com> - 0.19-5
- Bump release and rebuild

* Mon Feb 12 2024 Rachel Yan <rachel.yan@citrix.com> - 0.19-2
- Initial import
