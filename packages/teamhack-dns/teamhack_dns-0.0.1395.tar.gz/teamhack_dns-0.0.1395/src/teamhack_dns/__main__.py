"""
A DNS server implementation that starts the DNS server and handles command line arguments.
"""

import argparse
import psycopg2 # type: ignore
from teamhack_db.conf import config # type: ignore
from teamhack_db.sql import create_table # type: ignore
from teamhack_dns.version import __version__
from teamhack_dns.server import start_server


def parse_args():
    """
    Parse the command line arguments.

    @return: Parsed command line arguments
    @rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description='Start the server')
    parser.add_argument(
        '--host', type=str, default='', help='The host to bind to'
    )
    parser.add_argument(
        '--port', type=int, default=53, help='The port to listen on'
    )
    parser.add_argument(
        '--upstream-host', type=str, default='8.8.8.8', help='The upstream DNS server host'
    )
    parser.add_argument(
        '--upstream-port', type=int, default=53, help='The upstream DNS server port'
    )
    return parser.parse_args()


if __name__ == '__main__':
    print(f"teamhack_dns version: {__version__}")
    args = parse_args()
    params = config()
    conn = psycopg2.connect(**params)

    try:
        create_table(conn)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        raise e

    start_server(
        conn, host=args.host, port=args.port,
        upstream_server=args.upstream_host, upstream_port=args.upstream_port
    )
