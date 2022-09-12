from bs4 import BeautifulSoup
import requests
import re
links=[]
crocodice= "https://crocodice.net"

for page in range(1,25):
    print(page)
    url = f"https://crocodice.net/collections/all-games?page={page}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    for a in doc.find_all('a', href=True):
        if 'products' in a['href']:
            links.append(crocodice+ a['href'])

    # print(links)
for link in links:
    print(link)
#
#
with open('gamelink.txt', 'w') as f:
    for line in links:
     f.write(line)
     f.write("\n")



"""
[

]
"""
