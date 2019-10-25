#關鍵字
keyword='中秋節'

#爬文章的'頁數'，，每頁20篇文章。為避免造成對方伺服器負擔，每頁間有設定5秒休息時間
page_n =1

#board參數
board = 'Gossiping'  #如果要換不同的板，請更改這個參數 
'''
e.g.
這是八卦板的網址→https://www.ptt.cc/bbs/Gossiping/index.html
假如我想換成NBA板(https://www.ptt.cc/bbs/NBA/index.html)
可以看出網址邏輯為bbs/板名/index.html，因此將Gossiping改成NBA即可
'''

#正負向詞彙位置
pos_neg_word_file = '正負向詞彙.xlsx'


#ppt中，要顯示的參數
page3_article_show_n = 4   #在第三頁中，要顯示幾筆文章
page5_word_show_n=10  #在第五頁中，要顯示幾個正負向詞彙


#寄信
from_gmail_user = 'your_account@gmail.com'
from_gmail_password = 'your_password'
to_user = 'target_account@gemail.yuntech.edu.tw'

#設定寄件資訊
Subject = "當機器人來上班--每日輿情分析報表"
contents = """
當機器人來上班--每日輿情分析報表
""" 
#附件存檔與讀取名稱
attach_file_name_1='每日報表.pptx'

#附件存檔與讀取名稱
attach_file_name_2='每日輿情分析資料-文章.xlsx'

#設定信件伺服器
which_server = 'smtp.gmail.com'
server_smtp_port = 465





#爬蟲node參數
title_node = '.title a'
date_node = '.date'
push_node = '.nrec'
