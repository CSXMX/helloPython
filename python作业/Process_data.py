import numpy as np
import matplotlib.pyplot as plt
import csv
#设置字体为黑体
plt.rcParams['font.sans-serif']=['Simhei']
#解决坐标轴符号'-'显示为方块
plt.rcParams['axes.unicode_minus']= False
with open("美国疫情数据.csv","r") as fIn:
    reader = csv.reader(fIn)#创建阅读器
    data = list(reader)#存储csv数据
    date = [row[0] for row in data]#日期
    confirm_add = [row[1] for row in data]#新增病例
    confirm = [row[2] for row in data]#确诊人数
    heal = [row[3] for row in data]#治愈人数
    dead = [row[4] for row in data]#死亡人数
#第一步，我们开始制作一个新的.csv文件，统计每个月的疫情数据[3月-11月]
with open("处理后的疫情数据.csv","w",newline='') as fOut:
    myconfirm = []#每个月底的确诊人数
    myheal = []#治愈人数
    mydead = []#死亡人数
    Rate_Increase = []#增长率
    for i in range(len(date)):
        if(date[i] == '02.29'):
            myconfirm.append(int(confirm[i]))#选择2月最后一天为初始值
            myheal.append(int(heal[i]))
            mydead.append(int(dead[i]))
            break
    for j in range(i+1,len(date)-1):#只统计月底数据
        if(int(date[j+1][0:2]) in range(3,13) and int(date[j+1][3:])== 1):
            num =  '{:.2%}'.format((float(confirm[j])-float(myconfirm[-1])) /float(myconfirm[-1])) 
            Rate_Increase.append(num)
            myconfirm.append(int(confirm[j]))
            myheal.append(int(heal[j]))
            mydead.append(int(dead[j]))
    fOut.write('月份,确诊人数,治愈人数,死亡人数,本月增长的确诊人数,确诊人数的增长率\n')
    print(Rate_Increase)
    for row in range(len(myconfirm)):
        if(row == 0):
            fOut.write('2月底,'+str(myconfirm[row])+','+str(myheal[row])+','+str(mydead[row])+',0,0'+'\n')
        else:
            fOut.write(str(row+2)+'月底,'+str(myconfirm[row])+','+str(myheal[row])+','+str(mydead[row])+','+str(myconfirm[row]-myconfirm[row-1])+','+str(Rate_Increase[row-1])+'\n')
#第二步，制作关于美国2月底到11月底的确诊人数的折线图
index = np.arange(0,10)
plt.figure(figsize=(14,6))
plt.xlabel('月份')
plt.ylabel('确诊人数/万人')
plt.ylim(0,1400,400)
plt.title('美国2月底到11月底的确诊人数')
x =['2月底','3月底','4月底','5月底','6月底','7月底','8月底','9月底','10月底','11月底']
plt.xticks(index,x)
myconfirm = [row/1e4 for row in myconfirm]#换个单位
print(myconfirm)
plt.plot(index,myconfirm,"r-*")
plt.legend(['新型冠状病毒确诊人数'],loc ='best')
plt.savefig('确诊人数.png')
plt.show()
print('程序结束！')
