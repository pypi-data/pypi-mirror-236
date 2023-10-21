"""A tool runner for C++ development."""

from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("xyrha_flush")
except PackageNotFoundError as error:
    raise ModuleNotFoundError("Unable to determine version of package.") from error  # noqa: TRY003, EM101
