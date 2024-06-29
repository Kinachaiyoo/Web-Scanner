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
    global single_domain
    global protocol
    create_log(f"\n[*] Scanning Started on:  {start_time_str}", "green4")
    single_domain = domain_entry.get()
    create_log("\n[!] Creating a Target Folder ...... Please Wait", "blue")
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

    create_log("\n[-]+++++++++++GATHERING TARGET'S INFORMATION++++++++++++", "blue")
    from libraries.tech import detect_cms, detect_server
    from libraries.waf import detect_waf

    protocol = detect_http_or_https(single_domain)
    url = protocol
    create_log(f'\n[-] Target Domain: {checking}\n', "green4")
    create_log(f'[-] Target IP: {domain_to_ip}\n', "green4")
    create_log(f'[-] PROTOCOL: {url}\n', "green4")
    cms = detect_cms(single_domain)
    create_log(f"[-] CMS: {cms}\n", "green4")
    server = detect_server(single_domain)
    create_log(f"[-] SERVER: {server}\n", "green4")
    detect_waf(url, create_log)
    create_log('\n\n-----------------------------------------------\n')
    create_log('\n[*] Searching For Sensitive Paths & Files.....', "blue")

    from libraries.sensitive import find_sensitive_urls
    find_sensitive_urls(protocol, create_log)
    folder_path1 = os.path.join(single_domain, "results")
    if not os.path.exists(folder_path1):
        os.makedirs(folder_path1)  

    from libraries.info import scann
    output_file=os.path.join(folder_path1, "Target_info.txt")
    outing=os.path.join(folder_path1, "scanned_ports.txt")
    scann(single_domain, output_file, create_log)
    create_log('\n\n-----------------------------------------------\n')
    create_log('\n[+] Scanning Open Ports And Finding Exploits:-', "blue")
    dest = f"https://internetdb.shodan.io/{domain_to_ip}"
    response = requests.get(dest)
    data = response.json()
    ports = data.get('ports', [])
    vulns = data.get('vulns', [])
    cpes = data.get('cpes', [])
    create_log(f'\n[-] Ports: {ports}',"red")
    create_log(f'\n[-] Vulns: {vulns}',"red")
    create_log(f'\n[-] Cpes:  {cpes}',"red")
    write_results_to_file(outing, domain_to_ip, ports, vulns, cpes)
    create_log(f'\n[-] Results Saved To: {outing}\n',"DarkGoldenrod1")

    create_log('\n-----------------------------------------------\n')
    create_log('\n[*] Extracting Javascript Urls....',"blue")
    from libraries.javascript import extract_js_links
    js_file = path_of_folder + '/javascript_urls.txt'
    extract_js_links(url, js_file)
    create_log(f'\n[-] Javascript Urls Saved To: {js_file}\n', "DarkGoldenrod1")
    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Getting URLS From Public Archives...","blue")
    target = single_domain
    wayback_urls = fetch_urls_from_wayback(target)
    unique_urls = set()
    for url in wayback_urls:
        url = url.strip()  
        if url:
            unique_urls.add(url)
    filtered_urls = []
    for url in unique_urls:
        if not re.search(r'\.(woff|ttf|svg|eot|png|jpe?g|css|ico)$', url, re.IGNORECASE):
            url = re.sub(r':(80|443)', '', url)
            filtered_urls.append(url)
    output_file = path_of_folder + '/filtered_urls.txt'  
    with open(output_file, 'w') as file:
        for url in filtered_urls:
            file.write(url + '\n')
    create_log(f"\n[-] Filtered URLs saved to {output_file}\n","DarkGoldenrod1")
    time.sleep(1)

    create_log( '\n-----------------------------------------------\n',)
    create_log("\n[*] Filtering URLS for Open Redirect Vulnerability\n","blue")
    from libraries.redirect import apply_filter
    fil_urls = output_file
    red_out = path_of_folder + '/redirect_urls.txt'
    apply_filter(fil_urls, red_out)
    time.sleep(1)
    create_log(f"[-] Possible Vulnerable Open Redirect Urls Saved To {red_out}\n","DarkGoldenrod1")
    time.sleep(1)

    create_log('\n-----------------------------------------------\n',"yellow")
    create_log("\n[*] Filtering URLS for Cross Site Scripting...","blue")
    from libraries.xss import apply_filter
    input_file = output_file
    xss_file = path_of_folder + '/xss_urls.txt'
    apply_filter(input_file, xss_file)
    time.sleep(1)
    create_log(f'\n[-] Possible Vulnerable XSS Urls Saved To {xss_file}\n',"DarkGoldenrod1")
    time.sleep(1)

    create_log('\n-----------------------------------------------\n',"yellow")
    create_log("\n[*] Filtering URLS for SQL Injection.....\n","blue")
    from libraries.sqli import sql_urls
    input_file = output_file
    sql_file = path_of_folder + '/sql_urls.txt'
    sql_urls(input_file, sql_file)
    time.sleep(1)
    create_log(f"[-] Possible Vulnerable SQLI Urls Saved To {sql_file}\n","DarkGoldenrod1")
    time.sleep(1)

    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Filtering URLS for Local File Inclusion (LFI)...\n","blue")
    from libraries.lfi import apply_filter
    fil_urls = output_file
    red_out = path_of_folder + '/lfi_urls.txt'
    apply_filter(fil_urls, red_out)
    time.sleep(1)
    create_log(f'[-] Possible Vulnerable LFI Urls Saved To {red_out}',"DarkGoldenrod1")

    attacks()

