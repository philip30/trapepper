#!/usr/bin/env python3

import argparse
from machine import DialogueMachine
from trapepper import ParserResource

parser = argparse.ArgumentParser("Trapepper")
parser.add_argument("--debug", action="store_true")
args = parser.parse_args()

if __name__ == "__main__":
    dialogue = DialogueMachine(genre_list_path=ParserResource, debug=args.debug)
    dialogue.loop()

