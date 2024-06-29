import requests
from urllib.parse import urljoin, urlparse

def check_open_redirect(url, user_agent, create_log):
    redirect_payloads = [
        "http://evil.com",
        "https://malicious.com",
        "//evil.com",
        "//malicious.com",
        "javascript:alert('XSS')",
        "javascript:document.location='http://evil.com'",
        "%68%74%74%70%3a%2f%2f%65%76%69%6c%2e%63%6f%6d",  # Hex encoding for http://evil.com
        "%252F%252Fevil.com",  # Double encoding for //evil.com
        "/%5c%5cevil.com/%2e%2e",
        "/..%2f..%2f..%2f..%2fevil.com",
        "next=http://evil.com",
        "url=http://evil.com",
        "continue=http://evil.com",
        "redirect_uri=http://evil.com"
    ]

    try:
        headers = {'User-Agent': user_agent}
        for payload in redirect_payloads:
            test_url = f"{url}?redirect={payload}"
            response = requests.get(test_url, headers=headers, allow_redirects=False)
            if response.status_code in [301, 302] and response.headers.get('Location') == payload:
                create_log(f"\n[!] Open Redirect vulnerability detected at {test_url}", "red")
            else:
                create_log(f"\n[-] Open Redirect vulnerability not detected at {test_url} with payload {payload}", "green4")
    except requests.exceptions.RequestException as e:
        create_log(f"\n[!] An error occurred while checking Open Redirect: {e}")

if __name__ == "__main__":
    def create_log(message, color=None):
        print(message)

    starting_url = "http://example.com"  
    user_agent = "Mozilla/5.0"

    check_open_redirect(starting_url, user_agent, create_log)
