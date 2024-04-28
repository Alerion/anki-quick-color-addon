"""
`setFormat` triggers one of these commands:

https://developer.mozilla.org/en-US/docs/Web/API/document/execCommand
"""
import sys
import os.path

# Inject external dependencies.
DEPENDENCIES_PATH = os.path.join(os.path.dirname(__file__), '../dependencies')
sys.path.insert(0, DEPENDENCIES_PATH)

from functools import partial
import aqt.editor
from aqt import gui_hooks

from .wiktionary import get_word_wikitext, get_audio_url_from_wikitext, get_ipa_from_wikitext

RED = "#c12d30"


def change_color(editor: aqt.editor.Editor, color: str, bold: bool = False) -> None:
    editor.web.eval("setFormat('removeFormat')")
    if bold:
        editor.web.eval("setFormat('bold')")

    editor.web.eval(f"setFormat('forecolor', '{color}')")


def insert_template(editor: aqt.editor.Editor) -> None:
    html = '<h2>word</h2>[ipa]'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_der(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #2a74ff; font-size: inherit;"><b>der&nbsp;</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_die(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #fd6d85; font-size: inherit;"><b>die&nbsp;</b></span>'
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


def insert_das(editor: aqt.editor.Editor) -> None:
    html = '<span style="color: #00aa00; font-size: inherit;"><b>das&nbsp;</b></span>'
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


def insert_word_description(editor: aqt.editor.Editor, only_audio: bool = False) -> None:
    clipboard = editor.mw.app.clipboard()
    word = clipboard.text().strip()

    if not word:
        print("No word found in clipboard")
        return

    wikitext = get_word_wikitext(word)
    if not wikitext:
        print(f"No wikitext found for: {word}")
        return

    audio_url = get_audio_url_from_wikitext(wikitext)

    if not only_audio:
        # Load IPA
        ipa = get_ipa_from_wikitext(wikitext)
        # TODO: Add article.
        # Insert word
        html = f'<h2>{word}</h2>[{ipa}]'
        editor.web.eval(f"setFormat('insertHTML', '{html}')")
        # Can't paste new line with insertHTML.
        audio_url = f"\n{audio_url}"

    # Insert audio
    if audio_url:
        clipboard.setText(audio_url)
        # Trigger audio paste, so Anki can replace with proper tag.
        editor.onPaste()

        clipboard.setText(word)
    else:
        print(f"Audio file was not found for: {word}")


    # Get selected text.
    # def callback(*args, **kwargs):
    #     print(args, kwargs)
    # editor.web.evalWithCallback("window.getSelection().toString()", callback)


def add_shortcuts(shortcuts: list[tuple], editor: aqt.editor.Editor) -> None:
    shortcuts.append(("F1", partial(insert_word_description, editor)))
    # For edit page. F1 does not work.
    shortcuts.append(("F12", partial(insert_word_description, editor)))
    shortcuts.append(("F2", partial(insert_der, editor)))
    shortcuts.append(("F3", partial(insert_die, editor)))
    shortcuts.append(("F4", partial(insert_das, editor)))

    shortcuts.append(("F5", partial(change_color, editor, RED, bold=True)))

    shortcuts.append(("F6", partial(insert_noun, editor)))
    shortcuts.append(("F7", partial(insert_verb, editor)))
    shortcuts.append(("F8", partial(insert_adjective, editor)))
    shortcuts.append(("F9", partial(insert_adverb, editor)))
    shortcuts.append(("F10", partial(insert_pronoun, editor)))
    shortcuts.append(("Alt+F1", partial(insert_word_description, editor, only_audio=True)))


# https://addon-docs.ankiweb.net/hooks-and-filters.html
gui_hooks.editor_did_init_shortcuts.append(add_shortcuts)
