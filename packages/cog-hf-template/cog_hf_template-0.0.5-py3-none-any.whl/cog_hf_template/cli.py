import fire

from . import __version__
from .download_utils import mirror_weights


def main(args=None):
    return fire.Fire({"mirror-weights": mirror_weights, "version": lambda: print(__version__)})
