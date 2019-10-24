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

To draw the diagram run it with the path of models file:
```shell
$ peewee-erd <paths_of_models_files>...
```

For other variants of usage see help:
```shell
$ peewee-erd --help
```

Example output
--------------

This is the ER diagram generated for [conceptnet-lite](https://github.com/ldtoolkit/conceptnet-lite):
![ER diagram for conceptnet-lite](https://raw.githubusercontent.com/ldtoolkit/conceptnet-lite/master/docs/source/_static/erd.svg?sanitize=true)
