import json
import logging
import socket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def write_json_file(file: str, data: dict):
    """write a json file

    Args:
        file (str): path of t
        data (dict): data
    """
    logger.info("write json file")
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2)


def get_filename(server: str):
    """create a file name from server

    Args:
        server (str): the server name
    """
    return f"{server.replace('.', '_')}.json"

# check if ip match with the domain


def check_ip(domain: str, server_name: str):
    """check if ip match with the domain

    Args:
        ip (str): the ip address
        domain (str): the domain name
    """
    try:
        if not socket.gethostbyname(server_name) == socket.gethostbyname(domain):
            logger.info(f"Unable to add {domain} is not running on {server_name}")
            return False
    except socket.gaierror as e:
        logger.warning(f"Unable to add {domain} because {e}")
        return False
    return True
