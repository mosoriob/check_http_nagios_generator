import json
from .utils import check_ip, logger, get_filename, write_json_file


def generate_intermediate_file_kong(file: str, server: str):
    """read a kong configuration file exported using

    Args:
        file (str): path file
    """
    logger.info("handle kong file")
    hosts = read_kong_json_file(file, server)
    vhosts_file_path = get_filename(server)
    write_json_file(vhosts_file_path, hosts)
    return vhosts_file_path


def read_kong_json_file(file: str, server: str):
    '''
    Read kong file and return a dict
    '''
    all_hosts = {}
    with open(file, 'r', encoding='utf8') as file_pointer:
        data = json.load(file_pointer)
        services = data['services']
        for service in services:
            if "routes" in service:
                for route in service['routes']:
                    if "hosts" in route:
                        for host in route['hosts']:
                            if check_ip(host, server):
                                all_hosts[host] = {'url': host, 'hostname': host}
    return all_hosts
