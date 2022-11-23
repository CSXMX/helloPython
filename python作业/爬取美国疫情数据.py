import requests
import json
import csv
def getHTMLText(url):
    try:#实现对美国疫情数据的爬取，并将爬取的结果保存为美国疫情数据.csv
        header = {'User-Agent': 'Mozilla/5.0 '}
        r = requests.get(url,headers = header)
        r.raise_for_status()
        r.encoding = 'utf-8'
        #print(r.text) 
        return r.text
    except: 
        print("出现错误！")
        return ""
#end of getHTMLText(url)
def fillUnivList(html):
    alldata = [['日期','新增确诊人数','确诊人数','治愈人数','死亡人数','死亡率','治愈率']]
    ls = json.loads(html)#将爬取的字符串转换为字典
    data = ls['data']#取到疫情数据
    for i in data:
        a = []
        a.append(i['date'])
        a.append(i['confirm_add'])
        a.append(i['confirm'])
        a.append(i['heal'])
        a.append(i['dead'])
        healnum = int(i['heal'])
        deadnum = int(i['dead'])
        num = healnum+deadnum
        if(num != 0):
            a.append('{:.2%}'.format(deadnum/num))
            a.append('{:.2%}'.format(healnum/num))
        else:
            a.append('0')
            a.append('0')
        alldata.append(a)
    #print(alldata)#数据的列表，构造完毕
    with open('美国疫情数据.csv','w',newline='') as fs:
        writer = csv.writer(fs)
        for row in alldata:
            writer.writerow(row)
#end of fillUnivList(html)
url = "https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country=美国&"
html = getHTMLText(url)
fillUnivList(html)
print('数据爬取成功！')
