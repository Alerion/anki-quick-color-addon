"""
`setFormat` triggers one of these commands:

https://developer.mozilla.org/en-US/docs/Web/API/document/execCommand
"""

import sys
import os.path

# Inject external dependencies.
DEPENDENCIES_PATH = os.path.join(os.path.dirname(__file__), "./dependencies")
sys.path.insert(0, DEPENDENCIES_PATH)

from functools import partial
import aqt.editor
from aqt import gui_hooks
from aqt.utils import showInfo
from aqt import mw

from .wiktionary import (
    find_word_page,
    get_page_wikitext,
    get_audio_url_from_wikitext,
    get_ipa_from_wikitext,
    get_speach_part_from_wikitext,
    SpeachPart,
    get_gender_from_wikitext,
    Gender,
    get_plural_from_wikitext,
    get_genitive_from_wikitext,
    get_examples_from_wikitext,
)
from .translation import get_uk_translation

RED = "#c12d30"


def change_color(editor: aqt.editor.Editor, color: str, bold: bool = False) -> None:
    editor.web.eval("setFormat('removeFormat')")
    if bold:
        editor.web.eval("setFormat('bold')")

    editor.web.eval(f"setFormat('forecolor', '{color}')")


def insert_template(editor: aqt.editor.Editor) -> None:
    html = "<h2>word</h2>[ipa]"
    editor.web.eval(f"setFormat('insertHTML', '{html}')")


DER_TEXT = '<span style="color: #2a74ff; font-size: inherit;"><b>der&nbsp;</b></span>'


def insert_der(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{DER_TEXT}')")


DIE_TEXT = '<span style="color: #fd6d85; font-size: inherit;"><b>die&nbsp;</b></span>'


def insert_die(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{DIE_TEXT}')")


DAS_TEXT = '<span style="color: #00aa00; font-size: inherit;"><b>das&nbsp;</b></span>'


def insert_das(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{DER_TEXT}')")


NOUN_TEXT = '<span style="color: #3d405b;"><b>NOUN</b></span>'


def insert_noun(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{NOUN_TEXT}')")


VERB_TEXT = '<span style="color: #e07a5f;"><b>VERB</b></span>'


def insert_verb(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{VERB_TEXT}')")


ADJECTIVE_TEXT = '<span style="color: #81b29a;"><b>ADJECTIVE</b></span>'


def insert_adjective(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{ADJECTIVE_TEXT}')")


ADVERB_TEXT = '<span style="color: #d68c45;"><b>ADVERB</b></span>'


def insert_adverb(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{ADVERB_TEXT}')")


PRONOMEN_TEXT = '<span style="color: #98c1d9;"><b>PRONOUN</b></span>'


def insert_pronoun(editor: aqt.editor.Editor) -> None:
    editor.web.eval(f"setFormat('insertHTML', '{PRONOMEN_TEXT}')")


JUNKTION_TEXT = '<span style="color: #eee;"><b>JUNKTION</b></span>'
NUMBER_TEXT = '<span style="color: #eee;"><b>NUMBER</b></span>'


SPEACH_PART_TO_TEXT = {
    SpeachPart.NOUN: NOUN_TEXT,
    SpeachPart.VERB: VERB_TEXT,
    SpeachPart.ADVERB: ADVERB_TEXT,
    SpeachPart.ADJECTIVE: ADJECTIVE_TEXT,
    SpeachPart.PRONOUN: PRONOMEN_TEXT,
    SpeachPart.JUNKTION: JUNKTION_TEXT,
    SpeachPart.NUMBER: NUMBER_TEXT,
}

GENDER_TO_TEXT = {
    Gender.MALE: DER_TEXT,
    Gender.FEMALE: DIE_TEXT,
    Gender.NEUTRAL: DAS_TEXT,
}


def insert_word_description(
    editor: aqt.editor.Editor, only_audio: bool = False
) -> None:
    clipboard = editor.mw.app.clipboard()
    word = clipboard.text().strip()

    if not word:
        showInfo("No word found in clipboard")
        return

    page = find_word_page(word)
    if not page:
        showInfo(f"Page not found for word '{word}'")
        return

    wikitext = get_page_wikitext(page.page_id)
    if not wikitext:
        showInfo(f"No wikitext found for: {word}")
        return

    audio_url = get_audio_url_from_wikitext(wikitext)

    if not only_audio:
        # Set speech part into Info.
        speech_part = get_speach_part_from_wikitext(wikitext)
        if speech_part in SPEACH_PART_TO_TEXT:
            editor.note["Info"] = SPEACH_PART_TO_TEXT[speech_part]

        article_text = ""
        if speech_part == SpeachPart.NOUN:
            # Set article.
            gender = get_gender_from_wikitext(wikitext)
            if gender:
                article_text = f"{GENDER_TO_TEXT[gender]} "

            # Set Example field.
            plural = get_plural_from_wikitext(wikitext)
            genitive = get_genitive_from_wikitext(wikitext)
            editor.note["Example"] = (
                f'<span style="font-weight: bold">{genitive}</span>'
                f'<span style="font-style: italic">&nbsp;genitive</span>, '
                f'<span style="font-weight: bold">{plural}</span>'
                f'<span style="font-style: italic">&nbsp;plural</span>'
            )

        # Add examples.
        examples = get_examples_from_wikitext(wikitext)
        if examples:
            editor.note["Example"] += '<ul class="examples">'
            for example in examples:
                editor.note["Example"] += f"<li>{example}</li>"
            editor.note["Example"] += "</ul>"

        # Add Wiktionary URL.
        editor.note["Example"] += f'<a href="{page.full_url}">{page.full_url}</a>'

        # Add translation.
        config = mw.addonManager.getConfig(__name__)
        if config["DEEPL_AUTH_KEY"]:
            uk_word = get_uk_translation(word, config["DEEPL_AUTH_KEY"])
            editor.note["Back"] = f'<span style="font-weight: bold;">{uk_word}</span>'

        editor.set_note(editor.note)

        # Load IPA
        ipa = get_ipa_from_wikitext(wikitext)
        # TODO: Add article.
        # Insert word
        html = f"<h2>{article_text}{word}</h2>[{ipa}]"
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
    shortcuts.append(
        ("Alt+F1", partial(insert_word_description, editor, only_audio=True))
    )


# https://addon-docs.ankiweb.net/hooks-and-filters.html
gui_hooks.editor_did_init_shortcuts.append(add_shortcuts)
