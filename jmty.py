import requests
from bs4 import BeautifulSoup

from jmty_settings import send_notification,jmty_items

def get_date(detail_url):
    detail_r = requests.get(detail_url)
    detail_soup = BeautifulSoup(detail_r.text, "html.parser")
    detail_date = detail_soup.find_all('div',{"class":"p-article-history"})[0].findChildren("div")
    return ["".join(d.getText().split()) for d in detail_date]

def update_saved_items(allitems):
    try:
        with open("jmty.txt","r") as f:
            saved = f.readlines()
            saved = [s.strip() for s in saved if len(s.strip())]
    except: saved = []
    new_items = []
    for item in allitems:
        if len(item.findChildren("div",{"class":"p-item-close"})):
            continue
        item_info = item.findChild("div",{"class":"p-item-content-info"})
        item_title = item_info.findChild("a")
        url = item_title.get("href")
        item_date = get_date(url)
        item_line = "{} {} {}".format(url,item_title.getText()," ".join(item_date))
        if url not in [s.split()[0] for s in saved]:
            new_items.append(item_line)
            send_notification(item_line)
        else:
            # delete old line
            saved = [s for s in saved if s.split()[0] != url]
        saved.append(item_line)

    with open("jmty.txt","w") as f:
        f.write("\n".join(saved))
        f.write("\n")
    with open("jmty_new.txt","w") as f:
        f.write("\n".join(new_items))
        f.write("\n")
    return new_items

def get_items(selected_area,keyword):
    target_url = 'https://jmty.jp/osaka/sale-all/g-all/{}?keyword={}&max=0&min=0'.format(selected_area,keyword)
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")
    allitems = soup.find_all('li',{"class":"p-articles-list-item"})
    update_saved_items(allitems)

for i in jmty_items:
    get_items(i[0],i[1])
