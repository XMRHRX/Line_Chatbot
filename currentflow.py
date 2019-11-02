import data as dt
from compare import Compare_Interface
from app import push
from stock import *


class StateMachine():

    def __init__(self, received_text=""):
        self._push_string = ""
        self._received_text = received_text
        self.comp = Compare_Interface(received_text)
        if not dt.find_table("line_what"):
            push("機器人第一次使用資料庫，已新建資料表")

        # 如果line_what表單裡沒有此使用者資料
        if dt.find_ing() == False:
            push("使用者第一次使用，已新增資料")
            self._cur_state = dt.find_ing()
            self.newStart()
        # 抓使用者進度
        self._cur_state = dt.find_ing()
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
        self._action_list = ["do_SearchStockName",
                             "do_SearchStockID", "ShopeeQuery", ]
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
                {"1": "查詢中文對照股票代號，可輸入中文或代號", "next": self.do_SearchStockName}
            ],


            "InputStockID": [
                {"0": "取消", "next": "ChooseService"},
                {"1": "查詢即時股價，請輸入代號", "next": self.do_SearchStockID}
            ],
            "PriceFunction": [
                {"0": "取消", "next": "ChooseService"},
                {"1": "Shopee搜尋", "next": self.ShopeeQuery},
                {"2": "Pchome搜尋", "next": self.PchomeQuery},
                {"3": "全部搜尋", "next": self.ALLQuery}
            ]
        }

    def do_SearchStockName(self):
        push('股票代號查詢中...\n')
        stock_id_push_message = get_stock_code(_filter=self._received_text)
        push(stock_id_push_message)
        self.toDefault()

    def do_SearchStockID(self):

        push('即時股價查詢中...')
        stock_price_push_message = stock_realtime_price(
            sid=self._received_text)
        push(stock_price_push_message)
        self.toDefault()

    def ShopeeQuery(self):
        push('蝦皮比價查詢中...')
        shopee_price_push_message = self.comp.Search("shopee")
        push(shopee_price_push_message)
        self.toDefault()

    def PchomeQuery(self):
        push('pchome比價查詢中...')
        pchome_price_push_message = self.comp.Search("pchome")
        push(pchome_price_push_message)
        self.toDefault()

    def ALLQuery(self):
        push('比價查詢中...')
        price_push_message = self.comp.SearchALL()
        push(price_push_message+'\n')
        self.toDefault()

    def newStart(self):
        self.toDefault()
        self.showChoice()

    def toDefault(self):
        self._cur_state = "ChooseService"

    def action(self):
        if self._cur_state in self._action_list:
            self._cur_state()
        else:
            self.move()

    def move(self):
        # prevent bypass
        step = self._received_text
        if (step.lower() == "next"):
            self.toDefault()
            return

        if self._cur_state in self._action_list:
            self._cur_state()

        # check current is in table
        elif not (self._cur_state in self._state_table):
            self.toDefault()

        elif(self._cur_state in self._state_table):
            # check every choice depend on current state
            for i in self._state_table[self._cur_state]:
                # find
                if (step in self._state_table[self._cur_state][i]):
                    # something from table
                    self._cur_state = self._state_table[self._cur_state][i]["next"]

    def showChoice(self):
        for choice in self._state_table[self._cur_state]:
            print(next(iter(choice)), ":", choice[next(iter(choice))])
