#!/usr/bin/env python3

from machine import DialogueMachine

if __name__ == "__main__":
    dialogue = DialogueMachine(genre_list_path="./resources/small_search.tsv")
    dialogue.loop()
