import pathlib
import os

import auto_rxn
from auto_rxn import testing


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"


@testing.with_limit_set_to("myfurnace", "lower", float("-inf"))
@testing.with_limit_set_to("myfurnace", "upper", float("+inf"))
@testing.with_limit_set_to("mymfc", "lower", float("-inf"))
@testing.with_limit_set_to("mymfc", "upper", float("+inf"))
@testing.with_happi_db(happi_db)
def test_run():
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)


if __name__ == "__main__":
    test_run()
