from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import lxml
import os
# 以上導入套件
# 以下導入自己的檔案
from data import *
import key
import globalval as gl
from compare import Compare_Interface
from stock import *


class StateMachine:
	def __init__(self, rece_text=""):
		"""
        {
            "當下狀態":{（可以選擇的動作）
                            {1(編號 用編號搜尋選項):"股票"（輸出說明）,"next"(搜尋到後 固定用next呼叫):"選擇股票功能"（下個狀態）},
                            {2:"比價","next":"選擇比價功能"},
                            (沒有功能不用寫 固定維持當下狀態)
                        },
            "選擇比價功能":{
                            輸入1（瞎皮）:選擇參數
                            輸入2（批析鬨）:選擇參數
                            選錯:選擇比價功能功能
                            取消：選擇功能
                            }
        }
        """
		self._state_table = {
			"ChooseService": [
				{"1": "查詢股票", "next": "StockFunction"},
				{"2": "網購比價", "next": "PriceFunction"}
			],
			"StockFunction": [
				{"0": "取消", "next": "ChooseService"},
				{"1": "搜尋股票編號", "next": "InputStockName"},
				{"2": "搜尋股票價格", "next": "InputStockID"}
			],
			"InputStockName": [
				{"0": "取消", "next": "ChooseService"},
				{"1": "查詢中文對照股票代號，可輸入中文或代號", "next": 'do_SearchStockName'}
			],
			"InputStockID": [
				{"0": "取消", "next": "ChooseService"},
				{"1": "查詢即時股價，請輸入代號", "next": "do_SearchStockID"}
			],
			"PriceFunction": [
				{"0": "取消", "next": "ChooseService"},
				{"1": "Shopee搜尋", "next": "ShopeeQuery"},
				{"2": "Pchome搜尋", "next": "PchomeQuery"},
				{"3": "全部搜尋", "next": "ALLQuery"}
			],
			"do_SearchStockName":[{"FUNC":self.do_SearchStockName}],
			"do_SearchStockID":[{"FUNC":self.do_SearchStockID}],
			"ShopeeQuery":[{"FUNC":self.ShopeeQuery}],
			"PchomeQuery":[{"FUNC":self.PchomeQuery}],
			"ALLQuery":[{"FUNC":self.ALLQuery}]
			}
			
		self._received_text = rece_text
		self.comp = Compare_Interface(self._received_text)
		if not find_table("line_what"):
		    push("機器人第一次使用資料庫，已新建資料表")

		# 如果line_what表單裡沒有此使用者資料
		if find_ing() == False:
			push("使用者第一次使用，已新增資料")
			self._cur_state = find_ing()
			self.newStart()
		elif find_ing() in self._state_table :
			self._cur_state=find_ing()
		else:
			self.toDefault()

		

	def do_SearchStockName(self):
		push('股票代號查詢中...\n')
		stock_id_push_message = get_stock_code(_filter=self._received_text)
		push(stock_id_push_message)

	def do_SearchStockID(self):	
		push('即時股價查詢中...')
		stock_price_push_message = stock_realtime_price(
	        sid=self._received_text)
		push(stock_price_push_message)

	def ShopeeQuery(self):
		push('蝦皮比價查詢中...')
		shopee_price_push_message = self.comp.Search("shopee")
		push(shopee_price_push_message)

	def PchomeQuery(self):
		push('pchome比價查詢中...')
		pchome_price_push_message = self.comp.Search("pchome")
		push(pchome_price_push_message)

	def ALLQuery(self):
		push('比價查詢中...')
		price_push_message = self.comp.SearchALL()
		push(price_push_message+'\n')

	def newStart(self):
		self.toDefault()
		self.showChoice()

	def toDefault(self):
		self._cur_state = "ChooseService"

	def action(self):
		if  "FUNC" in self._state_table[self._cur_state]:
			self._state_table[self._cur_state]["FUNC"]()
			self.toDefault()
		else:
			self.move()
		set_ing(self._cur_state)

	def move(self):
        # prevent bypass
		step = self._received_text
		if (step.lower() == "next"):
			self.toDefault()
			return
        # check current is in table
		elif(self._cur_state in self._state_table):
            # check every choice depend on current state
			for i in self._state_table[self._cur_state]:
                # find
				if (step in i):
                    # something from table
					self._cur_state = i["next"]
					break
		

		

	def showChoice(self):
		push(self._cur_state)
		for choice in self._state_table[self._cur_state]:
			push(next(iter(choice))+":"+choice[str(next(iter(choice)))])