def attacks():
    url = protocol
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    path_of_folder = os.path.join(single_domain, "results")
    # Create the folder if it doesn't exist
    if not os.path.exists(path_of_folder):
        os.makedirs(path_of_folder)
    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Testing For CORS Misconfiguration.........\n","blue")
    from attacks.cors import check_cors
    check_cors(url,create_log)

    create_log('\n\n-----------------------------------------------\n')
    create_log("\n[*] Testing For XSS Detection.........","blue")
    from attacks.xss import check_xss
    check_xss(url,user_agent,create_log)

    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Testing For Open Redirect Detection.........","blue")
    from attacks.open_redirection import check_open_redirect
    check_open_redirect(url,user_agent,create_log)

    create_log('\n\n-----------------------------------------------\n')
    create_log("\n[*] Testing For Security Headers Detection.........","blue")
    from attacks.security_header import check_security_headers
    check_security_headers(url,user_agent,create_log)

    create_log('\n\n-----------------------------------------------\n')
    create_log("\n[*] Testing For Directory Tracersal Detection.........","blue")
    from attacks.directory_trav import check_directory_traversal
    check_directory_traversal(url,user_agent,create_log)

    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Testing for SQL Injections...","blue")
    from attacks.sql import check_sql_injection
    url = protocol
    check_sql_injection(url,user_agent,create_log)

    create_log('\n-----------------------------------------------\n')
    create_log("\n[*] Bruteforcing Directories...","blue")
    from attacks.dirbs import crawl_website
    website_url = protocol
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0.2 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/91.0.2 Safari/537.36',
    ]
    for user_agent in user_agents:
        crawl_website(website_url, user_agent,create_log)
        create_log("")
    elapsed_time = time.time() - start_time
    create_log(f"\n[*] Total Time Taken:  {elapsed_time}\n","red")
    create_log('\n-----------------------------------------------\n')



def creating_folder_path(path_of_folder):
    if not os.path.exists(path_of_folder):
        os.makedirs(path_of_folder)
        create_log(f"\n[*] Folder Created Successfully...{path_of_folder}\n", "green4")
    else:
        create_log("\nTarget Folder Already Exists...\n", "red")
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

def write_results_to_file(filename, domain_to_ip, ports, vulns, cpes):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"[ ✔ ] [IP]: {domain_to_ip}\n")
        file.write(f"[ ✔ ] [PORTS]: {ports}\n")
        file.write(f"[ ✔ ] [VULNS]: {vulns}\n")
        file.write(f"[ ✔ ] [INFO]: {cpes}\n")

def fetch_urls_from_wayback(target):
    url = f"https://web.archive.org/cdx/search/cdx?url={target}/*&output=json&fl=original"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        urls = [entry[0] for entry in data[1:]]
        return urls
    else:
        print(Colors.red+ "[*] Failed To Fetch Urls From Wayback...")
        return []

start_time = time.time()
start_time_str = time.ctime(start_time)

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
log_text.tag_configure("green4", foreground="green4")
log_text.tag_configure("blue", foreground="blue")
log_text.tag_configure("black", foreground="black")
log_text.tag_configure("DarkGoldenrod1", foreground="DarkGoldenrod1")
log_text.tag_configure("cyan", foreground="cyan")
log_text.tag_configure("purple3", foreground="purple3")

# Start GUI
root.mainloop()
