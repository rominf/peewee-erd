peewee ERD
==========

Draw ER diagram based on peewee models.

This project is heavily based on https://github.com/gustavi/peewee-graph-models.

Installation
------------

To install the peewee ERD use `pip`:

```shell
$ pip install peewee-erd
```

To install the peewee ERD with live view use `pip` with extras:

```shell
$ pip install peewee-erd[live-view]
```

Usage
-----

To draw the diagram, display, and update it on file changes, run it with the path of models file:
```shell
$ PATH_OF_MODELS_FILE=...
$ peewee-erd $PATH_OF_MODELS_FILE
```

For more other variants of usage see help:
```shell
$ peewee-erd --help
```
