import requests

def test():
    url = 'http://myip.ipip.net'


    proxyMeta = 'socks5://customer-c7590e:13c780cc@proxy.ipipgo.com:31212'
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }

    try:
        resp = requests.get(url=url, proxies=proxies, timeout=10)
        print(resp.text)
        print(resp.status_code)


    except Exception as e:
        print(e)

test()