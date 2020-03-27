from gen import gen
from pprint import pprint
import requests
from bs4 import BeautifulSoup as bs4
import random

def make():
    gen()
    with open("gen.txt","r",encoding="utf-8",errors="ignore") as f:
        wL = f.readlines()
    query = random.choice(wL)
    imgUrl = getImg(query)
    res = requests.get(imgUrl)
    while res.status_code != 200:
        res = requests.get(getImg(query))
    with open("img.jpg","wb") as f:
        f.write(res.content)
    return query

def getRandom():
    url = "https://www.wikihow.com/Special:Randomizer"
    res = requests.get(url)
    soup = bs4(res.content,"html.parser")
    imgs = ["https://wikihow.com"+x["data-srclarge"] for x in soup.findAll("img",{"class":"whcdn content-fill"})]
    filtered = ["/".join(a.replace("/thumb","").split("/")[:-1]) for a in imgs]
    return random.choice(filtered)

def getFixed(id=5209):
    baseUrl = "https://www.wikihow.com/?curid="
    url = baseUrl + str(id)
    res = requests.get(url)
    soup = bs4(res.content,'html.parser')
    imgs = ["https://www.wikihow.com"+x['data-srclarge'] for x in soup.findAll("img",{"class":"whcdn content-fill"})]
    filtered = ["/".join(a.replace("/thumb","").split("/")[:-1]) for a in imgs]
    if len(filtered)!=0:
        return random.choice(filtered)
    return []

def getImg(query="How to take care of fish with AIDS"):
    sess = requests.Session()
    baseUrl = "https://wikihow.com/api.php"
    params = {"action":"query","format":"json","list":"search","srsearch":query}
    res = sess.get(url=baseUrl,params=params)
    data = res.json()
    base = data["query"]["search"]
    if len(base)>0:
        final = [a["pageid"] for a in base]
        if len(final) != 0:
            t = random.choice(final)
            n = getFixed(t)
            final.remove(t)
            while len(n) == 0 and len(final) != 0:
                t = random.choice(final)
                n = getFixed(t)
                final.remove(t)
            return n
    return getRandom()

if __name__ == "__main__":
    print(getImg(query=input("Enter query: ")))
