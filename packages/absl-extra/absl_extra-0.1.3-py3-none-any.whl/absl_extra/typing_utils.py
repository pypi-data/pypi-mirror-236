import sys

if sys.version_info >= (3, 10):
    from typing import ParamSpec  # noqa
else:
    from typing_extensions import ParamSpec  # noqa
