'''
Created on 2021. 9. 13.

@author: user
'''
import requests
from bs4 import BeautifulSoup
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import os
from pyboard.settings import STATIC_DIR, TEMPLATE_DIR
from konlpy.tag._okt import Okt
from collections import Counter
import pytagcloud
import pandas as pd
import folium
from folium import plugins
def movie_crawling(data):
    for i in range(1,101):
        base="https://movie.naver.com/movie/point/af/list.naver?&page="
        url=base+str(i)
        req=requests.get(url)
        if req.ok:
            html=req.text
            soup=BeautifulSoup(html,'html.parser')
            titles=soup.select('.title > a.movie')
            points=soup.select('.title em')
            contents=soup.select('.title')
            n=len(titles)
            
            for i in range(n):
                title=titles[i].get_text()
                point=points[i].get_text()
                contentArr=contents[i].get_text().replace('신고','').split('\n\n')
                content=contentArr[2].replace('\t','').replace('\n','')
                data.append([title, point,content])
                print(title,point,content)
                
def makeGraph(titles,points):
    font_path="c:\Windows/fonts/malgun.ttf"
    font_name=font_manager.FontProperties(fname=font_path).get_name()
    rc('font',family=font_name)
    plt.title("영화 평점")
    plt.xlabel("영화 제목")
    plt.ylabel('평균평점')
    plt.grid(True)
    plt.bar(range(len(titles)),points, align='center')
    plt.xticks(range(len(titles)),list(titles),rotation=90)
    plt.savefig(os.path.join(STATIC_DIR,'images/fig01.png'),dpi=300)
    
def makeWordCloud(contents):
    nlp=Okt()
    fontname=''
    wordtext=""
    for t in contents:
        wordtext+=str(t)+" "
        
    nouns=nlp.nouns(wordtext)
    count=Counter(nouns)
    wordInfo=dict()
    for tags, counts in count.most_common(100):
        if(len(str(tags)) > 1):
            wordInfo[tags]=counts
            
    filename=os.path.join(STATIC_DIR,'images/wordcloud01.png')
    taglist=pytagcloud.make_tags(dict(wordInfo).items(),maxsize=80)
    pytagcloud.create_tag_image(taglist,filename, size=(800,600),
                                fontname='Korean', rectangular=False)
    
    # webbrowser(img)
    
def cctv_map():
    popup=[]
    data_lat_lng=[]
    a_path='c:/Temp/'
    df=pd.read_csv(os.path.join(a_path,'CCTV.csv'),encoding='CP949')
    print(pd)
    for data in df.values:
        if data[4] > 0:
            popup.append(data[1])
            data_lat_lng.append([data[10],data[11]])
            
    m=folium.Map([35.16242332,129.0441629],zoop_start=14)
    plugins.MarkerCluster(data_lat_lng,popups=popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR,'map/map01.html'))
            
        