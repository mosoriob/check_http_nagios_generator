from asyncio.log import logger
from .utils import check_ip, get_filename, write_json_file


def generate_intermediate_file_txt(file: str, server: str):
    logger.info("handle txt file")
    data = read_txt_file(file, server)
    file_name = get_filename(server)
    write_json_file(file_name, data)
    return file_name


def read_txt_file(file: str, server: str):
    """read a txt file per line and create a nagios service check

    Args:
        file (str): path of t
    """
    all_hosts = {}
    with open(file, 'r', encoding='utf8') as f:
        for url in f.read().splitlines():
            if check_ip(url, server):
                all_hosts[url] = {'url': url, 'hostname': server}
    return all_hosts
