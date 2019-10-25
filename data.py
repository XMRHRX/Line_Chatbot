import os
import sys
import psycopg2
import globalval as gl
from key import URI

# 此檔的全域變數
user_id = ""

def set_user_id():
    # 要先global才能在函式裡修改全域變數
    global user_id
    # 取得不同檔案設定的變數
    user_id = gl.get_value("user_id")

# 在資料庫中尋找表單，找不到的話就建一個
def find_table(table_name):
    # 連到資料庫
    conn = psycopg2.connect(URI, sslmode='require')
    # 取得指標執行資料庫操作
    cur = conn.cursor()
    # 在資料庫中搜尋表單
    cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '" + table_name + "'")
    exist = cur.fetchone()
    # 如果沒有找到表單
    if not exist:
        if table_name == "line_what":
            # 新增line_what表單
            cur.execute(
                "CREATE TABLE line_what ("+
                    "id     varchar(50),"+
                    "ing    varchar(20),"+
                    "value  varchar(100))")
    
    conn.commit() # 提交目前的設定至資料庫中進行修改
    conn.close() # 關閉資料庫連線
    return exist

# 在line_what表單中尋找ID，找到的話回傳現在在做什麼，沒找到的話就新增ID
def find_ing():
    # 連到資料庫
    conn = psycopg2.connect(URI, sslmode='require')
    # 取得指標執行資料庫操作
    cur = conn.cursor()
    # 在line_what表單中尋找ID
    cur.execute("SELECT id FROM line_what WHERE id = '"+user_id+"'")
    exist = cur.fetchone()
    # 如果有找到ID
    if exist:
        # 抓出現在在做甚麼的資料
        cur.execute("SELECT ing FROM line_what WHERE id = '"+user_id+"'")
        exist = cur.fetchone()[0]
    # 沒有找到ID的話
    else:
        # 在line_what表單新增ID
        cur.execute("INSERT INTO line_what VALUES ('"+user_id+"','','')")
        exist = False
    conn.commit() # 提交目前的交易至資料庫中進行修改
    conn.close() # 關閉 PostgreSQL 資料庫連線
    return exist

# 設定現在在做什麼
def set_ing(ing):
    # 連到資料庫
    conn = psycopg2.connect(URI, sslmode='require')
    # 取得指標執行資料庫操作
    cur = conn.cursor()
    # 在line_what表單中修改這個ID的ing(現在在做的事)
    cur.execute("UPDATE line_what SET ing = '" + ing + "' WHERE id = '" + user_id + "'")
    conn.commit() # 提交目前的交易至資料庫中進行修改
    conn.close() # 關閉  PostgreSQL 資料庫連線