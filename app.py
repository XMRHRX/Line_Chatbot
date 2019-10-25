from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import lxml
import os
#以上導入套件
#以下導入自己的檔案
import key
import globalval as gl
from data import *
from pchome import *
#from send_email import *
from shopee import *
from stock import *

#初始化跨檔案變數
gl._init()
#以下設定此檔的全域變數-----------
user_id="U64e7bdac6960662e11e711a92b15475d"
#功能對應，可改成文字
menu_stock = "1"
menu_price = "2"
menu_id    = "3"
menu_reset = "0"
#以上設定此檔的全域變數-----------

app = Flask(__name__)# __name__是這個檔案的路徑
# Channel Access Token 設定line API
line_bot_api = LineBotApi(key.line_bot_api)
# Channel Secret 設定handler
handler = WebhookHandler(key.handler)

# 監聽所有來自 /callback 的 Post Request
# @開頭叫做裝飾器，會執行app.route()，並且把callback()的位置移到app.route()裡面。所以呼叫callback()的話會先執行app.route()
@app.route("/callback", methods = ['POST']) 
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info("Request body:" + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 初始訊息
def start_message():
	push(
		'可使用功能如下：\n'+
		menu_stock+':股票查詢\n'+
		menu_price+':網購比價\n'+
		menu_id+':查看使用者ID')
	set_ing('')

# 處理訊息
@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    # 要先global才能在函式裡修改全域變數
	global user_id
	#設定user_id為使用者ID
	user_id = event.source.user_id
	# 設定跨檔案變數user_id
	gl.set_value("user_id", user_id)
	# 讓data.py取得跨檔案變數
	set_user_id()
	# 設定received_text為收到的訊息
	received_text = event.message.text
	push(ing)
	# 如果沒有找到line_what表單
	if not find_table("line_what"):
		push("機器人第一次使用資料庫，已新建資料表")
	# 如果line_what表單裡沒有此使用者資料
	if find_ing() == False:
		push("使用者第一次使用，已新增資料")
		start_message()
	# 抓使用者進度
	ing=find_ing()

	# 輸入menu_reset對應的文字以重新開始對話
	if received_text == menu_reset:
		start_message()

	# 股票查詢功能
	elif ing == "" and received_text == menu_stock:
		push(
			menu_reset+':取消\n'+
			'1:查詢股票代號\n'+
			'2:查詢即時股價')
		set_ing(menu_stock)
	# 1 股票查詢功能選項
	elif ing == menu_stock and received_text == "1":
		push(
			menu_reset+':取消\n'+
			'查詢中文對照股票代號，可輸入中文或代號:')
		set_ing(menu_stock + '1')
	elif ing == menu_stock and received_text == "2":
		push(
			menu_reset+':取消\n'+
			'查詢即時股價，請輸入代號:')
		set_ing(menu_stock + '2')
	# 11 查詢股票代號
	elif ing == menu_stock + "1":
		push('股票代號查詢中...')
		stock_id_push_message = get_stock_code(_filter = received_text)
		push(stock_id_push_message)
		start_message()
	# 12 查詢即時股價
	elif ing == menu_stock + "2":
		push('即時股價查詢中...')
		stock_price_push_message = stock_realtime_price(sid = received_text)
		push(stock_price_push_message)
		start_message()

	# 網購比價功能
	elif ing == "" and received_text == menu_price:
		push(
			menu_reset+':取消\n'+
			'1:蝦皮比價\n'+
			'2:pchome比價')
		set_ing(menu_price)
	# 2 網購比價功能選項
	elif ing == menu_price and received_text == "1":
		push(
			menu_reset+':取消\n'+
			'利用關鍵字搜尋蝦皮商品:')
		set_ing(menu_price + '1')
	elif ing == menu_price and received_text == "2":
		push(
			menu_reset+':取消\n'+
			'利用關鍵字搜尋pchome商品:')
		set_ing(menu_price + '2')
	# 21 使用蝦皮比價
	elif ing == menu_price + "1":
		push('蝦皮比價查詢中...')
		shopee_price_push_message = shopee_price(keyword = received_text)
		push(shopee_price_push_message)
		start_message()
	# 22 使用pchome比價
	elif ing == menu_price + "2":
		push('pchome比價查詢中...')
		pchome_price_push_message = pchome_price(keyword = received_text)
		push(pchome_price_push_message)
		start_message()

	# 傳送使用者ID
	elif ing == "" and received_text == menu_id:
		push(user_id)
		start_message()

	# 傳送現在在做什麼的代號
	elif received_text == 'ing':
		if ing:
			push(ing)
		else:
			push("初始狀態")
		start_message()

	else:
		push(ing)

# 簡單化傳送指令
def push(text):
	line_bot_api.push_message(user_id, TextSendMessage(text))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
