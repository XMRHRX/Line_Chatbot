import urllib
import json
import requests
import pandas as pd

#pchome比價功能
def pchome_price(keyword):
    #參數
    how_many_item_I_need=5
    rank_type = 'rnk/dc'   #有貨優先：sale/dc    精準度：rnk/dc    價格低到高：prc/dc    價格高到低：prc/ac    新上市：new/dc
    
    
    #生成查詢頁面的網址
    url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+urllib.parse.quote(keyword)+'&page=1&sort='+rank_type
    prod_url='https://24h.pchome.com.tw/prod/'
    r = requests.get(url)
    t = json.loads(r.text)
    
    #整理回傳的json檔案
    name=[]
    price=[]
    prod_id= []
    buy_url =[]
    for prod in t['prods']:
        prod_id.append(prod['Id'])
        price.append(prod['price'])
        name.append(prod['name'])
        buy_url.append(prod_url+prod['Id'])
        
    #整理成表格，並排序&移除重複
    result = pd.DataFrame({
    'prod_id':prod_id,
    'price':price,
    'name':name,
    'buy_url':buy_url
    }).drop_duplicates(['name','price']).sort_values('price').reset_index(drop=True)
    

    #如果要求的數量大於回傳結果長度，把要求數量改成結果長度
    if how_many_item_I_need > len(result):
        how_many_item_I_need = len(result)
    
    #生成文字
    t=''

    for i in range(how_many_item_I_need):
        t = t+'第'+str(i+1)+'名:\n'+\
        name[i]+'\n'+\
        '價格：'+str(price[i])+'\n'+\
        '購買網址：'+buy_url[i]+'\n\n'

    return(t)