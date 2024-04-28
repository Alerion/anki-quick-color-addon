from typing import Optional
from enum import Enum
import re
import requests
from aqt.utils import showInfo


class SpeachPart(str, Enum):
    NOUN = "NOUN"
    VERB = "VERB"
    ADJECTIVE = "ADJECTIVE"
    ADVERB = "ADVERB"
    PRONOUN = "PRONOUN"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTRAL = "NEUTRAL"

# https://www.mediawiki.org/wiki/API:Query
SEARCH_URL = "https://de.wiktionary.org/w/api.php"


def find_word_page_id(word: str) -> Optional[int]:
    params = {
        "action": "query",
        "format": "json",
        "titles": word,
    }
    response = requests.get(SEARCH_URL, params).json()
    pages = list(response["query"]["pages"].keys())
    if not pages:
        return None
    return int(pages[0])


# https://www.mediawiki.org/wiki/API:Parsing_wikitext
PAGE_URL = "https://de.wiktionary.org/w/api.php"


def get_page_wikitext(page_id: int) -> str:
    params = {
        "action": "parse",
        "format": "json",
        "prop": "wikitext",
        "pageid": page_id
    }
    response = requests.get(PAGE_URL, params).json()
    wikitext = response["parse"]["wikitext"]["*"]
    return wikitext


# https://www.mediawiki.org/wiki/API:Parsing_wikitext
FILES_URL = "https://de.wiktionary.org/w/api.php"


def get_file_url(file_name: str) -> Optional[str]:
    params = {
        "action": "query",
        "format": "json",
        "prop": "imageinfo",
        "iiprop": "url",
        "titles": f"File:{file_name}",
    }
    response = requests.get(FILES_URL, params).json()
    pages = list(response["query"]['pages'].values())
    imageinfo = pages[0]["imageinfo"][0]
    return imageinfo["url"]


def get_word_wikitext(word: str) -> Optional[str]:
    page_id = find_word_page_id(word)
    if not page_id:
        print(f"Page not found for word '{word}'")
        return

    wikitext = get_page_wikitext(page_id)
    return wikitext


AUDIO_RE = re.compile(r"\{\{Audio\|(?P<file>.*?)(|spr=(?P<spr>at))?\}\}")


def get_best_audio_match(matches) -> Optional[str]:
    """
    Return latest one withou specified language. It has the best audio quality.
    """
    for match in reversed(matches):
        if match.group("spr") is not None:
            continue
        file_name = match.group("file")
        if file_name.startswith("De-"):
            return file_name


def get_audio_url_from_wikitext(wikitext: str) -> Optional[str]:
    matches = list(AUDIO_RE.finditer(wikitext))

    if not matches:
        return
    audio_file_name = get_best_audio_match(matches)

    audio_file_url = get_file_url(audio_file_name)
    if not audio_file_url:
        showInfo(f"Audio file URL was not found for file: {audio_file_name}")
        return

    return audio_file_url


IPA_RE = re.compile(r"\{\{Lautschrift\|(.*?)\}\}")


def get_ipa_from_wikitext(wikitext: str) -> Optional[str]:
    matches = IPA_RE.findall(wikitext)

    if not matches:
        return
    return matches[0]


SPEECH_PART_RE = re.compile(r"\{\{Wortart\|(?P<part>\w+)\|Deutsch\}\}(, +\{\{(?P<gender>f|m|n)\}\})?")


def get_speach_part_from_wikitext(wikitext: str) -> SpeachPart:
    matches = list(SPEECH_PART_RE.finditer(wikitext))
    speech_part_match = matches[0].group("part")

    if speech_part_match == "Substantiv":
        return SpeachPart.NOUN
    if speech_part_match == "Verb":
        return SpeachPart.VERB
    if speech_part_match == "Adjektiv":
        return SpeachPart.ADJECTIVE
    if speech_part_match == "Lokaladverb":
        return SpeachPart.ADVERB
    if speech_part_match == "Personalpronomen":
        return SpeachPart.PRONOUN
    showInfo(f"Speach part is not detected from: {speech_part_match}")


def get_gender_from_wikitext(wikitext: str) -> Optional[Gender]:
    matches = list(SPEECH_PART_RE.finditer(wikitext))
    speech_part_match = matches[0].group("gender")

    if speech_part_match == "m":
        return Gender.MALE
    if speech_part_match == "f":
        return Gender.FEMALE
    if speech_part_match == "n":
        return Gender.NEUTRAL