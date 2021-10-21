import pytest
from rpmlint.checks.AlternativesCheck import AlternativesCheck
from rpmlint.filter import Filter

from Testing import CONFIG, get_tested_package


@pytest.fixture(scope='function', autouse=True)
def alternativescheck():
    CONFIG.info = True
    output = Filter(CONFIG)
    test = AlternativesCheck(CONFIG, output)
    return output, test


#
# udpate-alternatives tests
#


@pytest.mark.parametrize('package', ['binary/alternatives-ok'])
def test_update_alternative_ok(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    assert 'I: package supports update-alternatives' in out
    assert 'E' not in out
    assert 'W' not in out


@pytest.mark.parametrize('package', ['binary/alternatives-borked'])
def test_update_alternative_borked(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    assert 'E: update-alternatives-requirement-missing' in out
    assert 'E: alternative-generic-name-not-symlink' in out
    assert 'E: alternative-link-not-ghost' in out
    assert 'E: update-alternatives-postun-call-missing' in out


@pytest.mark.parametrize('package', ['binary/self'])
def test_non_update_alternative_pkg(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    # here we just check if there is no requirements checking on
    # non update-alternatived package
    assert 'E' not in out
    assert 'W' not in out


@pytest.mark.parametrize('package', ['binary/python39-evtx'])
def test_update_alternatives_correctness(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    assert 'E: update-alternatives-postun-call-missing' not in out


#
# libalternatives tests
#


@pytest.mark.parametrize('package', ['binary/libalternatives-ok'])
def test_libalternative_ok(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    assert 'I: package supports libalternatives' in out
    assert 'E' not in out
    assert 'W' not in out


@pytest.mark.parametrize('package', ['binary/libalternatives-borked'])
def test_libalternative_borked(tmpdir, package, alternativescheck):
    output, test = alternativescheck
    test.check(get_tested_package(package, tmpdir))
    out = output.print_results(output.results)
    assert 'I: package supports libalternatives' in out
    assert 'I: libalternatives-conf-not-found' in out
    assert 'E: alts-requirement-missed' in out
    assert 'E: libalternatives-directory-not-exist' in out
    assert 'E: empty-libalternatives-directory' in out
    assert 'W: man-entry-value-not-found' in out
    assert 'W: binary-entry-value-not-found' in out
