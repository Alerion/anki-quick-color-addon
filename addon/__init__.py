from functools import partial
import aqt.editor
from aqt import gui_hooks

RED = "#c12d30"


def change_color(editor: aqt.editor.Editor, color: str, bold: bool = False) -> None:
    editor.web.eval("setFormat('removeFormat')")
    if bold:
        editor.web.eval("setFormat('bold')")

    editor.web.eval(f"setFormat('forecolor', '{color}')")


def insert_der(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #2a74ff;"><b>der </b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_die(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #fd6d85;"><b>die </b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_das(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #00aa00;"><b>das </b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_noun(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #3d405b;"><b>NOUN</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_verb(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #e07a5f;"><b>VERB</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_adjective(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #81b29a;"><b>ADJECTIVE</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_adverb(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #d68c45;"><b>ADVERB</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_pronoun(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #98c1d9;"><b>PRONOUN</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def add_shortcuts(shortcuts: list[tuple], editor: aqt.editor.Editor) -> None:
    shortcuts.append(("F2", partial(change_color, editor, RED, bold=True)))

    shortcuts.append(("F3", partial(insert_der, editor)))
    shortcuts.append(("F4", partial(insert_die, editor)))
    shortcuts.append(("F5", partial(insert_das, editor)))

    shortcuts.append(("F6", partial(insert_noun, editor)))
    shortcuts.append(("F7", partial(insert_verb, editor)))
    shortcuts.append(("F8", partial(insert_adjective, editor)))
    shortcuts.append(("F9", partial(insert_adverb, editor)))
    shortcuts.append(("F10", partial(insert_pronoun, editor)))


# https://addon-docs.ankiweb.net/hooks-and-filters.html
gui_hooks.editor_did_init_shortcuts.append(add_shortcuts)
