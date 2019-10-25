import urllib
import json
import requests
#蝦皮比價功能
def shopee_price(keyword):
    #參數
    how_many_item_i_need=5
    search_by = 'price' #綜合排名：relevancy    價格：price    新上市：ctime    最熱銷：sales
    order_by = 'asc'  #遞增：asc  遞減：desc
    
    #生成網址
    url = 'https://shopee.tw/api/v2/search_items/?by='+search_by+'&keyword='+urllib.parse.quote(keyword)+'&limit='+str(how_many_item_i_need)+'&newest=0&order='+order_by+'&page_type=search'
    response = requests.get(url,
        headers = {
        'User-Agent': 'Googlebot',
        'cookie': '_gcl_au=1.1.519625963.1565756634; _med=refer; SPC_IA=-1; SPC_EC=-; SPC_F=fMMzZVTeg7HU0klqtscTmHz7aNWchorz; REC_T_ID=55bbaf9a-be4b-11e9-a764-f8f21e1ab7e0; SPC_U=-; _fbp=fb.1.1565756634056.1426173981; _ga=GA1.2.1310878136.1565756635; __BWfp=c1565756639587x1acbfd449; cto_lwid=8953f472-92f4-4182-8621-e6ee93a02357; SPC_SI=8a00gkmq3k54bsjj84vm0t8pdkpwsxd8; REC_MD_20=1567670474; csrftoken=0EsLK1rfQ3m8107QYzVmVSn5C62qke2a; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.2.1135347982.1567670376; REC_MD_14=1567670640; REC_MD_30_2000026608=1567670732; _dc_gtm_UA-61915057-6=1; SPC_T_IV="znr93s7tSe9UipUfoYEKmQ=="; SPC_T_ID="72lAoodt6cXTaFzMIebWDFo0gn/HS2RJaqvhBhzwfA5rxkmstamxwaaPmft67xx35IgfekzcrDpfQtqlWPdYUOIDVpUQ9OQunctWx5tiJr8="',
        'if-none-match': '"c2b8ef1a22487acf64ab242832602c8a;gzip"',
        'if-none-match-': '55b03-37b77fa9ebd20ab5d0ae24e962c0231e'})
    
    
    #清理資料
    text = json.loads(response.text)
    price_min=[]
    price_max=[]
    name=[]
    shop_id=[]
    item_id=[]

    for items_text in text['items']:
        item_id.append(items_text['itemid'])
        shop_id.append(items_text['shopid'])
        price_min.append(int(items_text['price_min']/100000))
        price_max.append(int(items_text['price_max']/100000))
        name.append(items_text['name'])
    
    #生成文字
    t = ''
    for i in range(how_many_item_i_need):
        t = t+'第'+str(i+1)+'名:\n'+\
        name[i]+'\n'+\
        '價格：'+str(price_min[i])+'~'+str(price_max[i])+'\n'+\
        '購買網址：'+shorten_url('https://shopee.tw/'+name[i].replace(' ','-')+'-i.'+str(shop_id[i])+'.'+str(item_id[i]))+'\n\n'
    return(t)

#縮網址
def shorten_url(long):
	URL = "http://tinyurl.com/api-create.php"
	r = requests.get(URL+"?"+urllib.parse.urlencode({"url": long}))
	return(r.text)
	