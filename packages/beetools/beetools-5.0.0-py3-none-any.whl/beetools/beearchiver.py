from termcolor import colored


# Message defaults
BAR_LEN = 50
MSG_LEN = 50
CRASH_RETRY = 2


def msg_display(p_msg, p_len=MSG_LEN, p_color='white') -> str:
    """Return a text message in white on black.

    Parameters
    ----------
    p_msg
        The message
    p_len
        The fixed length of the message. Default is beetools.MSG_LEN
    p_color
        Color of text, always on black.
            [ grey, red, green, yellow, blue, magenta, cyan, white ]

    Returns
    -------
    str
        Text in the specified color.

    Examples
    --------
    >>> from beetools.beearchiver import msg_display
    >>> msg_display( 'Display message' )
    '\\x1b[37mDisplay message                               '

    """
    msg = colored('{: <{len}}'.format(p_msg, len=p_len), p_color)
    return msg[:p_len] + ' '


def msg_error(p_msg) -> str:
    """Return an "error" text message in red on black

    Parameters
    ----------
    p_msg
        The message

    Returns
    -------
    str
        Text in red on black.

    Examples
    --------
    >>> from beetools.beearchiver import msg_error
    >>> msg_error( 'Error message' )
    '\\x1b[31mError message\\x1b[0m'

    """
    return colored(f'{p_msg}', 'red')


def msg_header(p_msg) -> str:
    """Return a "header" text message in cyan on black

    Parameters
    ----------
    p_msg
        The message

    Returns
    -------
    str
        Text in red on black.

    Examples
    --------
    >>> from beetools.beearchiver import msg_header
    >>> msg_header( 'Header message' )
    '\\x1b[36mHeader message\\x1b[0m'

    """
    return colored(f'{p_msg}', 'cyan')


def msg_info(p_msg) -> str:
    """Return an "information" text message in yellow on black

    Parameters
    ----------
    p_msg
        The message

    Returns
    -------
    str
        Text in red on black.

    Examples
    --------
    >>> from beetools.beearchiver import msg_info
    >>> msg_info( 'Info message' )
    '\\x1b[33mInfo message\\x1b[0m'

    """
    return colored(f'{p_msg}', 'yellow')


def msg_milestone(p_msg) -> str:
    """Return a "milestone" text message in magenta on black

    Parameters
    ----------
    p_msg
        The message

    Returns
    -------
    str
        Text in red on black.

    Examples
    --------
    >>> from beetools.beearchiver import msg_milestone
    >>> msg_milestone( 'Milestone message' )
    '\\x1b[35mMilestone message\\x1b[0m'

    """
    return colored(f'{p_msg}', 'magenta')


def msg_ok(p_msg) -> str:
    """Return an "OK" text message in green on black

    Parameters
    ----------
    p_msg
        The message

    Returns
    -------
    str
        Text in red on black.

    Examples
    --------
    >>> from beetools.beearchiver import msg_ok
    >>> msg_ok( 'OK message' )
    '\\x1b[32mOK message\\x1b[0m'

    """
    return colored(f'{p_msg}', 'green')


def example_messaging():
    """Standard example to illustrate standard use.

    Parameters
    ----------

    Returns
    -------
    bool
        Successful execution [ b_tls.archive_path | False ]

    Examples
    --------

    """
    success = True
    print(
        msg_display(
            f'This message print in blue and cut at {MSG_LEN} character because it is too long!',
            p_color='blue',
        )
    )
    print(msg_ok('This message is an OK message'))
    print(msg_info('This is an info message'))
    print(msg_milestone('This is a milestone message'))
    print(msg_error('This is a warning message'))
    return success


def do_examples(p_cls=True):
    return example_messaging()


if __name__ == '__main__':
    do_examples()
