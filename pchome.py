from OnlineShop import *

import urllib
import json
import requests
import pandas as pd

#pchome比價功能
class PChome(Shop):
    #參數
    def __init__(self,target , default_search = 0 ,defaul_sort=0, default_num = 5):
        super().__init__(target , default_search  ,defaul_sort, default_num)
        accept_sort = {0:'ac',1:'dc'}
        accept_search = {0:'prc',1:'rnk',2:'new',3:'sale'}#0:price 2:new 1:accuracy
        self.request_num=self._request_num
        self.target = self._target
        self.order_by = self.checkAccept(self._sort_by , accept_sort )
        self.search_by = self.checkAccept(self._search_by, accept_search )

    

    def Search(self):

        #生成查詢頁面的網址
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+urllib.parse.quote(self.target)+'&page=1&sort='+self.search_by+'/'+self.order_by
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
        if self.request_num > len(result):
            self.request_num = len(result)
        
        #生成文字
        t=''

        for i in range(self.request_num):
            t = t+'第'+str(i+1)+'名:\n'+\
            name[i]+'\n'+\
            '價格：'+str(price[i])+'\n'+\
            '購買網址：'+buy_url[i]+'\n\n'

        return(t)