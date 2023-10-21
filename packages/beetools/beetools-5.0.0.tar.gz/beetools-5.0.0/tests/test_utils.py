import configparser
import sys
from pathlib import Path

from beetools import beescript
from beetools import beeutils


class TestUtils:
    def test_tools_constants(self):
        """Assert class constants"""
        assert beeutils.DEF_LOG_LEV == 10
        assert beeutils.DEF_LOG_LEV_FILE == 10
        assert beeutils.DEF_LOG_LEV_CON == 30
        assert beeutils.LOG_FILE_FORMAT == '%(asctime)s%(msecs)d;%(levelname)s;%(name)s;%(funcName)s;%(message)s'
        assert (
            beeutils.LOG_CONSOLE_FORMAT == '\x1b[0;31;40m\n%(levelname)s - %(name)s - %(funcName)s - %(message)s\x1b[0m'
        )

        # Def date format strings
        assert beeutils.LOG_DATE_FORMAT == '%Y%m%d%H%M%S'
        assert beeutils.LONG_DATE_FORMAT == '%Y%m%d'
        assert beeutils.TIME_FORMAT == '%H%M%S'

        # Def message constants
        assert beeutils.BAR_LEN == 50
        assert beeutils.MSG_LEN == 50
        assert beeutils.CRASH_RETRY == 2

        # Operating system name defaults
        assert beeutils.WINDOWS == 'windows'
        assert beeutils.LINUX == 'linux'
        assert beeutils.MACOS == 'macos'
        assert beeutils.AIX == 'aix'

    def test_tools_do_examples(self):
        """Testing msg_do_examples()"""
        assert beeutils.do_examples()

    def test_get_os(self):
        """Testing get_os()"""
        if sys.platform.startswith('win32'):
            curr_os = 'windows'
        elif sys.platform.startswith('linux'):
            curr_os = 'linux'
        else:
            curr_os = 'macos'
        assert beeutils.get_os() == curr_os

    def test_get_tmp_dir(self):
        """Testing get_tmp_dir()"""
        assert beeutils.get_tmp_dir().exists()
        assert beeutils.get_tmp_dir('beeutils_').exists()
        pass

    def test_tools_is_struct_the_same_list_eq(self):
        """Testing is_struct_the_same_list_eq()"""
        x = [1, 2]
        y = [1, 2]
        assert beeutils.is_struct_the_same(x, y)

    def test_tools_is_struct_the_same_dict_eq(self):
        """Testing is_struct_the_same_dict_eq()"""
        x = {1: 'One', 2: 'Two'}
        y = {2: 'Two', 1: 'One'}
        assert beeutils.is_struct_the_same(x, y)

    def test_tools_is_struct_the_same_dict_diff_keys(self):
        """Testing is_struct_the_same_dict_diff_keys()"""
        x = {1: 'One', 3: 'Two'}
        y = {1: 'One', 2: 'Two'}
        assert not beeutils.is_struct_the_same(x, y)

    def test_tools_is_struct_the_same_dict_neq(self):
        """Testing is_struct_the_same_dict_neq()"""
        y = {2: 'Two', 1: 'One'}
        z = {2: 'Two', 1: 'Three'}
        assert not beeutils.is_struct_the_same(y, z, 'ref str')

    def test_tools_is_struct_the_same_len(self):
        """Testing is_struct_the_same_len()"""
        x = [1, 2]
        y = [1, 2, 3]
        assert not beeutils.is_struct_the_same(x, y)

    def test_tools_result_rep_true(self):
        """Testing tools_result_rep_true()
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beeutils.result_rep(True) == 'test_tools_result_rep_true - \x1b[32mSuccess\x1b[0m (No Comment)'
        else:
            assert beeutils.result_rep(True) == 'test_tools_result_rep_true - Success (No Comment)'

    def test_tools_result_rep_false(self):
        """Testing tools_result_rep_false()
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beeutils.result_rep(False) == 'test_tools_result_rep_false - \x1b[31mFailed\x1b[0m (No Comment)'
        else:
            assert beeutils.result_rep(False) == 'test_tools_result_rep_false - Failed (No Comment)'

    def test_tools_rm_temp_locked_file(self):
        """Testing tools_rm_temp_locked_file()"""
        tmp_test = beeutils.get_tmp_dir() / 'test'
        assert beeutils.rm_temp_locked_file(tmp_test)

    def test_tools_rm_tree(self, self_destruct_work_dir):
        """Testing tools_rm_tree()"""
        working_dir = self_destruct_work_dir.dir
        tmp_t1 = Path(working_dir, 'T1')
        if beeutils.get_os() == beeutils.WINDOWS:
            cmd = [f'md {tmp_t1}']
        else:
            cmd = [f'mkdir -p {tmp_t1}']
        beescript.exec_batch_in_session(cmd, p_verbose=False)
        t_file = working_dir / Path('t.tmp')
        t_file.touch(mode=0o666, exist_ok=True)
        t_file = tmp_t1 / Path('t.tmp')
        t_file.touch(mode=0o666, exist_ok=True)
        assert beeutils.rm_tree(working_dir, p_crash=True)
        pass

    def test_select_os_dir_from_config_simple(self):
        """Testing select_os_dir_from_config_simple()"""
        cnf = configparser.ConfigParser()
        cnf.read_dict(
            {
                'Folders': {
                    'windows1_MyFolderOnSystem': 'c:\\Program Files',
                    'windows2_MyFolderOnSystem': 'c:\\Program Files (x86)',
                    'linux1_MyFolderOnSystem': '/usr/local/bin',
                    'linux2_MyFolderOnSystem': '/bin',
                    'macos1_MyFolderOnSystem': '/System',
                    'macos2_MyFolderOnSystem': '/Application',
                }
            }
        )
        if beeutils.get_os() == beeutils.LINUX:
            bee_dir = '/usr/local/bin'
        elif beeutils.get_os() == beeutils.WINDOWS:
            bee_dir = 'c:\\Program Files'
        else:
            bee_dir = '/System'
        assert str(beeutils.select_os_dir_from_config(cnf, 'Folders', 'MyFolderOnSystem')) == bee_dir
