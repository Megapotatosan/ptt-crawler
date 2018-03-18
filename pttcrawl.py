from bs4 import BeautifulSoup
import requests
import re
import time
import sys
from collections import OrderedDict
import itertools
def crawl():
    exception = ["https://www.ptt.cc/bbs/Beauty/M.1490936972.A.60D.html",
                "https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html",
                "https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html",
                "https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html",
                "https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html",
                "https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html",
                "https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html",
                "https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html"]
    URL = "https://www.ptt.cc/bbs/Beauty"
    print("crawling~~~~~")
    allarticles = open('all_articles.txt', 'w', encoding="utf-8")
    allpopular = open('all_popular.txt', 'w', encoding="utf-8")
    for i in range(2000, 2352):
        content = requests.get(url=URL + '/index' + str(i) + '.html')
        soup = BeautifulSoup(content.text, 'html.parser')
        articles = soup.find_all("div", class_="r-ent")
        for articles in articles:
            try:
                datetag = articles.find('div', attrs={'class': 'date'})
                href = 'https://www.ptt.cc' + articles.find('a')['href']
                author = articles.find('div', attrs={'class': 'author'})
                date_str = datetag.text.replace('/', '').replace(' ', '')
                title = articles.find('a').text
                articles_str = date_str + ',' + title + ',' + href + '\n'
                if i == 2000:
                    if " 1/01" in datetag.contents:
                        if '公告' not in articles_str and href not in exception:
                            allarticles.write(articles_str)
                        if '爆' in articles.find("span").text and href not in exception:
                            allpopular.write(articles_str)
                elif i >= 2351:
                    if "12/31" in datetag.contents:
                        if '公告' not in articles_str and href not in exception:
                            allarticles.write(articles_str)
                        if '爆' in articles.find("span").text and href not in exception:
                            allpopular.write(articles_str)
                else:
                    if '公告' not in articles_str and href not in exception:
                        allarticles.write(articles_str)
                    if '爆' in articles.find("span").text and href not in exception:
                        allpopular.write(articles_str)
            except:
                pass
        time.sleep(0.2)
        print(i, " done")
    allarticles.close()
    allpopular.close()

def push(start,end):
    startdate = start
    enddate = end
    filename = 'push['+startdate+'-'+enddate+"].txt"
    userpush = {}
    userboo = {}
    print (filename)
    with open('all_articles.txt', 'r', encoding="utf-8") as readfile:
        with open(filename,"w",encoding="utf-8") as writefile:
            for line in readfile:
                currentline = line.split(",")
                if int(currentline[0]) >= int(startdate) and int(currentline[0]) <= int(enddate):
                    URL = currentline[-1].strip('\n')
                    print(URL)
                    time.sleep(0.1)
                    content = requests.get(url=URL)
                    if content.status_code != 404:
                        soup = BeautifulSoup(content.text, 'html.parser')
                        articles = soup.find_all("div", class_="push")
                        for articles in articles:
                            try:
                                pushtag = articles.find('span', attrs={'class': 'push-tag'}).get_text().strip(' ')
                                author = articles.find('span', attrs={'class': 'f3 hl push-userid'}).get_text().strip(' ')
                                if author not in userpush:
                                    if pushtag == "推":
                                        userpush[author] = 1
                                elif author in userpush:
                                    if pushtag == "推":
                                        userpush[author] += 1
                                if author not in userboo:
                                    if pushtag == "噓":
                                        userboo[author] = 1
                                elif author in userboo:
                                    if pushtag == "噓":
                                        userboo[author] += 1
                            except:
                                pass
                    else:
                        print("404 error")
                print(currentline[0],'done\n')
            print("---------------------")
            ordered_userpush = OrderedDict(sorted(userpush.items(),reverse=True, key=lambda t: t[1]))
            ordered_userboo = OrderedDict(sorted(userboo.items(),reverse=True, key=lambda t: t[1]))
            firsttenpush = itertools.islice(ordered_userpush.items(), 0, 10)
            firsttenboo = itertools.islice(ordered_userboo.items(), 0, 10)
            i = 1
            sumpush = "all like: "+str(sum(ordered_userpush.values()))+"\n"
            sumboo = "all boo: " + str(sum(ordered_userboo.values())) + "\n"
            writefile.write(sumpush)
            writefile.write(sumboo)
            for key, value in firsttenpush:
                like_str = "Like #"+str(i)+": "+key+" "+ str(value)+"\n"
                writefile.write(like_str)
                i += 1
            i = 1
            for key, value in firsttenboo:
                boo_str = "Boo #" + str(i) + ": " + key+" " + str(value) + "\n"
                writefile.write(boo_str)
                i += 1
    readfile.close()
    writefile.close()

