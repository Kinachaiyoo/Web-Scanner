import requests
import concurrent.futures

def check_url(url, create_log):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            create_log(f"\n[-] Sensitive URL found: {url}", "green4")
    except Exception as e:
        create_log(f"\n[!] Error checking URL {url}: {e}\n", "red")

def find_sensitive_urls(sensiURL, create_log):
    sensitive_paths = ['/cpanel', '/admin', '/login', '/wp-admin', '/admin.php', '/wp-login.php',
                       '/administrator', '/moderator', '/manager', '/user', '/admin_login',
                       '/adminpanel', '/superadmin', '/sysadmin', '/signin', '/log_in', '/auth',
                       '/controlpanel', '/login.php', '/admin/index.php', '/user/login',
                       '/secure', '/members', '/webmaster', '/root', '/account', '/admin_area',
                       '/admin_login.php', '/adminpanel.php', '/adm.php', '/admincontrol.php',
                       '/admincp', '/admcp', '/admin_login.asp', '/adminpanel.asp', '/adm.asp',
                       '/admincontrol.asp', '/admincp.asp', '/adm/admloginuser.asp', '/admin2.asp',
                       '/admincontrol/login.asp', '/admin/admin-login.asp',
                       '/config.ini', '/config.php', '/config.php.bak', '/config.inc', '/config.backup',
                       '/config.txt', '/backup', '/backups', '/backup.zip', '/backup.tar.gz', '/backup.tgz',
                       '/.git', '/.git/config', '/.gitignore']

    urls = [f"{sensiURL}{path}" for path in sensitive_paths]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_url, url, create_log): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            future.result()
