import pandas as pd
from bs4 import BeautifulSoup
import requests

products = []
prices = []
year = []
header = {
    "Accept": "html,application",
    "User-Agent": "chrome",
    "Accept-Language": "en-US",
    "Connection": "keep-alive",
    "Accept-Encoding": "deflate",
}
params = {
    "Order": 3,
    "priceOnly": 1,
    "imgOnly": 1,
    "page": 1,
}
request = requests.get("https://www.yad2.co.il/vehicles/cars?", params=params, headers=header)
print(request.url)
num = 0

for n in range(1, 11):
    params.update({"page": n})
    request = requests.get("https://www.yad2.co.il/vehicles/cars?", params=params, headers=header)
    soup = BeautifulSoup(request.text, features="html.parser")

    for num, a in enumerate(soup.findAll(attrs={'class': "feeditem table"})):
        name = a.find('span', attrs={'class': 'title'})
        try:
            price = a.find('div', attrs={'id': f'feed_item_{num}_price'}).text.strip()
        except AttributeError:
            price = a.find('span', attrs={'class': f'price'}).text.strip()
        y = a.find('span', attrs={'id': f'data_year_{num}'})
        try:
            pr = int(price.removesuffix(" ג‚×").removesuffix(" ₪").replace(",", "").removesuffix(" ₪ לחודש"))
            if pr > 6000:
                prices.append(price)
                products.append(name.text.strip())
                year.append(y.text.strip())
            elif pr > 20000:
                break
        except ValueError:
            break

print(prices)
print(year)
print(products)
dataframe = pd.DataFrame({"Product name": products, "price": prices, "year": year})
print(dataframe)
dataframe.to_csv("../Input/car_data.csv")