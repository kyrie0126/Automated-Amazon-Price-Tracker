import os
import requests
from bs4 import BeautifulSoup
import smtplib

# Scrape data and find current price
url = 'https://www.amazon.com/Instant-Zest-Rice-Cooker-Pot/dp/B07TZL8Y3C/ref=sr_1_10?crid=3N8T1Y0XCBNBH&keywords=rice+maker&qid=1671491013&s=home-garden&sprefix=rice+make%2Cgarden%2C265&sr=1-10'
headers = {
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
response = requests.get(url, headers=headers)
content = response.text
soup = BeautifulSoup(content, 'lxml')
output = soup.find(name='span', class_='a-offscreen').text
price = float(output.replace('$', ''))
name = soup.find(name='span', id='productTitle').text

# If price is below threshold, send email
# store EMAIL_USER and EMAIL_PASS as environmental variables

if price < 40:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(user=os.environ['EMAIL_USER'], password=os.environ['EMAIL_PASS'])
        connection.sendmail(
            from_addr=os.environ['EMAIL_USER'],
            to_addrs=os.environ['RECIP_EMAIL'],
            msg=("Subject: Low Price Alert\n\n"
                 f"Item: {name}\n\n"
                 f"It's only ${price}!\n\n"
                 f"{url}"
                 )
        )
