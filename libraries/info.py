import requests
import argparse
def get(websiteToScan):
    global user_agent
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }
    return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)

def scann(websiteToScan, output_file, create_log):
    if websiteToScan.startswith('http://'):
        proto = 'http://'
        websiteToScan = websiteToScan[7:]
    elif websiteToScan.startswith('https://'):
        proto = 'https://'
        websiteToScan = websiteToScan[8:]
    else:
        proto = 'http://'
    if websiteToScan.endswith('/'):
        websiteToScan = websiteToScan.strip('/')
    websiteToScan = proto + websiteToScan
    create_log("\n[*] Checking To See If Site Is Online...\n", "blue")

    try:
        onlineCheck = get(websiteToScan)
    except requests.exceptions.ConnectionError as ex:
        create_log("\n[*] {websiteToScan} appeas to be Offline...", "red")
    else:
        if onlineCheck.status_code == 200 or onlineCheck.status_code == 301 or onlineCheck.status_code == 302:
            create_log(f"\n[*] {websiteToScan} appears to be Online...","green")
            create_log("\n[*] Checking To See If Site Is Redirecting","cyan")
            redirectCheck = requests.get(websiteToScan, headers=user_agent)
            if len(redirectCheck.history) > 0:
                if '301' in str(redirectCheck.history[0]) or '302' in str(redirectCheck.history[0]):
                    create_log("[!] Site is redirecting to " + redirectCheck.url,"red")
            elif 'meta http-equiv="REFRESH"' in redirectCheck.text:
                create_log("[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!","red")
            else:
                create_log("[*] Site does not appear to be redirecting...","green")
        else:
            create_log("[!] " + websiteToScan + " appears to be online but returned a " + str(
                onlineCheck.status_code) + " error.","red")
            exit()
        create_log('\n[*] Attempting To Get HTTP HEADERS..........','blue')
        for header in onlineCheck.headers:
            try:
                create_log(" | " + header + " : " + onlineCheck.headers[header])
            except Exception as ex:
                create_log("[!] Error: " + ex.message,"red")

        create_log('[*] Checking Cpanel........',"yellow")
        cpanel_url = websiteToScan + '/cpanel'
        try:
            response = requests.head(cpanel_url)
            if response.status_code == 200:
                create_log(f"[*] cPanel Found: {cpanel_url}\n","green")

            else:
                create_log("[!] cPanel not detected on the website.\n","red")
        except requests.exceptions.RequestException as e:
            create_log(Colors.red+"[!] An error occurred:", e)
        create_log("[+] Running the WordPress scans...","blue")

        wpLoginCheck = requests.get(websiteToScan + '/wp-login.php', headers=user_agent)
        if wpLoginCheck.status_code == 200 and "user_login" in wpLoginCheck.text and "404" not in wpLoginCheck.text:
            create_log("[!] Detected: WordPress WP-Login page: " + websiteToScan + '/wp-login.php',"grean")
            detection_found = True
        else:
            detection_found = False

        wpAdminCheck = requests.get(websiteToScan + '/wp-admin', headers=user_agent)
        if wpAdminCheck.status_code == 200 and "user_login" in wpAdminCheck.text and "404" not in wpAdminCheck.text:
            create_log("[!] Detected: WordPress WP-Admin page: " + websiteToScan + '/wp-admin',"grean")
            detection_found = True

        wpAdminUpgradeCheck = get(websiteToScan + '/wp-admin/upgrade.php')
        if wpAdminUpgradeCheck.status_code == 200 and "404" not in wpAdminUpgradeCheck.text:
            create_log(
                "[!] Detected: WordPress WP-Admin/upgrade.php page: " + websiteToScan + '/wp-admin/upgrade.php',"grean")
            detection_found = True

        wpAdminReadMeCheck = get(websiteToScan + '/readme.html')
        if wpAdminReadMeCheck.status_code == 200 and "404" not in wpAdminReadMeCheck.text:
            create_log("[!] Detected: WordPress Readme.html: " + websiteToScan + '/readme.html',"grean")
            detection_found = True

        wpLinksCheck = get(websiteToScan)
        if 'wp-' in wpLinksCheck.text:
            create_log("[!] Detected: WordPress wp- style links detected on index","grean")
            detection_found = True

        if not detection_found:
            create_log("[!] No Wordpress Misconfiguration Found!!!","red")


        ####################################################
        # phpMyAdmin Scans
        ####################################################

        create_log("\n[+] Running the phpMyAdmin scans...","blue")

        phpMyAdminCheck = get(websiteToScan)
        if phpMyAdminCheck.status_code == 200 and 'phpmyadmin' in phpMyAdminCheck.text:
            create_log("[!] Detected: phpMyAdmin index page","green")
            detection_found = True

        pmaCheck = get(websiteToScan)
        if pmaCheck.status_code == 200 and ('pmahomme' in pmaCheck.text or 'pma_' in pmaCheck.text):
            create_log("[!] Detected: phpMyAdmin pmahomme and pma_ style links on index page","green")
            detection_found = True

        phpMyAdminConfigCheck = get(websiteToScan + '/config.inc.php')
        if phpMyAdminConfigCheck.status_code == 200 and '404' not in phpMyAdminConfigCheck.text:
            create_log("[!] Detected: phpMyAdmin configuration file: " + websiteToScan + '/config.inc.php',"green")
            detection_found = True

        if not detection_found:
            create_log("[!] No PHPMYADMIN Misconfiguration Detected!!!","red")


