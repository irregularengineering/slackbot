"""
String utils
"""


def pluralize(count: int) -> str:
    """
    Return 's' as long as count is not 1

    :param count: as int
    :return:
    """
    return '' if count == 1 else 's'
