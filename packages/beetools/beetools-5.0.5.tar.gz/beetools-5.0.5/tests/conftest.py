import datetime
from pathlib import Path
from tempfile import mkdtemp

import pytest

from beetools.beeutils import rm_tree


class SetUpParams:
    def __init__(self, p_type):
        self.dir = WorkingDir().dir
        self.app_desc = 'Test application description'
        self.app_dir = None
        self.app_name = 'TestApp'
        self.app_ver = '0.0.0'
        self.app_type = p_type
        self._setup_env()

    def _setup_env(self):
        '''Setup the environment base structure.'''
        app_root_dir = Path(self.dir, self.app_name)
        if self.app_type == 'module':
            self.app_dir = Path(app_root_dir, 'src', self.app_name.lower())
        elif self.app_type == 'tests':
            self.app_dir = Path(app_root_dir, 'tests')
        elif self.app_type == 'site-package':
            self.app_dir = Path(
                self.dir,
                'site-packages',
                self.app_name.lower(),
                self.app_name.lower(),
            )
            app_root_dir = self.app_dir
        elif self.app_type == 'package':
            self.app_dir = Path(app_root_dir, self.app_name.lower())
        self.app_dir.mkdir(parents=True)
        app_ver_arc_dir = app_root_dir / 'VersionArchive'
        app_ver_arc_dir.mkdir()
        app_arc_dir = app_root_dir / 'Archive'
        app_arc_dir.mkdir()
        app_pth = self.app_dir / Path(self.app_name.lower()).with_suffix('.py')
        app_pth.touch()
        (self.app_dir / Path(self.app_name.lower()).with_suffix('.ini')).touch()
        (self.app_dir / Path(self.app_name.lower()).with_suffix('.txt')).touch()
        start_time = datetime.datetime.now()
        start_date_str = start_time.strftime('%y%m%d%H%M%S')
        (app_ver_arc_dir / f'{self.app_name} {start_date_str} ({self.app_ver} Beta).zip').touch()
        (app_arc_dir / Path(self.app_name.lower()).with_suffix('.py')).touch()


class WorkingDir:
    def __init__(self):
        self.dir = Path(mkdtemp(prefix='beetools_'))


@pytest.fixture
def self_destruct_work_dir():
    """Set up the environment base structure"""
    sup = WorkingDir()
    yield sup
    rm_tree(sup.dir, p_crash=False)


@pytest.fixture
def setup_env_module():
    sup = SetUpParams('module')
    yield sup
    rm_tree(sup.dir, p_crash=False)


@pytest.fixture
def setup_env_tests():
    sup = SetUpParams('tests')
    yield sup
    rm_tree(sup.dir, p_crash=False)


@pytest.fixture
def setup_env_sitepackage():
    sup = SetUpParams('site-package')
    yield sup
    rm_tree(sup.dir, p_crash=False)


@pytest.fixture
def setup_env_package():
    sup = SetUpParams('package')
    yield sup
    rm_tree(sup.dir, p_crash=False)
