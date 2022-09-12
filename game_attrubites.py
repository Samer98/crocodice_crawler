from bs4 import BeautifulSoup
import requests
import json
import os
from _datetime import datetime
import time



parent_dir = "D:/Storage/Python/Projects/crocodice_crawler/game_images"
links =[]
with open('gamelink.txt') as f:
    lines = f.readlines()
    for line in lines:
        links.append(line[:-1])
    f.close()
games=[]
issue_links=[]
# links=["https://crocodice.net/products/forbidden-island"]
# i =0
now = datetime.now()
print ("The time is now: = %s:%s:%s" % (now.hour, now.minute, now.second))
for url in links:
    # url = 'https://crocodice.net/products/forbidden-island'
    # print(url)
    path = os.path.join(parent_dir, url[31:])
    image_links=[]
    result = requests.get(url)
    game = BeautifulSoup(result.text, "html.parser")
    # print(game.prettify())
    title= game.find("title")
    # print(title.string.strip())
    price = game.find(class_="product-single__price product-single__price--compare")
    discount = game.find(id="ProductPrice-product-template")
    # print(price)
    desc = game.find(class_="rte product-single__description")
    # print(desc.text.strip())
    language="English"
    if "[AR/EN]" in title.string.strip():
        language="English/Arabic"
    elif "[AR]" in title.string.strip():
        language="Arabic"
    # print(title.string.strip())
    if "[AR/EN]" in title.string.strip() :
        new_title = title.string.strip().replace("[AR/EN]","")
        SEO_EN = new_title.strip()[:-13].replace(" ","-").lower()
        SEO_AR = new_title.strip()[:-13].replace(" ","-").upper()
    elif "[AR]" in title.string.strip() :
        new_title = title.string.strip().replace("[AR]","")
        SEO_EN = new_title.strip()[:-13].replace(" ","-").lower()
        SEO_AR = new_title.strip()[:-13].replace(" ","-").upper()
    elif "[ar/en/fr]" in title.string.strip() :
        new_title = title.string.strip().replace("[ar/en/fr]","")
        SEO_EN = new_title.strip()[:-13].replace(" ","-").lower()
        SEO_AR = new_title.strip()[:-13].replace(" ","-").upper()
    else:
        SEO_EN = title.string.strip()[:-12].replace(" ","-").lower()
        SEO_AR = title.string.strip()[:-12].replace(" ","-").upper()
    # print(SEO_EN)
    # print(SEO_AR)
    # print(language)
    buy_button=  game.find(id="AddToCartText-product-template")
    buy_button = buy_button.text.strip()


    images = game.find_all(class_="product-single__thumbnail product-single__thumbnail-product-template")
    main_image = game.find_all("noscript")
    img = main_image[0].find("img")
    main_image_link=img['src']
    # print(main_image_link)
    os.mkdir(path)
    for image in range(len(images)):
        image_links.append(images[image]['data-zoom'])
        with open(f'D:/Storage/Python/Projects/crocodice_crawler/game_images/{url[31:]}/{url[31:]}_{image}.jpg', 'wb') as handler:
            handler.write(requests.get("https:"+images[image]['data-zoom']).content)
    with open(f'D:/Storage/Python/Projects/crocodice_crawler/game_images/{url[31:]}/{url[31:]}_main.jpg', 'wb') as handler:
        handler.write(requests.get("https:"+main_image_link).content)

    try:
        video = game.find('iframe')
        video_link= video['src']
        video_link= video_link.replace('embed/',"watch?v=")
    except:
        video_link ="None"
        pass
    try:
        games.append({"game":title.string.strip()[:-12],
            "url":url,
            "description":desc.text.strip(),
            "youtube_link":video_link,
            "original_price":int(price.string.strip()[3:-3].replace(",", '')),
            "discount_price":int(discount.string.strip()[3:-3].replace(",", '')),
            "images":image_links,
            "is_in_stock": buy_button == "Add to Cart",
            "language": language,
            "SEO_EN": SEO_EN,
            "SEO_AR": SEO_AR,
        })
    except:
            price = game.find(id="ProductPrice-product-template")
            games.append({"game":title.string.strip()[:-12],
            "url":url,
            "description":desc.text.strip(),
            "youtube_link":video_link,
            "original_price":int(price.string.strip()[3:-3].replace(",", '')),
            "discount_price":"None",
            "images":image_links,
            "is_in_stock": buy_button == "Add to Cart",
            "language": language,
            "SEO_EN": SEO_EN,
            "SEO_AR": SEO_AR,
            })
            # issue_links.append(url)

    print(f"{url} done")
    # i = i+1
    # if i == 3:
    #     break
# print(games)
with open("game_information", "w",encoding='utf-8') as fp:
    json.dump(games,fp)

with open('issue_links.txt', 'w') as f:
    for issue_link in issue_links:
     f.write(issue_link)
     f.write("\n")

now = datetime.now()
print ("The time is now: = %s:%s:%s" % (now.hour, now.minute, now.second))
