import pathlib
import auto_rxn


__here__ = pathlib.Path(__file__).parent


def test_run():
    path = __here__ / "recipe.csv"
    recipe = auto_rxn.Recipe(path)
    auto_rxn.run(recipe)


if __name__ == "__main__":
    test_run()
