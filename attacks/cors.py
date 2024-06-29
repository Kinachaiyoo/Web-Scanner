import os
from urllib.parse import urlparse
import requests


def check_cors(url, create_log,):
    headers = {
        'Origin': 'http://example.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.options(url, headers=headers, timeout=5)

        if response.status_code == 200 and 'Access-Control-Allow-Origin' in response.headers:
            allowed_origin = response.headers['Access-Control-Allow-Origin']
            if 'example.com' in allowed_origin or allowed_origin == '*':
                create_log(f"[-] URL: {url} [Vulnerable]", "red")
                save_vulnerability(url)
            else:
                create_log(f"[-]URL: {url} [Not Vulnerable]", "chartreuse2")
        else:
            create_log(f"[-]URL: {url} [Not Vulnerable]", "chartreuse2")

    except requests.exceptions.RequestException as e:
        create_log(f"[-] An error occurred for URL: {url} - {e}", "red")

def save_vulnerability(url):
    domain = urlparse(url).netloc.lstrip("www.")
    folder_path = os.path.join(domain, "results")
    output_file = os.path.join(folder_path, "cors_vuln.txt")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(output_file, 'a') as f:
        f.write(f"Vulnerable URL: {url}\n")

