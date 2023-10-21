'''Testing archiver__init__()'''
import sys

from beetools import beearchiver


class TestArchiver:
    def test_msg_display_simple(self):
        """Testing msg_simple()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert (
                beearchiver.msg_display('Display message') == '\x1b[37mDisplay message                               '
            )
        else:
            assert beearchiver.msg_display('Display message') == 'Display message                                    '

    def test_msg_error(self):
        """Testing msg_error()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beearchiver.msg_error('Error message') == '\x1b[31mError message\x1b[0m'
        else:
            assert beearchiver.msg_error('Error message') == 'Error message'

    def test_msg_header(self):
        """Testing msg_header()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beearchiver.msg_header('Header message') == '\x1b[36mHeader message\x1b[0m'
        else:
            assert beearchiver.msg_header('Header message') == 'Header message'

    def test_msg_info(self):
        """Testing msg_info()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beearchiver.msg_info('Info message') == '\x1b[33mInfo message\x1b[0m'
        else:
            assert beearchiver.msg_info('Info message') == 'Info message'

    def test_msg_milestone(self):
        """Testing msg_milestone()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beearchiver.msg_milestone('Milestone message') == '\x1b[35mMilestone message\x1b[0m'
        else:
            assert beearchiver.msg_milestone('Milestone message') == 'Milestone message'

    def test_msg_ok(self):
        """Testing msg_ok()
        ToDO
        Testing the method with PyTest is problematic.  It seems that because the output is intercepted by PyTest, it is
        now seen as writing to a terminal and therefore the test does not work.  For now I keep the skeleton for the
        test, but it is useless and needs further investigation.
        """
        if sys.stdout.isatty():
            assert beearchiver.msg_ok('OK message') == '\x1b[32mOK message\x1b[0m'
        else:
            assert beearchiver.msg_ok('OK message') == 'OK message'
