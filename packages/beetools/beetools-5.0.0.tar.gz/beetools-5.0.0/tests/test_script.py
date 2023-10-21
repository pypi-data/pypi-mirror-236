from beetools import beescript
from beetools import beeutils


class TestScript:
    def test__do_example(self):
        """Testing script_do_example()"""
        assert beescript.do_examples()
        pass

    def test__exec_batch(self, self_destruct_work_dir):
        """Testing script_exec_batch()"""

        tmp_test = self_destruct_work_dir.dir / 'test'
        tmp_t1 = tmp_test / 'T1'
        cmds = []
        if beeutils.get_os() in [beeutils.LINUX, beeutils.MACOS]:
            cmds = [
                ['mkdir', '-p', f'{tmp_t1}'],
                ['ls', '-l', f'{tmp_test}'],
            ]
        elif beeutils.get_os() == beeutils.WINDOWS:
            cmds = [
                ['md', f'{tmp_t1}'],
                ['dir', '/B', f'{tmp_test}'],
            ]
        assert beescript.exec_batch(cmds, p_verbose=False) == [0, 0]
        pass

    def test__exec_batch_in_session(self, self_destruct_work_dir):
        """Testing script_exec_batch_in_session()"""
        tmp_test = self_destruct_work_dir.dir / 'test'
        tmp_t1 = tmp_test / 'T1'
        batch = []
        if beeutils.get_os() in [beeutils.LINUX, beeutils.MACOS]:
            batch = [
                f'mkdir -p {tmp_t1}',
                f'ls -l {tmp_test}',
                f'rm -R {tmp_test}',
            ]
        elif beeutils.get_os() == beeutils.WINDOWS:
            batch = [
                f'md {tmp_t1}',
                f'dir /B {tmp_test}',
                f'rd /Q /S {tmp_test}',
            ]
        assert beescript.exec_batch_in_session(batch, p_verbose=False) == 0
        pass

    def test__exec_cmd(self, self_destruct_work_dir):
        """Testing script_exec_cmd()"""
        tmp_dir = self_destruct_work_dir.dir / 'test' / 'T1'
        if beeutils.get_os() in [beeutils.LINUX, beeutils.MACOS]:
            cmd1 = ['mkdir', '-p', f'{tmp_dir}']
            cmd2 = ['touch', f'{tmp_dir}/t.txt']
            cmd3 = ['rmdir', f'{tmp_dir}']
        else:
            cmd1 = ['md', f'{tmp_dir}']
            cmd2 = ['echo.', '>>', f'{tmp_dir}\\t.txt']
            cmd3 = ['rd', f'{tmp_dir}']
        assert beescript.exec_cmd(cmd1) == 0
        assert beescript.exec_cmd(cmd2) == 0
        assert beescript.exec_cmd(cmd3) != 0  # Attempt to remove non-empty directory to create exception

        pass

    def test__write_script(self, self_destruct_work_dir):
        """Testing script_exec_batch()"""
        script_pth = self_destruct_work_dir.dir / __name__
        cmds = [
            ['echo', 'Hello'],
            ['echo', 'Goodbye'],
        ]
        assert beescript.write_script(script_pth, cmds) == 'echo Hello\necho Goodbye\n'
        pass
