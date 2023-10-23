"""Showcase (Finnish: vitriini) some packaged content - guided by conventions - command line interface."""
import argparse
import json
import pathlib
import re
import sys
from typing import List, no_type_check

import vitriini.api as api
from vitriini import (
    APP_NAME,
    APP_VERSION,
    ENCODING,
    LOG_SEPARATOR,
    QUIET,
    TS_FORMAT_PAYLOADS,
    log,
)


@no_type_check
def parser():
    """Implementation of command line API returning parser."""
    impl = argparse.ArgumentParser(
        description='Showcase (Finnish: vitriini) some packaged content - guided by conventions.'
    )
    impl.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Be more verbose, maybe',
    )
    impl.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Support debugging, maybe',
    )
    impl.add_argument(
        '-i',
        '--input',
        dest='archive_path',
        type=str,
        help='Archive path',
    )
    return impl


@no_type_check
def app(argv=None):
    """Drive the transformation."""
    argv = sys.argv[1:] if argv is None else argv
    arg_parser = parser()
    if not argv:
        print(f'{APP_NAME} version {APP_VERSION}')
        arg_parser.print_help()
        return 0

    options = arg_parser.parse_args(argv)
    return api.process(options)


if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))
