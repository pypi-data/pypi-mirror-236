'''Testing script__init__()'''
# import configparser
from pathlib import Path

from beetools import beeutils
from beetools import beevenv

# from beetools import beearchiver


# _PROJ_DESC = __doc__.split('\n')[0]
# _PROJ_PATH = Path(__file__)
# _PROJ_NAME = _PROJ_PATH.stem
# _PROJ_VERSION = '0.0.5'


class TestVenv:
    def test_venv_activate(self, self_destruct_work_dir):
        """Testing venv_activate()"""
        if beeutils.get_os() == beeutils.WINDOWS:
            cmd = 'CALL ' + str(self_destruct_work_dir.dir / Path('bee-project_env', 'Scripts', 'activate'))
        else:
            cmd = 'source ' + str(self_destruct_work_dir.dir / Path('bee-project_env', 'bin', 'activate'))
        assert beevenv.activate(self_destruct_work_dir.dir, 'bee-project') == cmd

    def test_venv_do_example(self):
        """Testing venv_do_example()"""
        assert beevenv.do_examples() == 0
        pass

    def test_venv_get_dir(self, self_destruct_work_dir):
        """Testing venv_get_dir()"""
        assert str(beevenv.get_dir(self_destruct_work_dir.dir, 'bee-project')) == str(
            Path(self_destruct_work_dir.dir, 'bee-project_env')
        )

    def test_venv_install_in(self, self_destruct_work_dir):
        """Testing install_in_venv()"""
        project_name = 'new-project'
        beevenv.set_up(beeutils.get_tmp_dir(), project_name, ['pip'], p_verbose=True)
        batch = ['echo Installing in VEnv', 'pip install wheel', 'echo Done!']
        assert beevenv.install_in(self_destruct_work_dir.dir, project_name, batch) == 0
        pass

    def test_venv_set_up(self, self_destruct_work_dir):
        """Testing venv_set_up()"""
        project_name = 'new_project'
        package_list = [['pypi', 'pip'], ['pypi', 'wheel']]
        assert beevenv.set_up(self_destruct_work_dir.dir, project_name, package_list, p_verbose=False) == 0
