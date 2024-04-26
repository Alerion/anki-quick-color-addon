from typing import Optional
import re
import requests


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
PAGE_URL = "https://de.wiktionary.org/w/api.php?redirects&action=parse&format=json&prop=wikitext&pageid={}"


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


AUDIO_RE = re.compile(r"\{\{Audio\|(.*?)\}\}")


def get_audio_url_from_wikitext(wikitext: str) -> Optional[str]:
    matches = AUDIO_RE.findall(wikitext)

    if not matches:
        return
    audio_file_name = matches[0]

    audio_file_url = get_file_url(audio_file_name)
    if not audio_file_url:
        print(f"Audio file URL was not found for file: {audio_file_name}")
        return
    return audio_file_url


IPA_RE = re.compile(r"\{\{Lautschrift\|(.*?)\}\}")


def get_ipa_from_wikitext(wikitext: str) -> Optional[str]:
    matches = IPA_RE.findall(wikitext)

    if not matches:
        return
    return matches[0]
