# -*- coding: UTF-8 -*-
import argparse
from game import *

def parse_cli_args():
    """parse args from the CLI and return a dict"""
    parser = argparse.ArgumentParser(description='Text detector by OpenCV and PyTesser')
    parser.add_argument('-t', '--training', action="store_true")
    parser.add_argument('-n', '--normal', action="store_true")
    return vars(parser.parse_args())

def start_app():
    args = parse_cli_args()
    if args["training"] == True:
        win = Window("training")
        game.mainloop()
    else:
        game.mainloop()
start_app()
