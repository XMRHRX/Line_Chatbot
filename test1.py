# import child as ch
#import testParent as aa
# a = ch.Child(111)
# a.sss()

# a = aa.Parent()
# a.sss()

# num = {0:{"one":"data"},2:"two",1:"one"}
# print(num[0]["one"])


# a = {'test':1,"BON":4}
# b={"aa":0,"cc":1,'test':2}
# print(a[0])

# for i in b:
#     if(b[i] in a.values() ):
#         print(i,"IN",a)


table={
            "ChooseService":[
                                {"1":"查詢股票","next":"StockFunction"},
                                {"2":"網購比價","next":"PriceFunction"}
                            ],
            "StockFunction":[
                            {0:"取消","next":"ChooseService"},
                            {1:"搜尋股票編號","next":"SearchStockName"},
                            {2:"搜尋股票價格","next":"InputStockID"}
                        ],
            "SearchStockName":[
                            {0:"取消","next":"ChooseService"},
                            {1:"查詢中文對照股票代號，可輸入中文或代號","next":"do_SearchStockName"}
                        ],
            "InputStockID":[
                            {0:"ChooseService",1:"查詢即時股價，請輸入代號","next":"do_SearchStockID"}
                        ] ,
            "PriceFunction":[
                            {0:"取消","next":"ChooseService"},
                            {1:"Shopee搜尋","next":"InputQuery"},
                            {2:"Pchome搜尋","next":"InputQuery"},
                            {3:"全部搜尋","next":"InputQuery"}
                        ]
        }

# cur = 'ChooseService'
# step = 1
# for i in table[cur]:
#     print(next(iter(i)),":",i[next(iter(i))] )

state_table = {
            "ChooseService": [
                {"1": "查詢股票", "next": "StockFunction"},
                {"2": "網購比價", "next": "PriceFunction"}
            ],
            "StockFunction": [
                {"0": "取消", "next": "ChooseService"},
                {"1": "搜尋股票編號", "next": "InputStockName"},
                {"2": "搜尋股票價格", "next": "InputStockID"}
            ]
        }

cur='ChooseService'
print(13)
for choice in state_table[cur]:
    print(next(iter(choice)), ":", choice[str(next(iter(choice)))])