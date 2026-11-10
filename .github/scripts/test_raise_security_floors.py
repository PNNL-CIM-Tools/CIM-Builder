import pytest
from raise_security_floors import raise_floors

PYPROJECT = '''
[project]
name = "example"
dependencies = [
    "pint>=0.24.4",
    "Some_Package[extra]>=1.0,<2",
]

[project.optional-dependencies]
neo4j = ["neo4j>=5.10.0"]

[dependency-groups]
dev = ["pytest>=8.3.5"]
'''


def update(name, version):
    return {'dependencyName': name, 'newVersion': version}


def test_raises_runtime_and_optional_floors_keeping_upper_bounds():
    text, raised = raise_floors(PYPROJECT, [update('pint', '0.25.1'), update('some-package', '1.2'),
                                            update('neo4j', '5.11.0')])
    assert raised == ['pint>=0.25.1', 'Some_Package[extra]>=1.2,<2', 'neo4j>=5.11.0']
    assert '"Some_Package[extra]>=1.2,<2"' in text


def test_ignores_dev_and_transitive_deps():
    text, raised = raise_floors(PYPROJECT, [update('pytest', '9.0'), update('urllib3', '2.8.0')])
    assert raised == []
    assert text == PYPROJECT


def test_fails_without_lower_bound():
    with pytest.raises(ValueError, match='no >= bound'):
        raise_floors('[project]\ndependencies = ["pint"]\n', [update('pint', '0.25.1')])
