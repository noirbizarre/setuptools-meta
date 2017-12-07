import json
import pytest
import subprocess
import sys

from textwrap import dedent

from distutils.errors import DistutilsSetupError

from setuptools import Distribution

from setuptools_meta import setup_keyword


class Workspace(object):
    def __init__(self, root, meta):
        self.module_name = 'fake'
        self.root = root
        self.meta_json = root / '{}.egg-info'.format(self.module_name) / 'meta.json'
        self.meta = meta

        self.setup_py = self.write('setup.py', '''\
            from setuptools import setup
            setup(
                name='{module_name}',
                py_modules=['{module_name}'],
                meta={meta}
            )
        ''')

        self.module = self.write('{0}.py'.format(self.module_name), 'print("fake")')

    def write(self, filename, content):
        target = self.root / filename
        with target.open('wb') as f:
            content = dedent(content).format(**self.__dict__)
            f.write(content.encode('utf8'))
        return target

    def chdir(self):
        self.root.chdir()

    def run_setup(self, params):
        cmd = [sys.executable, 'setup.py']
        cmd.extend(params.split())
        return subprocess.call(cmd)


@pytest.fixture
def workspace(request, tmpdir):
    marker = request.node.get_marker('meta')
    meta = marker.args[0] if marker else {}
    wksp = Workspace(tmpdir, meta)
    wksp.chdir()

    yield wksp


def test_setup_keyword_ok():
    dist = Distribution()
    data = {'meta1': 'value1', 'meta2': 'value2'}
    setup_keyword(dist, attr='meta', value=data)


def test_setup_keyword_not_a_dict():
    dist = Distribution()
    with pytest.raises(DistutilsSetupError):
        setup_keyword(dist, attr='meta', value='a string')


@pytest.mark.meta({'key': 'value'})
def test_write_meta_json(workspace):
    assert workspace.run_setup('egg_info') == 0
    assert workspace.meta_json.exists()
    with workspace.meta_json.open() as f:
        data = json.load(f)
    assert data == {'key': 'value'}


@pytest.mark.meta({'key': 'value'})
def test_meta_command(workspace):
    assert workspace.run_setup('meta --key key2 --value value2 egg_info') == 0
    assert workspace.meta_json.exists()
    with workspace.meta_json.open() as f:
        data = json.load(f)
    assert data == {'key': 'value', 'key2': 'value2'}


def test_meta_command_missing_key(workspace):
    assert workspace.run_setup('meta --value value') != 0


def test_meta_command_missing_value(workspace):
    assert workspace.run_setup('meta --key key') != 0