def popular(start,end):
    startdate = start
    enddate = end
    filename = 'popular[' + startdate + '-' + enddate + "].txt"
    regex = re.compile('https?://\S+?\.(?:jpg|jpeg|gif|png)$')
    print(filename)
    i = 0
    with open('all_popular.txt', 'r', encoding="utf-8") as readfile:
        with open(filename, "w", encoding="utf-8") as writefile:
            for line in readfile:
                currentline = line.split(",")
                if int(currentline[0]) >= int(startdate) and int(currentline[0]) <= int(enddate):
                    i += 1
                    URL = currentline[-1].strip('\n')
                    print(URL)
                    time.sleep(0.1)
                    content = requests.get(url=URL)
                    if content.status_code != 404:
                        soup = BeautifulSoup(content.text, 'html.parser')
                        for a in soup.find_all('a', href=True):
                            if re.match(regex,a['href']) is not None:
                                writefile.write(str(a['href'])+'\n')
                    else:
                        print("404 error")
            numline = 'number of popular articles: '+str(i)+'\n'
    readfile.close()
    writefile.close()
    f = open(filename, 'r+')
    lines = f.readlines()  # read old content
    f.seek(0)  # go back to the beginning of the file
    f.write(numline)  # write new content at the beginning
    for line in lines:  # write old content after new
        f.write(line)
    f.close()

def keyword(keyword,start,end):
    startdate = start
    enddate = end
    imgregex = re.compile('https?://\S+?\.(?:jpg|jpeg|gif|png)$')
    filename = 'keyword('+str(keyword)+')[' + startdate + '-' + enddate + "].txt"
    with open('all_articles.txt', 'r', encoding="utf-8") as readfile:
        with open(filename, "w", encoding="utf-8") as writefile:
            for line in readfile:
                currentline = line.split(",")
                if int(currentline[0].strip('\n')) >= int(startdate) and int(currentline[0].strip('\n')) <= int(enddate):
                    URL = currentline[-1].strip('\n')
                    time.sleep(0.5)
                    content = requests.get(url=URL)
                    if content.status_code != 404:
                        soup = BeautifulSoup(content.text, 'html.parser')
                        articles = soup.find_all('div',class_='bbs-screen bbs-content')
                        checkcontent = str(articles).split("--")[0]
                        if str(keyword) in checkcontent:
                            print("keyword found")
                            for a in soup.find_all('a', href=True):
                                if re.match(imgregex, a['href']) is not None:
                                    writefile.write(str(a['href']) + '\n')
                    else:
                        print("404 error")
    readfile.close()
    writefile.close()
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(" help : use crawl | push (start) (end) | popular (start) (end) | keyword (keyword) (start) (end) ")
        sys.exit()
    elif sys.argv[1] == "crawl":
        crawl()
    elif sys.argv[1] == "push":
        if len(sys.argv) < 4:
            print("wrong argument")
        else:
            push(sys.argv[2] , sys.argv[3])
    elif sys.argv[1] == "popular":
        if len(sys.argv) < 4:
            print("wrong argument")
        else:
            popular(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "keyword":
        if len(sys.argv) < 5:
            print("wrong argument")
        else:
            keyword(sys.argv[2], sys.argv[3], sys.argv[4])




