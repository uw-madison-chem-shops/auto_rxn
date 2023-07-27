import pathlib
import os
from unittest.mock import patch, MagicMock, call

import auto_rxn
from auto_rxn.devices import Status


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"


@auto_rxn.with_happi_db(happi_db)
def test_fallback():
    furnace = auto_rxn.load_device("myfurnace")
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)
    assert furnace.read()["myfurnace_setpoint"]["value"] == 50.0


if __name__ == "__main__":
    test_fallback()
