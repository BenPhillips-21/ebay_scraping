import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

laptop_dict = {
    'name': [],
    'price': [],
    'purchase_option': [],
    'shipping': [],
    'link': []
}

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0' }
cookies = {
    "__deba": "7ewrALrIRTtOo_kNegISMFnZ4ENlS617eO0C26x1SghDL0VCowEHKipGMdPhO3jPXR8UW1J2_XMwSXzXGqPFGMLNQcpnJAFZCVLs4cYp7v4uQD8WMJFMPSItyg7WVRrPMFFuQtob4aWT1kV-yq1ERA==",
    "__ssds": "3",
    "__ssuzjsr3": "a9be0cd8e",
    "__uzma": "83a2d7d6-3c99-4031-b8d6-74a789de133d",
    "__uzmb": "1737774217",
    "__uzmc": "852593411969",
    "__uzmd": "1737774282",
    "__uzme": "9674",
    "__uzmf": "7f60004bd413d6-b405-4c4e-88e6-1357c590de83173777421765464971-e8d9a939f8149c4334",
    "ak_bmsc": "5721AD1A8FEE4B30ED7F550F7E688406~000000000000000000000000000000~YAAQF18wF7q3LpOUAQAATzZqmxrEd3E9e7bbkG6FTdZK3GO+8HCOn132oB1WUS6L2pPj+66ACFGcHHnG+HcYGYpowwMXGu2CWsUQbQDgdBseQR3FbEI4loT7Iqg04TjownzioSkc2Q8V8tqSv4X+6qURShscp9IOB/D6ZhLrM9lm91TGt+5Rtx0wBYm7qnSS1UzP4rziUetOqoSRhnF42lCtgRgeRlnGjpIUALqlChyYijBQZwEeNphQecHcQrZwTLFmrAanJv2a2R18wB4Zi9uoQ7i7kuJK9Z4sX2lE+tSXLZLA+fbXszAn6rdKBPwZfdxc+lGtkuvWvCnUh8LMiT0iOvUc1jMveZQMtx16r32j06rL/lp8be3DwfQB3uh9JtyznFogjVYWDBM=",
    "bm_sv": "F20BD564A5903246F23CA9A38EC087E6~YAAQF18wF1fKLpOUAQAALEVrmxrGf1D5dZ1McCeUfXTr32bBiqc7Z0dKhYbAwMjWhtFJmEwuHWHu/NhIWZm/32T6C5ZUdO4VGv9Y4+bQz6PVAoQfpnutovfXKhfEweHOqehmCN1EOJ4kxB8DOPWAXcYI4V0RWTr8+e39qJNUXY/N24Fuxi5kbMRqg5rUWvzP9PbQw9Uk2qMiyv1jW/2VLYGcf/Y8a239f+lVQI9ISoHcH8fPKN/r9F3kHeIv8d73LMQ=~1",
    "dp1": "bpbf/%230002000000000000000006975884e^bl/AU6b56bbce^",
    "ebay": "%5Ejs%3D1%5Esbf%3D%23000000%5E",
    "nonsession": "BAQAAAZRXz2gmAAaAADMABGl1iE4zMDY1AMoAIGtWu845YjZhMzVjMTE5NDBhYjcyZTliOGFlY2JmZmY5OGZhZADLAAJnlFvWMjTPJ+26G5Bd8z3Gwhab+iu3pAEE6A**",
    "ns1": "BAQAAAZRXz2gmAAaAANgAU2l1iE5jNjl8NjAxXjE3Mzc3NzQyMzA1MzheXjFeM3wyfDV8NHw3fDEwfDQyfDQzfDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NQ1S+ukY7G6KC++mkPPqClLkfi0j",
    "s": "CgAD4ACBnlaYIOWI2YTM1YzExOTQwYWI3MmU5YjhhZWNiZmZmOThmYWS9vCW2"
}

page_no = 1
while True:
    print('**************************')
    print(f'Page number: {page_no}')
    print('**************************\n')
    url = f'https://www.ebay.com.au/sch/i.html?_dcat=177&_fsrp=1&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&rt=nc&_ipg=120&_pgn={page_no}'

    res = requests.get(url, headers=headers, cookies=cookies)
    print(res.status_code)

    # if the status code is not 200, keep trying until it is
    if res.status_code != 200:
        continue

    page_html = res.text

    soup = BeautifulSoup(page_html, 'html.parser')
    print(soup.title)

    container = soup.find('div', id='srp-river-results')
    laptops_ul = container.find('ul', class_='srp-results')
    laptops = laptops_ul.find_all('li', class_='s-item s-item__pl-on-bottom', recursive=False)
    for laptop in laptops:
        laptop_item_info = laptop.div.find('div', class_='s-item__info')
        if laptop_item_info.find('div', class_='s-item__title') is not None:
            name_div = laptop_item_info.find('div', class_='s-item__title')
            name = name_div.span.text
        else:
            name = 'No Info'

        laptop_dict['name'].append(name)
        print(name)

        item_details_primary = laptop_item_info.find('div', class_='s-item__details').div
        if item_details_primary.find('span', class_='s-item__price') is not None:
            price = item_details_primary.find('span', class_='s-item__price').text
        else:
            price = 'No Price'

        laptop_dict['price'].append(price)
        print(price)

        purchase_option_div = laptop_item_info.find('div', class_='s-item__details').div.div.find_next_sibling()
        if purchase_option_div.span.text:
            purchase_option = purchase_option_div.span.text
        else:
            purchase_option = 'No Purchase Option'

        laptop_dict['purchase_option'].append(purchase_option)
        print(purchase_option)

        if item_details_primary.find('span', class_='POSITIVE BOLD') is not None:
            postage_info = item_details_primary.find('span', class_='POSITIVE BOLD').text
        else:
            postage_info = 'No Postage'

        laptop_dict['shipping'].append(postage_info)
        print(postage_info)

        if laptop_item_info.find('a', class_='s-item__link')['href'] is not None:
            link = laptop_item_info.find('a', class_='s-item__link')['href']
        else:
            link = 'No Link'

        laptop_dict['link'].append(link)
        print(link)

    next_as_button = soup.find('button', class_='pagination__next')
    if next_as_button:
        break
    else:
        page_no += 1

    print('\n\n')

df = pd.DataFrame(laptop_dict)
df.to_excel('laptops.xlsx')