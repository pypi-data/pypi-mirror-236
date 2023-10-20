import argparse

from ._version import __version__


def main():
    parser = argparse.ArgumentParser(prog="apix")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--serializers", action="store_true")
    parser.parse_args()
