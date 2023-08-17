# installation

## conda-forge (recommended)

The conda package manager is recommended for scientists wanting access to Python tools. If you're just getting started with Python, we recommend miniconda.

<https://docs.conda.io/en/latest/miniconda.html>

Once conda is installed on your machine, you can install auto-rxn. On a Windows machine, use Anaconda Prompt for these commands.

```bash
$ conda config --add channels conda-forge
$ conda install auto_rxn
```

If you installed a previous version of auto-rxn using conda, you can update using the following command.

```bash
$ conda update auto_rxn
```

## PyPI

Auto-rxn is also avaliable from Python's default package manager, pip.

```bash
$ python -m pip install auto_rxn
```

If you installed a previous version of auto-rxn from PyPI, you can update using the following command.

```bash
$ python -m pip install -U auto_rxn
```