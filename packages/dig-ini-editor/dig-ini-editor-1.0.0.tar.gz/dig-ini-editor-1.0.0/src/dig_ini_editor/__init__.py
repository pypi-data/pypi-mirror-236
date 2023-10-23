from sys import version_info as sys_version_info


def __get_version() -> str:
    if sys_version_info < (3, 8):
        from pkg_resources import get_distribution  # pylint: disable=import-outside-toplevel

        return get_distribution("dig-ini-editor").version

    from importlib.metadata import version as importlib_version  # pylint: disable=import-outside-toplevel

    return importlib_version("dig-ini-editor")


__version__ = __get_version()
