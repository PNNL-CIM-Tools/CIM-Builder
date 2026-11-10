"""Raise pyproject.toml minimum versions for runtime deps in a Dependabot security PR.

Only [project] dependencies and optional-dependencies ship to PyPI users; dev,
docs and transitive deps are lockfile-only and left alone. Reads the
fetch-metadata `updated-dependencies-json` from $UPDATED_DEPENDENCIES, rewrites
pyproject.toml in place and prints each raised requirement (nothing if none).
"""

import json
import os
import re
import tomllib
from pathlib import Path

NAME_PATTERN = re.compile(r'[A-Za-z0-9._-]+')
LOWER_BOUND_PATTERN = re.compile(r'>=\s*[^,;\s]+')


def normalize(name: str) -> str:
    return re.sub(r'[-_.]+', '-', name).lower()


def runtime_requirements(pyproject_text: str) -> list[str]:
    project = tomllib.loads(pyproject_text)['project']
    requirements = list(project.get('dependencies', []))
    for extra in project.get('optional-dependencies', {}).values():
        requirements.extend(extra)
    return requirements


def raise_floors(pyproject_text: str, updates: list[dict]) -> tuple[str, list[str]]:
    new_versions = {normalize(u['dependencyName']): u['newVersion'] for u in updates}
    raised = []
    for requirement in runtime_requirements(pyproject_text):
        name = normalize(NAME_PATTERN.match(requirement).group())
        if name not in new_versions:
            continue
        if not LOWER_BOUND_PATTERN.search(requirement):
            raise ValueError(f'{requirement!r} has no >= bound to raise; update pyproject.toml manually')
        new_requirement = LOWER_BOUND_PATTERN.sub(f'>={new_versions[name]}', requirement, count=1)
        pyproject_text = pyproject_text.replace(f'"{requirement}"', f'"{new_requirement}"')
        raised.append(new_requirement)
    return pyproject_text, raised


def main() -> None:
    pyproject = Path('pyproject.toml')
    updates = json.loads(os.environ['UPDATED_DEPENDENCIES'])
    new_text, raised = raise_floors(pyproject.read_text(), updates)
    pyproject.write_text(new_text)
    print('\n'.join(raised))


if __name__ == '__main__':
    main()
