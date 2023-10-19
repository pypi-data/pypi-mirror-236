"""
Script entry point.

Parses command line arguments and starts the server using the provided host and port.
"""

import argparse

from teamhack_cis.version import __version__
from teamhack_cis.server import start_server

def parse_args():
    """
    Parse the command line arguments.

    Returns:
        Parsed command line arguments as an instance of `argparse.Namespace`.
    """
    parser = argparse.ArgumentParser(description='Start the server')
    parser.add_argument(
        '-H', '--host', type=str, default='0.0.0.0', help='The host to bind to'
    )
    parser.add_argument(
        '-p', '--port', type=int, default=2223, help='The port to listen on'
    )
    return parser.parse_args()


if __name__ == '__main__':
    print(f"teamhack_cis version: {__version__}")
    args = parse_args()
    start_server(host=args.host, port=args.port)
