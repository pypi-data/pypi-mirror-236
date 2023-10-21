from testbrain.core import platform

__version__ = "2023.9.9"
__build__ = "undefined"
__name__ = "appsurify-testbrain-cli"

VERSION = f"{__name__.capitalize()} ({__version__}) [{__build__}]"
RUNTIME = f"{platform.PY_IMPLEMENTATION} {platform.PY_VERSION} on {platform.VERSION}"
