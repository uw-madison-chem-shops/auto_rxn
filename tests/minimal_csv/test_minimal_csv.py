import pathlib
import os

import auto_rxn


__here__ = pathlib.Path(__file__).parent
happi_db = __here__ / "db.json"


@auto_rxn.with_happi_db(happi_db)
def test_run():
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)


if __name__ == "__main__":
    test_run()
