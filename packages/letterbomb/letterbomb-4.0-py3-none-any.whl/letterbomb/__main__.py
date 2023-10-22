#!/usr/bin/env python3
# coding: utf-8
# SPDX-License-Identifier: MIT
"""
CLI interface for ✉️💣 **LetterBomb**.

----

positional arguments:
  * mac                   string of Wii's MAC address
  * {U,E,K,J}             uppercase letter of Wii's region

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTFILE, --outfile OUTFILE
                        filename of ZIP archive. If omitted,
                        bytes of ZIP archive will be written to stdout
  -b, --bundle          pack the HackMii installer into archive
  -l LOGFILE, --logfile LOGFILE
                        filepath to put log output
  -g {debug,info,warn,error,critical}, --loglevel {debug,info,warn,error,critical}
                        minimum logging level

"""
import argparse
import io
import sys
import logging
import pathlib
import typing

import letterbomb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"LetterBomb v{'.'.join(str(x) for x in letterbomb.__version__)}",
    )
    parser.add_argument("mac", help="string of Wii's MAC address")
    parser.add_argument(
        "region",
        choices=letterbomb.REGIONS,
        help="uppercase letter of Wii's region",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help="filename of ZIP archive. If omitted, bytes of ZIP archive will be written to stdout",
        default="",
    )
    parser.add_argument(
        "-b",
        "--bundle",
        action="store_true",
        help="pack the HackMii installer into archive",
    )
    parser.add_argument("-l", "--logfile", help="filepath to put log output")
    parser.add_argument(
        "-g",
        "--loglevel",
        help="minimum logging level",
        choices=letterbomb.LOGGING_DICT.keys(),
        default="info",
    )

    vargs = vars(parser.parse_args())
    if letterbomb.LOGGING_DICT[vargs["loglevel"]] == logging.DEBUG:
        print(vargs)
    if vargs["logfile"]:
        LOGGING_FILE = pathlib.Path(vargs["logfile"]).expanduser()
    result = letterbomb.write(vargs["mac"], vargs["region"], vargs["bundle"], vargs["outfile"])

    if not vargs["outfile"]:
        # No outfile, return raw
        result = typing.cast(io.BytesIO, result)
        sys.stdout.buffer.write(result.getvalue())
        sys.stdout.buffer.flush()
    else:
        # Outfile, show resulting file name as string, so it can be passed
        print(str(result))
