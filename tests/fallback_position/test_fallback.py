import pathlib
import os
from unittest.mock import patch, MagicMock, call

import auto_rxn
from auto_rxn import testing


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"

@testing.with_limit_set_to("myfurnace", "lower", float("-inf"))
@testing.with_limit_set_to("myfurnace", "upper", 250.0)
@testing.with_limit_set_to("myfurnace", "fallback", 50.0)
@testing.with_limit_set_to("mymfc", "lower", float("-inf"))
@testing.with_limit_set_to("mymfc", "upper", float("+inf"))
@testing.with_happi_db(happi_db)
def test_fallback():
    furnace = auto_rxn.load_device("myfurnace")
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)
    assert furnace.read()["myfurnace_setpoint"]["value"] == 50.0


if __name__ == "__main__":
    test_fallback()
