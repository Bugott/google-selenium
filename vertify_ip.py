import requests


def validateIp(ip, protocol):
    url = "http://ip.chinaz.com/getip.aspx"
    try:
        proxy_host = protocol + "://" + ip
        html = requests.get(url, proxies=proxy_host, timeout=10)
        if html.status_code == 200:
            return True
        else:
            return False
    except:
        return 'error'


print(validateIp("219.73.56.246:556","http"))