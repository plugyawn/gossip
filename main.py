import argparse
import atexit
import base64
import collections
import codecs
import functools
import gzip
import json

from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    Iterator,
    List,
    Match,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast,
)

import html.entities
import html.parser
import http.client
from http.client import HTTPSConnection
import locale
import logging
import os
import platform
import shutil
import signal
import socket
import ssl
import subprocess
from subprocess import Popen, PIPE, DEVNULL
import sys
import textwrap
import unicodedata
import urllib.parse
import urllib.request
import uuid
import webbrowser

from interpreter import interpret

_VERSION_ = "0.0.1a"
_DESCRIPTION_ = "Run beautiful Gossip-Lang code, straight from your terminal."
_AUTHOR_ = "Dhyey Thummar, Progyan Das, Rahul Chembakasseril, Sukruta Prakash Midigeshi"
_LAST_MODIFIED_ = "2023-01"
_GIT_LINK_ = "https://github.com/plugyawn/gossip"

# Color codes for more flavorful output -- contamination is bad, so we want it in red.

color_codes = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "bright_black": "90",
    "bright_red": "91",
    "bright_green": "92",
    "bright_yellow": "93",
    "bright_blue": "94",
    "bright_magenta": "95",
    "bright_cyan": "96",
    "bright_white": "97",
}

bold_color_codes = {f"bright_{k}": f"{v};1" for k, v in color_codes.items()}
color_codes.update(bold_color_codes)

special_codes = {
    "reset": "0",
    "bold": "1",
    "inverse": "7",
    "bright_inverse": "7;1",
}

color_codes.update(special_codes)

# Useful dictionary with color codes for easy access.
COLORMAP = {k: f"\x1b[{v}m" for k, v in color_codes.items()}

# Some commonly used colours for easier access.
BLACK = COLORMAP["black"]
RED = COLORMAP["red"]
GREEN = COLORMAP["green"]
YELLOW = COLORMAP["yellow"]
BLUE = COLORMAP["blue"]
RESET = COLORMAP["reset"]

# Some commonly used styles for easier access.
BOLD = COLORMAP["bold"]
INVERSE = COLORMAP["inverse"]
BRIGHT_INVERSE = COLORMAP["bright_inverse"]


class GossipArgumentParser(argparse.ArgumentParser):
    """
    Class for parsing arguments for predicting contamination.
    """

    @staticmethod
    def print_information() -> None:
        """
        Print information about the program.
        """
        print(f"Version: {RED}{_VERSION_}{RESET}")
        print(f"Description: {RED}{BOLD}{_DESCRIPTION_}{RESET}")
        print(f"Author: {RED}{_AUTHOR_}{RESET}")
        print(f"Last Modified: {GREEN}{_LAST_MODIFIED_}{RESET}")
        # color this text

    @staticmethod
    def print_custom_helper() -> None:
        """
        Print help for the program.
        """
        print("Usage patterns about the tool to be printed here.")

    @staticmethod
    def update_latest() -> None:
        """
        Update the tool.
        Borrowed from Jarun/Googler.
        """
        request = urllib.request.Request(
            f"{_GIT_LINK_}/releases?per_page=1",
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        response = urllib.request.urlopen(request)
        if response.status != 200:
            raise http.client.HTTPException(response.reason)
        import json

        return json.loads(response.read().decode("utf-8"))[0]["tag_name"]

    def parse_arguments(args=None, namespace=None) -> argparse.Namespace:
        """
        Parse predict_contamination arguments.

        Parameters
        ----------

        args: list, optional
            List of arguments to parse. Defaults to None.


        Returns
        -------
        argparse.Namespace
            Namespace object containing parsed arguments.
            Works like a dictionary, but it isn't a subclass, so it doesn't have all the methods.
        """

        argparser = GossipArgumentParser(description=_DESCRIPTION_)

        # Bind the add_arg method to the variable -- the name is too long to type again and again.
        addarg = argparser.add_argument

        addarg(
            "-f",
            "--from-file",
            type=str,
            help="path to input .gos file containing gossip.",
        )
        addarg(
            "-u",
            "--update",
            action="store_true",
            help="update the tool to the latest version, if available.",
        )
        addarg(
            "-i",
            "--interpret",
            action="store_true",
            help="start a prompt where you can write pretty gossip.",
        )
        addarg(
            "-s",
            "--show-feedback",
            action="store_true",
            help="show feedback whenever a command is written.",
        )
        addarg(
            "-v",
            "--visualize",
            action="store_true",
            help="show a visualization of the gossip code, line by line.",
        )

        # Make sure data is properly formatted.

        parsed = argparser.parse_args(args, namespace)

        return parsed

    @staticmethod
    def show_title_card() -> None:
        """
        Show a fancy title.
        """
        print(
            f"""{GREEN}                             
                                        o8o                     oooo                                   
                                                                `888                                   
 .oooooooo  .ooooo.   .oooo.o  .oooo.o oooo  oo.ooooo.           888   .oooo.   ooo. .oo.    .oooooooo 
888' `88b  d88' `88b d88(  "8 d88(  "8 `888   888' `88b          888  `P  )88b  `888P"Y88b  888' `88b  
888   888  888   888 `"Y88b.  `"Y88b.   888   888   888 8888888  888   .oP"888   888   888  888   888  
`88bod8P'  888   888 o.  )88b o.  )88b  888   888   888          888  d8(  888   888   888  `88bod8P'  
`8oooooo.  `Y8bod8P' 8""888P' 8""888P' o888o  888bod8P'         o888o `Y888""8o o888o o888o `8oooooo.  
d"     YD                                     888                                           d"     YD  
"Y88888P'                                    o888o                                          "Y88888P'  
                                            
                                            {RESET}{GREEN}{BOLD}Gossip is a python-compiled language for whimsical code.{RESET}    
                                            {RED}{BOLD}Version: {_VERSION_}{RESET} | {RED}{_DESCRIPTION_}{RESET}
                                            {RED}{BOLD}Authors{RESET}:{RED} {_AUTHOR_}{RESET}

        {RESET}"""
        )

    def main():

        GossipArgumentParser.show_title_card()

        opts = GossipArgumentParser.parse_arguments()

        if opts.update:
            latest = GossipArgumentParser.update_latest()
            if latest != _VERSION_:
                print(f"Updating to {latest}...")
                os.system(f"pip install --upgrade {_GIT_LINK_}")
                print("Done.")
            else:
                print("Already up to date.")
            sys.exit(0)

        if opts.interpret:
            interpret(feedback=opts.show_feedback, visualize=opts.visualize)
            sys.exit(0)


if __name__ == "__main__":
    GossipArgumentParser.main()
