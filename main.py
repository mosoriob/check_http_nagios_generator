import argparse
import os
from utils.kong import generate_intermediate_file_kong
from utils.nagios import generate_nagios_configuration
from utils.txt import generate_intermediate_file_txt


def handle_args():
    """handle args using argparse

    Returns:
        Namespace: the args
    """
    parser = argparse.ArgumentParser(description='Generate http check file')
    parser.add_argument('--kong-file', help='kong file name', required=False)
    parser.add_argument(
        '--server-file', help='contains a list of url to check', required=False)
    parser.add_argument(
        '--server', help='the server that you are working', required=True)
    parser.add_argument(
        '--vhosts-file', help='json file contains the vhosts to check', required=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = handle_args()
    if args.kong_file:
        intermediate_file = generate_intermediate_file_kong(
            args.kong_file, args.server)
    elif args.server_file:
        intermediate_file = generate_intermediate_file_txt(
            args.server_file, args.server)

    generate_nagios_configuration(intermediate_file, args.server)
    if os.path.exists(intermediate_file):
        os.remove(intermediate_file)
