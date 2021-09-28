from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl

pages_to_scrape = 10

pages = []
stars = []
links = []
titles = []


for i in range(1, pages_to_scrape+1):
    url = f"https://books.toscrape.com/catalogue/page-{i}.html"

    # append all the pages
    pages.append(url)

for item in pages:
    #make a request and a  soup
    response = requests.get(item) # item will be a page
    soup = BeautifulSoup(response.text, "html.parser")

    # to get all the elements by using soup.select() , return a list
    all_tag_titles = soup.select("h3 a")
    #loop through each tag
    for tag in all_tag_titles:
        tags = tag.get("href")  # get the attributes
        links.append("https://books.toscrape.com/catalogue/" + tags)


        # append all the titles
        titles_ = tag.get("title")
        titles.append(titles_)

    #print(links)

    # get each product price use list comprehension
    product_price = [price.text for price in soup.find_all("p", class_="price_color")]
    #print(product_price)


    for s in soup.find_all("p",class_="star-rating"):
        for k, v in s.attrs.items(): # not sure about this function, a dict
            star = v[1]
            stars.append(star)

    #print(stars)


    # get each product instock availability use list comprehension
    product_availability = [instock.text.strip() for instock in soup.find_all("p",class_="instock availability")]
    #print(product_availability)


    # create a data_dict to store all the data
    data_dict = {'Title': titles, 'Prices': product_price,'Stars':stars, 'Product_availability': product_availability, "URLs": links}
    #print(data_dict)

    df = pd.DataFrame(data_dict)
    #print(df)
    df.to_excel("books_information.xlsx")
    break # the loop can loop once if use break