# import the main window object (mw) from aqt
from functools import partial
from aqt import mw
import aqt.editor
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from aqt import gui_hooks
from aqt.qt import QColor

BLUE = "#2a74ff"
GREEN = "#00aa00"
PINK = "#fd6d85"
RED = "#c12d30"


def change_color(editor: aqt.editor.Editor, color: str, bold: bool = False) -> None:
    editor.web.eval("setFormat('removeFormat');")
    if bold:
        editor.web.eval("setFormat('bold');")

    editor.web.eval(f"setFormat('forecolor', '{color}');")


def add_shortcuts(shortcuts: list[tuple], editor: aqt.editor.Editor) -> None:
    shortcuts.append(("F2", partial(change_color, editor, BLUE, bold=True)))
    shortcuts.append(("F3", partial(change_color, editor, GREEN, bold=True)))
    shortcuts.append(("F4", partial(change_color, editor, PINK, bold=True)))
    shortcuts.append(("F5", partial(change_color, editor, RED, bold=True)))
    shortcuts.append(("Shift+F2", partial(change_color, editor, BLUE, bold=False)))
    shortcuts.append(("Shift+F3", partial(change_color, editor, GREEN, bold=False)))
    shortcuts.append(("Shift+F4", partial(change_color, editor, PINK, bold=False)))
    shortcuts.append(("Shift+F5", partial(change_color, editor, RED, bold=False)))


# https://addon-docs.ankiweb.net/hooks-and-filters.html
gui_hooks.editor_did_init_shortcuts.append(add_shortcuts)
