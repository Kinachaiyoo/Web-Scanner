import json
import os
import platform
import re
import socket
import time
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading

def start():
    single_domain = domain_entry.get()
    create_log("Creating a Target Folder *****\n", "blue")
    path_of_folder = single_domain
    creating_folder_path(path_of_folder)

    domain_part = single_domain.split(":")
    if len(domain_part) > 1:
        domain_to_ip = domain_part[0]
        port_number = domain_part[1]
        checking = f'{domain_to_ip}:{port_number}'
    else:
        checking = single_domain.replace('http://', '').replace('https://', '')
        domain_to_ip = socket.gethostbyname(checking)

    from libraries.tech import detect_cms, detect_server
    from libraries.waf import detect_waf

    protocol = detect_http_or_https(single_domain)
    url = protocol
    create_log(f'Target Domain: {checking}\n', "green")
    create_log(f'Target IP: {domain_to_ip}\n', "green")
    create_log(f'PROTOCOL: {url}\n', "green")
    cms = detect_cms(single_domain)
    create_log(f"CMS: {cms}\n", "green")
    server = detect_server(single_domain)
    create_log(f"SERVER: {server}\n", "green")
    detect_waf(url)
    create_log('\n-----------------------------------------------\n', "blue")
    create_log('\n[*] Searching For Sensitive Paths & Files.....\n', "blue")

def creating_folder_path(path_of_folder):
    if not os.path.exists(path_of_folder):
        os.makedirs(path_of_folder)
        create_log(f"Folder Created Successfully...{path_of_folder}\n", "green")
    else:
        create_log("Target Folder Already Exists...\n", "red")
        create_log("Remove Or Replace it before continuing...\n", "red")
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
    value = True
    while value:
        os.system('cls' if os.name == 'nt' else 'clear')
        start()

def options():
    create_log("""-----------------------------------------------------------------------------------------
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
""", "blue")

def create_log(message, color="black"):
    # Use the `after` method to safely update the GUI from the background thread
    log_text.after(0, log_text.insert, tk.END, message, color)
    log_text.after(0, log_text.see, tk.END)

def run_scan():
    # Start the scanning process in a new thread
    threading.Thread(target=start).start()

# GUI Setup
root = tk.Tk()
root.title("Web Domain Scanner")
root.geometry("800x600")

# Domain Entry
tk.Label(root, text="Enter the Domain Name (website.com):").pack(pady=10)
domain_entry = tk.Entry(root, width=50)
domain_entry.pack(pady=10)

# Buttons
tk.Button(root, text="START SCAN", command=run_scan).pack(pady=10)
tk.Button(root, text="SHOW AVAILABLE SCANNING MODULE", command=options).pack(pady=10)

# Log Output
log_text = scrolledtext.ScrolledText(root, width=100, height=30)
log_text.pack(pady=10)

# Adding color tags
log_text.tag_configure("red", foreground="red")
log_text.tag_configure("green", foreground="green")
log_text.tag_configure("blue", foreground="blue")
log_text.tag_configure("black", foreground="black")

# Start GUI
root.mainloop()
