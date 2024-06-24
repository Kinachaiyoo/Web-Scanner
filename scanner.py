import json
import os
import platform
import re
import socket
import time
import requests

def start():
    global single_domain;
    global protocol;
    single_domain = input("Enter the Domain Name (website.com): ");
    print("Creating a Target Folder *****");
    path_of_folder = single_domain;
    creating_folder_path(path_of_folder);

    domain_part = single_domain.split(":")
    if len(domain_part) > 1:
        domain_to_ip = domain_part[0]
        port_number = domain_part[1]
        checking = f'{domain_to_ip}:{port_number}'
    else:
        checking = single_domain.replace('http://','').replace('https://','')
        domain_to_ip = socket.gethostbyname(checking)

    from libraries.tech import detect_cms, detect_server
    from libraries.waf import detect_waf

    protocol = detect_http_or_https(single_domain)
    url = protocol
    print(f'Target Domain: {checking}')
    print(f'Target IP: {domain_to_ip}')
    print(f'PROTOCOL: {url}')
    cms = detect_cms(single_domain)
    print(f"CMS: {cms}")
    server = detect_server(single_domain)
    print(f"SERVER: {server}")
    detect_waf(url)
    print('\n-----------------------------------------------')
    print('\n[*] Searching For Sensitive Paths & Files.....\n')

def creating_folder_path(path_of_folder):
    if not os.path.exists(path_of_folder):
        os.makedirs(path_of_folder)
        print(f"Folder Created Successfully...{path_of_folder}")
    else:
        print("Target Folder Already Exists...")
        print("Remove Or Replace it before contuning...")
        exit()

def detect_http_or_https(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.url
        return 'Unknown'
    except requests.exceptions.RequestException:
        return 'Invalid'

def scanner():
    value = True;
    while value:
        print(""" 
        1. START SCAN
        2. SHOW AVAILABLE SCANNING MODULE
        3. Exit
        """)
        value = input("Choose an option to continue: ")
        if value == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            start()
        elif value == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            options()
        elif value == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Colors.red+"\n Thanks For Using! See You Soon :)")
            value = False
        else:
            print("!!! Not a valid option. Try again. !!!")

def options():
    print("""-----------------------------------------------------------------------------------------
1.  WEB DOMAIN INFORMATION(IP, PROTOCOL, CMS DETECTION, SERVER DETECTION, WAF DETECTION) -
2.  SENSITIVE PATH FINDER                                                                -
3.  MISCONFIGURATIONS/SENSITIVE SCANS(WORDPRESS, JOOMLA, DRUPAL, PHPMYADMIN)             -
4.  SCANNING PORTS & LOOKING FOR EXPLOITS                                                -
5.  EXTRACTING JAVASCRIPT URLS                                                           -
6.  GETTING URLS FROM PUBLIC ARCHIVES                                                    -
7.  FILTERNING URLS FOR OPEN REDIRECTION                                                 -
8.  FILTERNING URLS FOR CROSS SITE SCRIPTING                                             -
9.  FILTERNING URLS FOR LOCAL FILE INCLUSION                                             -
10. FILTERNING URLS FOR SQLI INJECTION                                                   -
11. TESTING CORS MISCONFIGURATION                                                        -
12. TESTING CLICKJACKING VULNERABILITY                                                   -
13. TESTING SQLI INJECTION VULNERABILITY                                                 -
14. TESTING OPEN REDIRECT VULNERABILITY                                                  -
15. TESTING LOCAL FILE INCLUSION VULNERABILITY                                           -
16. TESTING CROSS SITE SCRIPTING VULNERABILITY                                           -
17. DIRECTORY BRUTEFORCING                                                               -
------------------------------------------------------------------------------------------
""")


def check():
    try:
        if platform.system().startswith("Linux"):
            os.system("clear");
            scanner()
        elif platform.system().startwith("Windows"):
            os.system("cls");
            scanner()
    except KeyboardInterrupt:
        print("!!! Something went wrong. Please check and try again. !!!")

check()