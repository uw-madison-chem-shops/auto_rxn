__all__ = ["with_happi_db"]


import pathlib

import platformdirs
import happi  # type: ignore

from auto_rxn import _device as auto_rxn_happi


def with_happi_db(path):
    def decorator(function):
        def wrapper():
            # make happi client
            auto_rxn_happi.db_path = path
            auto_rxn_happi.happi_backend = happi.backends.backend(path)
            auto_rxn_happi.happi_client = happi.Client(database=auto_rxn_happi.happi_backend)
            auto_rxn_happi.device_singletons = dict()

            function()

            # make happi client
            auto_rxn_happi.db_path = platformdirs.user_data_path("happi") / "db.json"
            db_path = platformdirs.user_data_path("happi") / "db.json"
            auto_rxn_happi.happi_backend = happi.backends.backend(db_path)
            auto_rxn_happi.happi_client = happi.Client(database=auto_rxn_happi.happi_backend)

        return wrapper

    return decorator
