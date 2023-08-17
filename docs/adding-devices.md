# adding devices

Auto-rxn has been built to be as flexible as possible in accepting devices.
Any device supporting [Bluesky protocols](https://blueskyproject.io/bluesky/hardware) should work, including a growing ecosystem of [hardware interface packages](https://blueskyproject.io/bluesky/hardware-interfaces).

Auto-rxn relies on [HAPPI](https://pcdshub.github.io/happi/) for device-discovery.
HAPPI provides a persistant database of what devices are avaliable on a given machine, and how to construct a Python interface to each device.
When running from a recipe file, auto-rxn queries HAPPI for devices according to their `Control Point ID`.
Sometimes it's useful to interact directly with HAPPI when managing devices for auto-rxn.
Refer to the HAPPI documentation for more, or on the command line type.

```bash
$ happi --help
```

## initializing HAPPI on a new machine

At minimum, HAPPI needs a configuration file and a database file to operate.
You can quickly create these files in their default locations by typing the following into the command line.

```bash
$ happi config init
```

If your database is broken and you want to start fresh, you can do so using the following flag.
Be careful, as this will delete your current database!

```bash
$ happi config init --overwrite
```

## populating a database from yaq

For yaq devices, there is a special integration between yaqd-control and HAPPI that makes populating the HAPPI database simple.

```bash
$ yaqd list --format happi | happi update -
```

You can safely repeat this command whenever you add or change a yaq daemon.

## interacting with the HAPPI database

Auto-rxn users will find it useful to know a few basic ways of interacting with the HAPPI database.

To list all entries in the HAPPI databse:

```bash
$ happi search "*"
```

To drop into an iPython shell with all devices loaded:

```bash
$ happi load "$(happi search "*" --names)"
```