# 初始化跨檔案變數
gl._init()

app = Flask(__name__)  # __name__是這個檔案的路徑
# Channel Access Token 設定line API
line_bot_api = LineBotApi(key.line_bot_api)
# Channel Secret 設定handler
handler = WebhookHandler(key.handler)

# 監聽所有來自 /callback 的 Post Request
# @開頭叫做裝飾器，會執行app.route()，並且把callback()的位置移到app.route()裡面。所以呼叫callback()的話會先執行app.route()
@app.route("/callback", methods= ['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body:" + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 初始訊息


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 要先global才能在函式裡修改全域變數
    global user_id
    # 設定user_id為使用者ID
    user_id = event.source.user_id
    # 設定跨檔案變數user_id
    gl.set_value("user_id", user_id)
    # 設定received_text為收到的訊息
    received_text = event.message.text

    # get current state
    ing = StateMachine(received_text)
    ing.action()
	
	# show what can do
	ing.showChoice()

    # ========================選擇功能===========================

    # if ing == "":
    # 		#股票
    # 	if received_text == menu_stock:
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'1:查詢股票代號\n'+
    # 			'2:查詢即時股價')
    # 		set_ing(menu_stock)
    # 		#比價
    # 	elif received_text == menu_price:
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'1:蝦皮 比價\n'+
    # 			'2:pchome 比價\n'+
    # 			'3:pchome+蝦皮 比價')
    # 		set_ing(menu_price)

    # 		# 傳送使用者ID
    # 	"""elif received_text == menu_id:
    # 		push("此功能以關閉：P")
    # 		start_message()"""
    # #=======================================================
    # #========================股票查詢功能=====================

    # #1 股票查詢功能選項
    # elif ing == menu_stock:
    # 	if received_text == "1":
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'查詢中文對照股票代號，可輸入中文或代號:')
    # 		set_ing(menu_stock + '1')
    # 	elif received_text == "2":
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'查詢即時股價，請輸入代號:')
    # 		set_ing(menu_stock + '2')
    # # 11 查詢股票代號
    # elif ing == menu_stock + "1":
    # 	push('股票代號查詢中...')
    # 	stock_id_push_message = get_stock_code(_filter = received_text)
    # 	push(stock_id_push_message)
    # 	start_message()
    # # 12 查詢即時股價
    # elif ing == menu_stock + "2":
    # 	push('即時股價查詢中...')
    # 	stock_price_push_message = stock_realtime_price(sid = received_text)
    # 	push(stock_price_push_message)
    # 	start_message()
    # #================================================================

    # #======================== 網購比價功能=============================

    # # 2 網購比價功能選項
    # elif ing == menu_price:
    # 	if received_text == "1":
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'利用關鍵字搜尋蝦皮商品:')
    # 		set_ing(menu_price + '1')
    # 	elif received_text == "2":
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'利用關鍵字搜尋pchome商品:')
    # 		set_ing(menu_price + '2')
    # 	elif received_text == "3":
    # 		push(
    # 			menu_reset+':取消\n'+
    # 			'利用關鍵字搜尋pchome和蝦皮商品:')
    # 		set_ing(menu_price + '3')
    # # 21 使用蝦皮比價
    # elif ing == menu_price + "1":
    # 	push('蝦皮比價查詢中...')
    # 	comp = Compare_Interface(received_text)
    # 	shopee_price_push_message = comp.Search("shopee")
    # 	push(shopee_price_push_message)
    # 	start_message()
    # # 22 使用pchome比價
    # elif ing == menu_price + "2":
    # 	push('pchome比價查詢中...')
    # 	comp = Compare_Interface(received_text)
    # 	pchome_price_push_message = comp.Search("pchome")
    # 	push(pchome_price_push_message)
    # 	start_message()
    # elif ing == menu_price + "3":
    # 	push('比價查詢中...')
    # 	comp = Compare_Interface(received_text)
    # 	price_push_message = comp.SearchALL()

    # 	push(price_push_message+'\n')
    # 	start_message()
    # #==============================================================

    # # 傳送現在在做什麼的代號
    # elif received_text == 'ing':
    # 	if ing:
    # 		push(ing)
    # 	else:
    # 		push("初始狀態")
    # 	start_message()

# 簡單化傳送指令


def push(text):
    line_bot_api.push_message(user_id, TextSendMessage(text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
