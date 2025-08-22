from __future__ import annotations
from babbel.cli import set_langs, show_meta, cultural_shift, status, chat_once

def main() -> None:
    set_langs("en","en")
    show_meta(False)
    cultural_shift(True)
    print(status())
    print(chat_once("hello world"))
    set_langs("en","ja")
    show_meta(True)
    print(status())
    print(chat_once("idiom about rain"))

if __name__ == "__main__":
    main()
