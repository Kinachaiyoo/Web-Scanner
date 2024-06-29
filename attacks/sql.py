import requests
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

def check_sql_injection(url, user_agent, create_log):
    try:
        headers = {'User-Agent': user_agent}
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        sql_payloads = ["' OR '1'='1", "' OR '1'='1' --", "' OR 1=1 --", '" OR "1"="1', '" OR "1"="1" --']

        if not query_params:
            create_log("\n[*] No query parameters found in the URL. SQL Injection check skipped.","green4")
            return

        for param in query_params:
            for payload in sql_payloads:
                query_params[param] = payload
                new_query = urlencode(query_params, doseq=True)
                new_url = urlunparse(parsed_url._replace(query=new_query))
                
                create_log(f"\n[*] Testing URL: {new_url}") 
                response = requests.get(new_url, headers=headers)
                
                if "syntax error" in response.text.lower() or "mysql" in response.text.lower():
                    create_log(f"\n[!] Potential SQL Injection vulnerability detected at {new_url}","red")
                else:
                    create_log(f"\n[-] SQL Injection vulnerability not detected at {new_url}","green4")
    except requests.exceptions.RequestException as e:
        create_log(f"\n[!]An error occurred while checking SQL injection: {e}","red")

if __name__ == "__main__":
    def create_log(message):
        print(message)

    starting_url = "http://example.com"  
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    check_sql_injection(starting_url, user_agent, create_log)
