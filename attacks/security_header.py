import requests

def check_security_headers(url, user_agent, create_log):
    required_headers = {
        "Content-Security-Policy": "Content Security Policy",
        "Strict-Transport-Security": "HTTP Strict Transport Security",
        "X-Content-Type-Options": "MIME Type Sniffing Protection",
        "X-Frame-Options": "Clickjacking Protection",
        "X-XSS-Protection": "Cross-Site Scripting Protection"
    }
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        for header, description in required_headers.items():
            if header not in response.headers:
                create_log(f"\n[!] Missing Security Header: {header} ({description})","red")
            else:
                create_log(f"\n[*] Security Header Found: {header}","green4")
    except requests.exceptions.RequestException as e:
        create_log(f"\n[!]An error occurred while checking security headers: {e}")

if __name__ == "__main__":
    def create_log(message):
        print(message)

    starting_url = "http://example.com"  
    user_agent = "Mozilla/5.0"

    check_security_headers(starting_url, user_agent, create_log)
