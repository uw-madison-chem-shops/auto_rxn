import pathlib
import os
from unittest.mock import patch, MagicMock, call

import auto_rxn
from auto_rxn.devices import Status


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"


@auto_rxn.with_happi_db(happi_db)
def test_ramp_time_called():
    furnace = auto_rxn.load_device("myfurnace")
    furnace.ramp_time.set = MagicMock(side_effect=furnace.ramp_time.set)
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)
    assert call(0.0) == furnace.ramp_time.set.mock_calls.pop(0)
    assert call(0.1) == furnace.ramp_time.set.mock_calls.pop(0)
    assert call(0.2) == furnace.ramp_time.set.mock_calls.pop(0)
    assert call(0.3) == furnace.ramp_time.set.mock_calls.pop(0)


if __name__ == "__main__":
    test_ramp_time_called()
