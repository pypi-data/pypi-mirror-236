"""Anagram solver

Solves single word anagrams.

The word list file (words_alpha.txt) is from:
https://github.com/dwyl/english-words
It may be replaced by any plain text word list, formatted as
one word per line, and (re-)named as "words.txt".
"""
import json
import sys
from collections import defaultdict
from pathlib import Path
from string import ascii_lowercase

from appdirs import AppDirs
from pkg_resources import resource_filename


def import_word_list(wordlist_path: Path) -> list[str]:
    """Return a list of words from the word list file.

    Parameters
    ----------
    wordlist_path: Path
        File path to plain text list of line separated words.

    Return
    ------
    list[str]
        Each element of the list is a word from the word-list file.
    """
    try:
        with open(wordlist_path, 'rt', encoding='utf-8') as fp:
            unique_words = {word.strip() for word in fp}
            return list(unique_words)
    except FileNotFoundError:
        print(f'"{wordlist_path}" not found.')
        sys.exit()
    except PermissionError as err:
        sys.exit(str(err))


def is_cache_invalid(wordlist_path: Path, cache_path: Path) -> bool:
    """Return True if cache needs updating, else False."""
    if not cache_path.exists():
        return True

    wordlist_mtime = wordlist_path.stat().st_mtime
    cache_mtime = cache_path.stat().st_mtime
    return wordlist_mtime > cache_mtime


def build_dict_cache(wordlist_path: Path, cache_path: Path) -> dict[str, list[str]]:
    """Build dictionary cache and return anagram dictionary."""
    print('Building dictionary.')
    anagram_dict = get_all_anagrams(wordlist_path)
    try:
        with open(cache_path, 'wt', encoding='utf-8') as fp:
            json.dump(anagram_dict, fp)
    except OSError as exc:
        print(f'Error {exc}')
        print(f'Unable to write cache to {cache_path}.')
        print(f'Consider making {cache_path} writeable.')
        print('Memory resident anagram dictionary will be used instead.')
    print()
    return anagram_dict


def get_letters() -> str:
    """Return user input string, or an empty string to quit."""
    while True:
        user_input = input('Enter the letters, or "Q" to quit: ')
        # Remove spaces.
        user_input = user_input.strip().replace(' ', '')
        user_input = user_input.lower()

        if user_input == 'q':
            return ''

        if all(char in ascii_lowercase for char in user_input):
            return user_input

        print('Type letters only.')


def print_anagrams(original_letters: str, anagrams: list[str] | None) -> None:
    """Pretty print found anagrams."""
    # Remove the original word if it is in the list.
    # A word is not an anagram of itself.
    if anagrams:
        try:
            anagrams.remove(original_letters)
        except ValueError:
            pass

    if anagrams:
        print(f'These anagrams were found in "{original_letters}": ')
        for word in anagrams:
            print(f'* {word}')
        print()
    else:
        print(f'No anagrams were found in "{original_letters}"\n')


def get_all_anagrams(filename: Path) -> dict[str, list[str]]:
    """Return a dictionary of anagrams.

    Parameters
    ----------
    filename: Path
        File path to plain text list of line separated words.

    Returns
    -------
    dict[str, list[str]]
        Data is in the form:
        {sorted_word: [anagram1, anagram2, ...], ...}
    """
    word_list = import_word_list(filename)

    # Filter and sort words, then group them by sorted form
    anagrams = defaultdict(list)
    for word in word_list:
        if len(word) > 1:
            sorted_word = ''.join(sorted(word))
            anagrams[sorted_word].append(word.lower())

    # Return dict of groups with more than one word.
    return anagrams


def main_loop(anagram_dict: dict[str, list[str]]) -> None:
    """Print a list of anagrams from user supplied letters.

    Parameters
    ----------
    anagram_dict: dict[str, list[str]]
        A dictionary in which:
            key: str
                The input characters in alphabetic  order
            value: list[str]
                A list of anagram strings comprising the same
                characters as the key.
    """
    print("Anagram Monkey.")
    print("Find single word angrams from your letters.")
    print()
    while True:
        letters: str = get_letters()
        if not letters:
            break

        sorted_letters: str = ''.join(sorted(letters))
        anagrams: list[str] | None = anagram_dict.get(sorted_letters)
        if anagrams:
            print_anagrams(letters, anagrams.copy())
        else:
            print_anagrams(letters, None)


def main() -> None:
    """Main set-up. Calls main_loop()"""
    app_name = "monkey_anagram"
    app_author = "Steve Daulton"
    dirs = AppDirs(app_name, app_author)
    # Determine absolute paths to resource files.
    word_list_file = Path(resource_filename(app_name, 'words.txt'))
    cache_path = Path(dirs.user_cache_dir)
    # Ensure the target directory exists
    cache_path.mkdir(parents=True, exist_ok=True)
    cache_file = cache_path/'anagram_dictionary.json'

    anagram_dictionary: dict[str, list[str]]

    # Auto-update cache if necessary.
    if is_cache_invalid(word_list_file, cache_file):
        anagram_dictionary = build_dict_cache(word_list_file, cache_file)
    else:
        # load cache from disk.
        with open(cache_file, 'rt', encoding='utf-8') as file_pointer:
            print('Loading dictionary from disk.\n')
            anagram_dictionary = json.load(file_pointer)

    # Start main loop.
    main_loop(anagram_dictionary)


if __name__ == '__main__':
    main()
