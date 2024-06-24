import json
import os
import platform
import re
import socket
import time
import requests
from pystyle import *

def start():
    global single_domain;
    global protocol;
    single_domain = input("Enter the Domain Name (website.com): ");
    print("Creating a Target Folder *****");
    path_of_folder = single_domain;
    creating_folder_path(path_of_folder);

def creating_folder_path(path_of_folder):
    if not os.path.exists(path_of_folder):
        os.makedirs(path_of_folder)
        print(f"Folder Created Successfully...{path_of_folder}")
    else:
        print("Target Folder Already Exists...")
        print("Remove Or Replace it before contuning...")
        exit()

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
    print(Colors.yellow+"""-----------------------------------------------------------------------------------------
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