import re
#到每一篇文章底下，得到文章正文的文字內容
def article_text(article_soup):
	import re
	article_context_node = '#main-content'   #文章主體的CSS NODE
	text = str(article_soup.select(article_context_node))   
	text_2 = re.sub('\n','',text)
	text_3 = re.sub('--<span class="f2">.*','',text_2)
	text_4 = re.sub('.*</span></div>','',text_3)
	text_5 = re.sub('<.*>','',text_4)
	return(text_5)

#到每一篇文章下得到推噓文的文字內容，用\n分開
def push_content(article_soup):    
    text = ''
    for push_text in article_soup.select('.push-content'):
        text = text + push_text.text.replace(':','').replace(' ','') +'\n'
    return(text)

#計算推噓數量，會回推、箭頭、噓三個數字	
def push_num(article_soup):   
    push=0
    sh=0
    arrow=0
    for push_tag in article_soup.select('.push-tag'):
        if '推' in push_tag.text:
            push = push+1
        elif '→' in push_tag.text:
            arrow = arrow+1
        elif '噓' in push_tag.text:
            sh = sh+1            
    return(push,arrow,sh)

#得到文章的時間文字內容 例如: Mon Aug 26 23:52:28 2019	
def article_time(article_soup):  
	import re
	text = str(article_soup)
	text_2 = re.sub('\n','',text)
	text_3 = re.sub('.*<span class="article-meta-value">','',text_2)
	text_4 = re.sub('</span></div>.*','',text_3)
	return(text_4)

#計算詞組中文字在文章中的次數，回覆所有詞組X所有文章之表格		
def count_word(all_text,word_list):
	import pandas as pd
	import numpy as np
	result=pd.DataFrame()
	for i in range(len(all_text)):
		count_list=[]
		for single_word in word_list:
			count_list.append(all_text[i].count(single_word,0,len(all_text[i])))
		result = pd.concat([result,pd.Series(count_list,name=str(i+1))],axis=1)
	result.index = word_list
	result = pd.concat([result,pd.Series(np.sum(result,axis=1),name='Total')],axis=1)
	result = result.sort_values('Total',ascending=False)
	return(result)
	