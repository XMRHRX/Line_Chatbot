import twstock
import requests
import pandas as pd


#股票代號查詢功能
def get_stock_code(strMode=2,_filter = None): 
#向網頁要求資料
	res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode="+str(strMode))

	#將網頁的原始碼轉換為可閱讀的表格
	df = pd.read_html(res.text)[0]

	# 設定column名稱
	df.columns = df.iloc[0]

	# 刪除第一行
	df = df.iloc[1:]

	# 移除備註columns
	df = df.drop(columns='備註')
	
	#移除"上市認購(售)權證"等非股票項目
	df = df[~df['產業別'].isna()]
	
	#篩選並把移除空值(NAN補空白)，重設index
	df = df[df['有價證券代號及名稱'].apply(lambda x : str(_filter) in x)].fillna(" ").reset_index(drop=True)
	Chinese_Code_list_raw = df['有價證券代號及名稱']
	
    #清理爬回來的資料，組合成代碼<>中文的表格方便待會查詢
	stock_code = []
	stock_chinese= []
	for raw_text in Chinese_Code_list_raw:
		raw_text_split = raw_text.split()
		stock_code.append(raw_text_split[0])
		stock_chinese.append(raw_text_split[1])
	
	
	clean_result = pd.DataFrame({"股票代碼":stock_code,
				"股票中文名稱":stock_chinese})
	
	if len(clean_result) == 0:
		return("查無股票!請確認輸入項目是否正確")
	else:
		return(clean_result.to_string(index=False))
		

#即時股價功能		
def stock_realtime_price(sid="error_id"):
    stock_price_result = twstock.realtime.get(str(sid))
    if stock_price_result['success']:
        t = '查詢代號\n'+str(sid)+'\n'+\
'最新成交價\n'+stock_price_result['realtime']['latest_trade_price']+'\n'+\
'開盤價\n'+stock_price_result['realtime']['open']+'\n'+\
'最高價\n'+stock_price_result['realtime']['high']+'\n'+\
'最低價\n'+stock_price_result['realtime']['low']+'\n'
        return(t)
    else:
        return('請輸入正確代碼')