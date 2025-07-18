# NOTE: for versions >= 5 (for python 3.5+) see python3-pytest.spec
#
# Conditional build:
%bcond_without	doc	# HTML documentation build
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-pytest.spec)
%bcond_without	tests	# unit tests

%define		pylib_version	1.5.0
%define 	module	pytest
Summary:	Simple and popular testing tool for Python
Summary(pl.UTF-8):	Proste i popularne narzędzie testujące dla Pythona
# note: keep 4.x here for python2 support
Name:		python-%{module}
Version:	4.6.11
Release:	6
License:	MIT
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/pytest/
Source0:	https://files.pythonhosted.org/packages/source/p/pytest/pytest-%{version}.tar.gz
# Source0-md5:	26cf20887076ad8a7beccfb5e9c44d04
Patch0:		%{name}-tests.patch
URL:		https://pytest.org/
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-py >= %{pylib_version}
BuildRequires:	python-setuptools >= 1:40.0
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc >= 1:2.7
BuildRequires:	python-argcomplete
BuildRequires:	python-atomicwrites >= 1.0
BuildRequires:	python-attrs >= 17.4.0
BuildRequires:	python-funcsigs >= 1.0
BuildRequires:	python-hypothesis >= 3.56
BuildRequires:	python-importlib_metadata >= 0.12
BuildRequires:	python-mock
BuildRequires:	python-more_itertools >= 4.0.0
BuildRequires:	python-more_itertools < 6.0.0
BuildRequires:	python-nose
BuildRequires:	python-packaging
BuildRequires:	python-pathlib2 >= 2.2.0
BuildRequires:	python-pluggy >= 0.12
BuildRequires:	python-pluggy < 1.0
BuildRequires:	python-requests
BuildRequires:	python-six >= 1.10.0
BuildRequires:	python-wcwidth
BuildConflicts:	python-pytest-benchmark < 3.2.1
# outdated
BuildConflicts:	python-pytest-catchlog
# with xdist requires various modules source and breaks other things
BuildConflicts:	python-pytest-xdist
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-py >= %{pylib_version}
BuildRequires:	python3-setuptools >= 1:40.0
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	pydoc3 >= 1:3.4
BuildRequires:	python3-argcomplete
BuildRequires:	python3-atomicwrites >= 1.0
BuildRequires:	python3-attrs >= 17.4.0
BuildRequires:	python3-hypothesis >= 3.56
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.12
%endif
BuildRequires:	python3-more_itertools >= 4.0.0
BuildRequires:	python3-nose
BuildRequires:	python3-packaging
%if "%{py3_ver}" < "3.6"
BuildRequires:	python3-pathlib2 >= 2.2.0
%endif
BuildRequires:	python3-pluggy >= 0.12
BuildRequires:	python3-pluggy < 1.0
BuildRequires:	python3-requests
BuildRequires:	python3-six >= 1.10.0
BuildRequires:	python3-wcwidth
BuildConflicts:	python3-pytest-benchmark < 3.2.1
# outdated
BuildConflicts:	python3-pytest-catchlog
# seems to break things
BuildConflicts:	python3-pytest-xdist
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-atomicwrites
BuildRequires:	python3-attrs
BuildRequires:	python3-pluggy
BuildRequires:	python3-pygments_pytest
BuildRequires:	python3-sphinx_removed_in >= 0.2.0
BuildRequires:	python3-sphinxcontrib-trio
BuildRequires:	sphinx-pdg-3 >= 1.8.2
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-pluggy
Requires:	python-setuptools
Obsoletes:	python-pytest-cache < 1.1
Obsoletes:	python-pytest-catchlog < 1.2.3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
py.test is a simple and popular testing tool for Python.

%description -l pl.UTF-8
py.test to proste i popularne narzędzie testujące dla Pythona.

%package -n python3-pytest
Summary:	Simple powerful testing with Python
Summary(pl.UTF-8):	Proste, ale funkcjonalne narzędzie testujące dla Pythona
Group:		Development/Languages
Requires:	python3-devel-tools >= 1:3.4
Requires:	python3-setuptools
Obsoletes:	python3-pytest-cache < 1.1
Obsoletes:	python3-pytest-catchlog < 1.2.3

%description -n python3-pytest
py.test provides simple, yet powerful testing for Python.

%description -n python3-pytest -l pl.UTF-8
py.test to proste, ale bardzo funkcjonalne narzędzie testujące dla
Pythona.

%package apidocs
Summary:	Documentation for py.test Pythona package
Summary(pl.UTF-8):	Dokumentacja pakietu Pythona py.test
Group:		Documentation

%description apidocs
Documentation for py.test Pythona package.

%description apidocs -l pl.UTF-8
Dokumentacja pakietu Pythona py.test.

%prep
%setup -q -n %{module}-%{version}
%patch -P0 -p1

%build
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
%if %{with python2}
%py_build

%if %{with tests}
# test_pdb_custom_cls_with_settrace fails without preinstalled pytest
# test_cache_writefail_permissions, test_cache_failure_warns makes tests unreliable due to post-test cleanup failures
# test_pytester.py, test_terminal.py, test_unittest.py need ptys to spawn processes with terminal
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest -k 'not (test_pdb or test_cache_writefail_permissions or test_cache_failure_warns or test_pytester or test_terminal or test_unittest)' testing
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_pdb_custom_cls_with_settrace fails without preinstalled pytest
# test_pdb_* which spawn pdb hang under some unclear conditions
# test_cache_writefail_permissions, test_cache_failure_warns makes tests unreliable due to post-test cleanup failures
# test_pytester.py, test_terminal.py, test_unittest.py need ptys to spawn processes with terminal
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest -k 'not (test_pdb or test_cache_writefail_permissions or test_cache_failure_warns or test_pytester or test_terminal or test_unittest)' testing
%endif
%endif

%if %{with doc}
for l in doc/*; do
	PYTHONPATH=$(pwd)/src \
	%{__make} -C $l html \
		SPHINXBUILD=sphinx-build-3
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test{,-2}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest{,-2}

# pytest.py source seems required for "monkeypatching" tests
%py_postclean -x pytest.py
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/py.test{,-3}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/pytest{,-3}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test-2
%attr(755,root,root) %{_bindir}/pytest-2
%{py_sitescriptdir}/pytest.py*
%{py_sitescriptdir}/_pytest
%{py_sitescriptdir}/pytest-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pytest
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/py.test-3
%attr(755,root,root) %{_bindir}/pytest-3
%{py3_sitescriptdir}/pytest.py
%{py3_sitescriptdir}/_pytest
%{py3_sitescriptdir}/__pycache__/pytest.*.py[co]
%{py3_sitescriptdir}/pytest-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/en/_build/html/{_images,_modules,_static,announce,example,proposals,*.html,*.js}
%endif
