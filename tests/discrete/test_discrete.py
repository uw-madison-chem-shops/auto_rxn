import pathlib
import os
from unittest.mock import patch, MagicMock, call
from yaqd_core import testing as yct

import auto_rxn
from auto_rxn import testing


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"


@yct.run_daemon_entry_point("fake-continuous-hardware", config=__here__ / "continuous-config.toml")
@yct.run_daemon_entry_point("fake-discrete-hardware", config=__here__ / "discrete-config.toml")
@testing.with_happi_db(happi_db)
def test_fallback():
    discrete = auto_rxn.load_device("discrete")
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)
    assert discrete.read()["discrete_position_identifier"]["value"] == "blue"


if __name__ == "__main__":
    test_fallback()
