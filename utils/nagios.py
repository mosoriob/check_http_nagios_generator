import socket
import json
from urllib.parse import urlparse


def generate_nagios_configuration(file: str, host: str):
    """read a json file

    Args:
        file (str): path of t
    """

    nagions_file = f'{host}.cfg'
    hostname_from_url = []
    with open(nagions_file, 'w', encoding='utf8') as nagios_f:
        nagios_f.write(add_host_definition(host))
        with open(file, 'r', encoding='utf8') as file_d:
            data = json.load(file_d)
            for entry in data:
                url = data[entry]['url']
                # extract the hostname from the url avoid duplicates in the nagios configuration
                hostname_url = url.split('/')[0]
                if hostname_url not in hostname_from_url:
                    hostname_from_url.append(url)
                    line = add_check_cert(hostname_url, host)
                    nagios_f.write(line)
                line = add_http_service(host, entry, f'''https://{url}''')
                nagios_f.write(line)


def add_host_definition(hostname: str):
    return f"""
define host{{
    use                     linux-server
    host_name               {hostname}
    alias                   {hostname}
    address                 {socket.gethostbyname(hostname)}
}}
"""

def add_http_service(server: str, domain: str, url: str):
    """create nagios service check

    Returns:
        str: the nagios service check
    """
    url = url.replace(' ', '')
    url = url.replace('\n', '')
    description = f'''Checking {url} running on {server}'''"".replace(
        '\n', ' ')
    check_command = f"check_http!{url}!{domain}".replace('\n', ' ')
    return f"""
define service {{
    use                             local-service,graphed-service
    host_name                       {server}
    service_description             {description}
    check_command                   {check_command}
}}
    """


def add_check_cert(hostname, host):
    return f"""
define service {{
    use                             local-service,graphed-service         ; Name of service template to use
    host_name                       {host}                               ; Host name
    service_description             check {hostname} certificate
    check_command                   check_ssl_cert!{hostname}
}}
    """
