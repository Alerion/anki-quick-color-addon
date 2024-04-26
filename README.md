# Mark Deutch with colors

## Hotkeys

- ``F2`` - color translation and makes text bold.
- ``F3`` - insert "der".
- ``F4`` - insert "die".
- ``F5`` - insert "das".
- ``F6`` - insert "NOUN".
- ``F7`` - insert "VERB".
- ``F8`` - insert "ADJECTIVE".
- ``F9`` - insert "ADVERB".
- ``F10`` - insert "PRONOUN".

## Install

Run anki in console:

    cd "C:\Program Files\Anki"
    export QTWEBENGINE_REMOTE_DEBUGGING=8080
    ./anki-console.bat

Create symlink to addons folder:

    mklink /D C:\Users\user\AppData\Roaming\Anki2\addons21\quickcolor <path to project>\anki-quick-color-addon\addon\

Activate virtualenv:

    source ./venv/Scripts/activate
