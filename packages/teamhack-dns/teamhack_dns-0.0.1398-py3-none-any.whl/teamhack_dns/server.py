"""
A DNS server implementation that handles DNS queries and provides responses.
"""

import traceback
#import logging
from socket import AF_INET, SOCK_DGRAM
import socket
from typing import Any, Callable, List, TypeVar

from dnslib import DNSHeader, DNSRecord, QTYPE, NS, A, RR # type: ignore
from teamhack_db.sql import select_hostname_recordtype # type: ignore
#from libia.log import configure_logging
from teamhack_dns.log import configure_logging

T = TypeVar('T')

# Configure logging
logger = configure_logging(__name__)


def handle_exception(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator function to handle exceptions and log error messages.

    Args:
        func: The function to decorate.

    Returns:
        The decorated function.
    """
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error('Error: %s\n%s', e, traceback.format_exc())
            raise
    return wrapper


@handle_exception
def parse_dns_query(data: bytes) -> DNSRecord:
    """
    Parses the DNS query from the received data.

    Args:
        data: The received data containing the DNS query.

    Returns:
        The parsed DNSRecord object.
    """
    return DNSRecord.parse(data)


def create_dns_reply(request: DNSRecord) -> DNSRecord:
    """
    Creates a DNS reply based on the DNS request.

    Args:
        request: The DNS request.

    Returns:
        The DNSRecord object representing the DNS reply.
    """
    return DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)


def send_request_to_upstream(request: DNSRecord, upstream_server: str,
                             upstream_port: int) -> bytes:
    """
    Sends the DNS request to the upstream server.

    Args:
        request: The DNS request.
        upstream_server: The IP address of the upstream DNS server.
        upstream_port: The port of the upstream DNS server.

    Returns:
        The response received from the upstream server.
    """
    return request.send(upstream_server, upstream_port, tcp=False, timeout=10)


@handle_exception
def select_hostname_record(conn: Any, qname: str, qtype: int) -> List:
    """
    Selects the hostname record type from the database.

    Args:
        conn: The database connection object.
        qname: The queried hostname.
        qtype: The record type.

    Returns:
        The database result for the given query.
    """
    res = select_hostname_recordtype(conn, qname, qtype)
    if not isinstance(res, list):
        raise TypeError(f'Unexpected result type: {type(res)}, expected list.')
    return res


@handle_exception
def handle_dns_query(conn: Any, data: bytes, upstream_server: str,
                     upstream_port: int) -> bytes:
    """
    Handles the DNS query and returns a response.

    Args:
        conn: The database connection object.
        data: The received data containing the DNS query.
        upstream_server: The IP address of the upstream DNS server.
        upstream_port: The port of the upstream DNS server.

    Returns:
        The DNS response as a byte string.
    """
    request = parse_dns_query(data)
    reply = create_dns_reply(request)

    qname = str(request.q.qname)
    qtype = request.q.qtype

    logger.debug('Received DNS query - qname: %s, qtype: %s', qname, qtype)

    res = select_hostname_record(conn, qname, qtype)

    if not res:
        return send_request_to_upstream(request, upstream_server, upstream_port)

    res = res[0]

    if not res:
        return send_request_to_upstream(request, upstream_server, upstream_port)

    res = res[3]

    if not res:
        return send_request_to_upstream(request, upstream_server, upstream_port)

    logger.debug(
        'Found result for DNS query - qname: %s, qtype: %s, res: %s', qname, qtype, res)

    if qtype == QTYPE.NS:
        reply.add_answer(RR(rname=qname, rtype=qtype, rdata=NS(res)))
    else:
        reply.add_answer(RR(rname=qname, rtype=qtype, rdata=A(res)))

    return reply.pack()


def start_server(conn: Any, host: str = '', port: int = 53,
                 upstream_server: str = '8.8.8.8', upstream_port: int = 53) -> None:
    """
    Starts the DNS server and listens for incoming requests.

    Args:
        conn: The database connection object.
        host: The host IP address to bind the DNS server. (default: all interfaces)
        port: The port to bind the DNS server. (default: 53)
        upstream_server: The IP address of the upstream DNS server. (default: 8.8.8.8)
        upstream_port: The port of the upstream DNS server. (default: 53)
    """
    server_socket = socket.socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((host, port))

    logger.info('DNS server listening on port %s...', port)

    while True:
        try:
            data, address = server_socket.recvfrom(1024)
            response = handle_dns_query(
                conn, data, upstream_server, upstream_port)
            server_socket.sendto(response, address)
        except KeyboardInterrupt:
            logger.info("DNS server stopped.")
            break
        except TypeError as e:
            logger.error('Error in start_server: %s\n%s',
                         e, traceback.format_exc())
