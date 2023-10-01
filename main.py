## AUTOMATED AMAZON PRICE TRACKER
from bs4 import BeautifulSoup
import requests
import smtplib
import os

amazon_header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
                 "Accept-Language": 'en-US,en;q=0.5',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                 'upgrade-insecure-requests': '1',
                 'sec-fetch-user': '?1',
                 'X-Forwarded-For': '76.168.239.133'
                 }

URL = 'https://www.amazon.com/Instant-Pot-Ultra-Programmable-Sterilizer/dp/B06Y1MP2PY/ref=dp_fod_2?pd_rd_w=QiJIb' \
      '&content-id=amzn1.sym.68174014-ed7a-4e35-badd-6d3576b85c0b&pf_rd_p=68174014-ed7a-4e35-badd-6d3576b85c0b' \
      '&pf_rd_r=RMGW1KW0DBV517D1Z2K9&pd_rd_wg=BYpLi&pd_rd_r=500ee866-a244-4f6e-916c-6e15377dc235&pd_rd_i=B06Y1MP2PY' \
      '&th=1'
response = requests.get(url=URL, headers=amazon_header)
amazon_webpage = response.text
amazon_soup = BeautifulSoup(markup=amazon_webpage, features='lxml')
amazon_price_whole = amazon_soup.find(name='span', class_='a-price-whole').get_text()
amazon_price_fraction = amazon_soup.find(name='span', class_='a-price-fraction').get_text()

amazon_item_title = amazon_soup.find(name='span', id='productTitle', class_='a-size-large product-title-word-break').get_text()

amazon_price = float(f'{amazon_price_whole}{amazon_price_fraction}')

email_pass = os.environ.get("email_pass")
email = os.environ.get("email")

if amazon_price <= 200:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=email_pass)
        connection.sendmail(from_addr=email, to_addrs=email, msg=f'Subject:Amazon Price Alert!\n\n{amazon_item_title} is now ${amazon_price}\n{URL}'.encode("utf-8"))
