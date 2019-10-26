#!/usr/bin/env python
"""peewee ERD.

Usage:
  peewee-erd [--output=<file>] [--main-color=<color>] [--bg-color=<color>] [--font-size=<pt>] <path_of_models_file>...
  peewee-erd -h | --help

Options:
  -h --help                  Show this screen.
  -o=<file> --output=<file>  Save generated model to file (disables [live] view).
  --main-color=<color>       Main color used for models background and fields names [default: #0b7285].
  --bg-color=<color>         Background of models [default: #e3fafc].
  --font-size=<pt>           Font size [default: 12].
"""
import time
from contextlib import suppress
from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Collection, Union, Callable, List
import importlib.util
import inspect
from uuid import uuid4

try:
    from PySide2.QtCore import QRectF
    from PySide2.QtGui import QPainter
    from PySide2.QtSvg import QSvgWidget
    from PySide2.QtWidgets import QApplication
    PYSIDE2_AVAILABLE = True
except ImportError:
    PYSIDE2_AVAILABLE = False

from dataclasses import dataclass
from docopt import docopt
from jinja2 import Template
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import graphviz
import peewee


@dataclass
class Field:
    name: str
    type: str
    color: str


@dataclass
class Model:
    name: str
    fields: List[Field]
    bg_color: str
    main_color: str


@dataclass
class Relation:
    model: str
    target_model: str
    field: str
    target_field: str


@dataclass
class Graph:
    models: List[Model]
    relations: List[Relation]
    font_size: int


class DrawOnFileChangesHandler(FileSystemEventHandler):
    def __init__(
            self,
            paths_of_models_files: Collection[Union[Path, str]],
            draw_function: Callable,
            svg_widget: 'QSvgWidget',
            output: Union[Path, str],
    ):
        self._draw_function = draw_function
        self._paths_of_models_files = [Path(path_of_models_file) for path_of_models_file in paths_of_models_files]
        self._svg_widget = svg_widget
        self._output = output

    def on_modified(self, event):
        if Path(event.src_path) in self._paths_of_models_files:
            try:
                self._draw_function()
                self._svg_widget.load(self._output)
            except ImportError:
                pass


def draw(
        paths_of_models_files: Collection[Union[Path, str]],
        output: Union[Path, str],
        main_color: str,
        bg_color: str,
        font_size: int,
        view: bool,
        cleanup: bool,
):
    """
    Draw ER diagram based on peewee models.
    """
    models_modules = []
    try:
        for path_of_model_file in paths_of_models_files:
            spec = importlib.util.spec_from_file_location('models', path_of_model_file)
            models_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(models_module)
            models_modules.append(models_module)
    except:
        raise ImportError()

    def is_peewee_model(obj) -> bool:
        """Check if the object is a peewee model."""
        return (inspect.isclass(obj) and
                issubclass(obj, peewee.Model) and
                not obj == peewee.Model and
                not obj.__name__.startswith('_'))

    relations = []
    models = []

    for models_module in models_modules:
        for name, model in inspect.getmembers(models_module, predicate=is_peewee_model):
            fields = []

            # noinspection PyProtectedMember
            for field, obj in model._meta.fields.items():
                fields.append(Field(
                    name=field,
                    type=type(obj).__name__,
                    color=main_color,
                ))

                if isinstance(obj, peewee.ForeignKeyField):
                    relations.append(Relation(
                        model=name,
                        target_model=obj.rel_model.__name__,
                        field=field,
                        target_field=obj.rel_field.name,
                    ))

            models.append(Model(
                name=name,
                fields=fields,
                bg_color=bg_color,
                main_color=main_color,
            ))

    graph_template = Template(open(Path(__file__).parent / 'erd.dot').read())
    graph_dot = graph_template.render(graph=Graph(
        models=models,
        relations=relations,
        font_size=font_size,
    ))

    # Render graph
    output = Path(output)
    src = graphviz.Source(
        source=graph_dot,
        filename=output.with_suffix(''),
        format=output.suffix[1:],
    )
    src.render(
        view=view,
        cleanup=cleanup,
    )


def start_live_view(
        draw_function: Callable,
        paths_of_models_files: Collection[Union[Path, str]],
        output: Union[Path, str]
):
    class SvgWidget(QSvgWidget):
        def paintEvent(self, paint_event):
            painter = QPainter(self)
            default_width, default_height = self.renderer().defaultSize().toTuple()
            widget_width, widget_height = self.size().toTuple()
            ratio_x = widget_width / default_width
            ratio_y = widget_height / default_height
            if ratio_x < ratio_y:
                new_width = widget_width
                new_height = widget_width * default_height / default_width
                new_left = 0
                new_top = (widget_height - new_height) / 2
            else:
                new_width = widget_height * default_width / default_height
                new_height = widget_height
                new_left = (widget_width - new_width) / 2
                new_top = 0
            self.renderer().render(painter, QRectF(new_left, new_top, new_width, new_height))

    app = QApplication()
    svg_widget = SvgWidget(output)
    svg_widget.setWindowTitle("peewee ERD")
    svg_widget.show()

    file_changes_observer = Observer()
    draw_on_file_changes_handler = DrawOnFileChangesHandler(
        paths_of_models_files=paths_of_models_files,
        draw_function=draw_function,
        svg_widget=svg_widget,
        output=output,
    )
    for path_of_models_file in paths_of_models_files:
        file_changes_observer.schedule(
            event_handler=draw_on_file_changes_handler,
            path=str(path_of_models_file.parent),
        )
    file_changes_observer.start()

    app.exec_()
    file_changes_observer.stop()
    file_changes_observer.join()


def main():
    args = docopt(__doc__)
    paths_of_models_files = [Path(path_of_models_file) for path_of_models_file in args['<path_of_models_file>']]
    output = args['--output']
    view = output is None and not PYSIDE2_AVAILABLE
    live_view = output is None and PYSIDE2_AVAILABLE
    if output is None:
        output_tmp_dir = TemporaryDirectory()
        output = str(Path(output_tmp_dir.name) / f'{uuid4()}.svg')
    backed_draw = partial(
        draw,
        paths_of_models_files=paths_of_models_files,
        main_color=args['--main-color'],
        bg_color=args['--bg-color'],
        font_size=int(args['--font-size']),
        output=output,
        view=view,
        cleanup=not view,
    )
    backed_draw()
    if live_view:
        start_live_view(
            draw_function=backed_draw,
            paths_of_models_files=paths_of_models_files,
            output=output,
        )
    if view:
        with suppress(KeyboardInterrupt):
            while True:
                time.sleep(1)


if __name__ == '__main__':
    main()
