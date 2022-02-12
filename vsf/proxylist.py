from bs4 import BeautifulSoup as bs
import requests

def get_free_proxy():
    url = 'https://free-proxy-list.net/'
    webpage = requests.get(url)
    print(webpage.status_code)

    soup_obj = bs(webpage.content, 'html.parser')

    proxy_list = []


    table = soup_obj.find('table', class_='table table-striped table-bordered')
    tr_list = table.find_all('tr')[1:]

    for row in tr_list:
        tds = row.find_all('td')
        try:
            is_https = tds[6].text.strip()
            if is_https == 'yes':
                ip = tds[0].text.strip()
                port = tds[1].text.strip()
                host = f"{ip}:{port}"
                proxy_list.append(host)
            else:
                continue
        except IndexError:
            continue

    return proxy_list




