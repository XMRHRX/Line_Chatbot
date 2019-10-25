from email.mime.text import MIMEText
import pandas as pd
import smtplib
'''
請手動安裝pandas、openpyxl、xlrd
於cmd輸入pip install --upgrade pip 更新後
輸入pip install XXXXX
'''


# 設定寄件人資料
# HOST
smtpHost = 'smtp.gmail.com'
# 寄件人mail
sender   = '@gmail.com'
# 寄件人mail密碼
password = ''


# 輸入選項
input1 = input("請注意!Gmail一天只能寄500封信\n1.設定格式\n2.發送mail\n:")
# 如果選項輸入1
if input1 == "1":
    # 儲存空間，會是之後Excel檔的標頭，預先放入信箱，之後放入標題跟內容
    dit    = {"信箱":[]}
    # 輸入標題分幾段
    input2 = input("請注意!若email.xlsx已開啟，請將它關閉，以免寫入失敗\n請問標題要分幾段?\n:")
    # 標題分幾段就執行幾次
    for i in range(int(input2)):
        # 輸入欄位名稱
        dit.setdefault("標題" + str(i+1) + ":" + input("請輸入標題欄位 " + str(i+1) + " 名稱:"),[])
    # 輸入內文分幾段
    input3 = input("請問內容要分幾段?\n:")
    # 內容分幾段就執行幾次
    for i in range(int(input3)):
        # 輸入內文名稱
        dit.setdefault("內容" + str(i+1) + ":" + input("請輸入標題欄位 " + str(i+1) + " 名稱:"),[])
    # 嘗試儲存成Excel檔
    try:
        # 資料
        df        = pd.DataFrame(dit)
        # 檔名
        file_path = 'email.xlsx'
        # 準備寫入
        writer    = pd.ExcelWriter(file_path)
        # 開始寫入(編碼UTF-8，表單名稱sheet1)
        df.to_excel(writer, index=False,encoding='utf-8',sheet_name='sheet1')
        # 存檔
        writer.save()
    # 失敗的話
    except:
        print("寫入失敗，請確認檔案已關閉後再試一次")
    # 成功的話
    else:
        print("寫入成功，編輯後即可發信")
# 如果選項輸入2
elif input1 == "2":
    # 讀取檔案
    df        = pd.read_excel('email.xlsx')
    # 取得標頭
    df_header = df.columns.values
    # 取得資料
    df_list   = df.values
    # 資料列數
    y         = len(df_list)
    # 資料欄數
    x         = len(df_list[0])
    # 新增存放空間，之後整理完把資料放入
    email     = []
    title     = []
    content   = []
    # 資料有幾列就執行幾次，抓出每列資料，整理後放入存放空間
    for i in range(y):
        # 在存放空間新增一筆資料
        email.append("")
        title.append("")
        content.append("")
        # 資料有幾欄就執行幾次
        for j in  range(x):
            # 如果是第一個欄位
            if j == 0:
                # 把第一欄的資料放入信箱的存放空間
                email[i]=df_list[i][0]
            # 如果是標題
            elif df_header[j][0:2:1] == "標題":
                # 如果沒有資料的話
                if type(df_list[i][j]) is float:
                    # 複製第一列的資料到標題的存放空間
                    title[i] += df_list[0][j]
                # 有資料的話
                else:
                    # 複製資料到標題的存放空間
                    title[i] += df_list[i][j]
            # 如果是內容
            elif df_header[j][0:2:1] == "內容":
                # 如果沒有資料的話
                if type(df_list[i][j]) is float:
                    # 複製第一列的資料到內容的存放空間
                    content[i] += df_list[0][j]
                # 有資料的話
                else:
                    # 複製資料到內容的存放空間
                    content[i] += df_list[i][j]
        # 展示資料
        print("收件人"+ str(i+1) +" 信箱:" + email[i] + " 標題:" + title[i] + " 內容:" + content[i])
    # 輸入是否寄出
    input4 = input("確認寄出嗎?(Y/N):")
    # 如果輸入Y或y
    if input4.lower() == "y":
        print("確認寄出")
        # 資料有幾列就執行幾次
        for i in range(y):
            # 設定寄件內文
            msg = MIMEText(content[i])
            # 設定寄件人
            msg['From']    = sender
            # 設定收件人
            msg['To']      = email[i]
            # 設定寄件標題
            msg['Subject'] = title[i]
            # 嘗試寄出
            try:
                # smtp
                smtpServer = smtplib.SMTP_SSL(smtpHost, 465)     # 465用這行
                # smtpServer = smtplib.SMTP(smtpHost, 587)       # 25跟587用這行。
                # smtpServer.ehlo()                              # 25跟587需要這行。465不需要。
                # smtpServer.starttls()                          # 25跟587需要這行。465不需要。
                # 登入信箱
                smtpServer.login(sender, password)
                # 寄出信件
                smtpServer.sendmail(sender, email[i], msg.as_string())
                smtpServer.quit()
            # 寄件失敗的話
            except:
                print("發送失敗(" + str(i+1) + "/" + str(y) + "):" + email[i])
            # 寄件成功的話
            else:
                print("發送成功(" + str(i+1) + "/" + str(y) + ")")
    # 如果輸入的不是Y或y
    else:
        print("取消寄出")
input("按下Enter結束")