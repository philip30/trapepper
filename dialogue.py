#!/usr/bin/env python3

import argparse
from machine import DialogueMachine

parser = argparse.ArgumentParser("Trapepper")
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

if __name__ == "__main__":
    dialogue = DialogueMachine(genre_list_path="./resources/small_search.tsv", debug=args.debug)
    dialogue.loop()

