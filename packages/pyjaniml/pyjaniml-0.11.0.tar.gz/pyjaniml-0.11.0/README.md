# pyjaniml

[![Version](https://img.shields.io/pypi/v/pyjaniml?label=Version&style=for-the-badge)](https://pypi.org/project/pyjaniml/)
![License: MIT](https://img.shields.io/pypi/l/pyjaniml?style=for-the-badge)
[![Python Versions: see setup.py](https://img.shields.io/pypi/pyversions/pyjaniml?label=Python&style=for-the-badge)](https://gitlab.com/clade-public/pyjaniml/)

A package to serialize and deserialize janiml json documents using marshmallow.

## Based on
https://docs.google.com/document/d/1vpPbkAqPFc22efJ0IXvGGSzAn_4VFNG_OiaEfn42zx4/edit?usp=sharing

https://github.com/AnIML/schemas/blob/master/animl-core.xsd

## Installation
Install directly from the GitLab repository
`$ pip install pyjaniml`

## Usage

### Example usage

### Not yet implemented
- Nested categories
- Signature Set
- Audit Trail

## Contributing

The project uses [black](https://pypi.org/project/black/) and
[isort](https://pypi.org/project/isort/) for formatting its code.
[flake8](https://pypi.org/project/flake8/) is used for linting.
[mypy](http://www.mypy-lang.org/) is used for type checking. All these are
combined into [pre-commit](https://pre-commit.com/) to run before each commit
and push. To set it up:

```console
(env)$ python -m pip install pre-commit
(env)$ pre-commit install -t pre-commit -t pre-push --install-hooks
```

To run the unit tests you need some additional utilities that need to be
installed before you can run the tests.

```console
(env)$ python -m pip install -r requirements/tests.txt .
(env)$ python -m pip install -e .
(env)$ pytest --cov
```

### Issuing a new Release

1. Determine the next version you want to release. For that, check the
   [CHANGELOG](https://gitlab.com/clade-public/pyjaniml/-/blob/main/CHANGELOG.md)
   and the chances made since the last release. Let's call it `$VERSION`.

1. Start a new branch `release/$VERSION`.

   ```console
   (env)$ git checkout main
   (env)$ git pull
   (env)$ git checkout -b "release/$VERSION"
   ```

1. Update the
   [CHANGELOG](https://gitlab.com/clade-public/pyjaniml/-/blob/main/CHANGELOG.md)
   with the new desired version. Also ensure the notes for the new release make
   sense and are coherant. Remember, the target audience for this changelog.

1. Commit the changes an push them. Then open a merge request.

   ```console
   (env)$ git add CHANGELOG.md
   (env)$ git commit -m "Release $VERSION"
   (env)$ git push -o merge_request.create -u origin "release/$VERSION"
   ```

1. Once the merge request has been approved and merged, pull the changes, add a
   git tag and push it:

   ```console
   (env)$ git checkout main
   (env)$ git pull
   (env)$ # If you have a GPG key, please sign the tag:
   (env)$ git tag -s -m "Release $VERSION" "$VERSION"
   (env)$ # If you do not have a GPG key:
   (env)$ git tag -m "Release $VERSION" "$VERSION"
   (env)$ git push --tags
   ```

1. [Check the build pipeline](https://gitlab.com/clade-public/pyjaniml/-/pipelines?scope=tags)
