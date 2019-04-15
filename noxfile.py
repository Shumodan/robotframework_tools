import os

from pathlib import Path

import nox


UPLOAD_TEST_URL = 'https://test.pypi.org/legacy/'

pkg_creds = Path('.upload.cred')

if pkg_creds.exists():
    with pkg_creds.open('r') as file:
        UPLOAD_USER, UPLOAD_PASS = file.read().strip('\n').split('::')
else:
    UPLOAD_USER = os.getenv('UPLOAD_USER')
    UPLOAD_PASS = os.getenv('UPLOAD_PASSWORD')


def install(*args):
    def deco(function):
        def wrapper(session, *params):
            for item in args:
                session.install(item)
            function(session, *params)
        return wrapper
    return deco


@install('flake8')
def lint(session):
    session.run('flake8', './robotframework_rp_tools')


@install('wheel')
def build(session):
    session.install('-r', 'install_requires.txt')
    session.run('python', 'setup.py', 'sdist', 'bdist_wheel')


@install('twine')
def upload(session, url=None):
    cmd = [
        'twine', 'upload',
        '--username', UPLOAD_USER,
        '--password', UPLOAD_PASS,
        'dist/*'
    ]
    if url:
        cmd.insert(-1, '--repository-url')
        cmd.insert(-1, url)
    session.run(*cmd)


def base_steps(session, url):
    lint(session)
    build(session)
    upload(session, url)


@nox.session
def test(session):
    base_steps(session, UPLOAD_TEST_URL)


@nox.session
def prod(session):
    base_steps(session)
