__all__ = ["with_happi_db"]


import pathlib

import appdirs
import happi  # type: ignore

from . import _happi as auto_rxn_happi


def with_happi_db(path):
    def decorator(function):
        def wrapper():
            # make happi client
            auto_rxn_happi.happi_backend = happi.backends.backend(path)
            auto_rxn_happi.happi_client = happi.Client(database=auto_rxn_happi.happi_backend)

            function()

            # make happi client
            db_path = pathlib.Path(appdirs.user_data_dir("happi")) / "d"
            auto_rxn_happi.happi_backend = happi.backends.backend(db_path)
            auto_rxn_happi.happi_client = happi.Client(database=auto_rxn_happi.happi_backend)

        return wrapper

    return decorator
