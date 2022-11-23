import csv
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
#设置字体为黑体
plt.rcParams['font.sans-serif']=['Simhei']
#解决坐标轴符号'-'显示为方块
plt.rcParams['axes.unicode_minus']= False
#选择部分疫情数据，用作机器学习的训练集和测试集
with open("美国疫情数据.csv","r") as fIn:
    reader = csv.reader(fIn)#创建阅读器
    data = list(reader)#存储csv数据
    date = [row[0] for row in data[40:]]#日期
    confirm_add = [int(row[1]) for row in data[40:]]#新增病例
    confirm = [int(row[2]) for row in data[40:]]#确诊人数
    heal = [int(row[3]) for row in data[40:]]#治愈人数
    dead = [int(row[4]) for row in data[40:]]#死亡人数
    Rate_Dead = [float(row[5].strip('%'))/100 for row in data[40:]]#死亡率
    Rate_Heal = [float(row[6].strip('%'))/100  for row in data[40:]]#治愈率
X = []#（确诊人数、新增确诊人数、治愈人数）->预测死亡人数
for i in range(len(confirm)):
    a = []
    a.append(confirm_add[i])
    a.append(confirm[i])
    a.append(heal[i])
    X.append(a)
x_train, x_test, y_train, y_test = train_test_split(X, dead, test_size=0.25)
#特征工程(对特征值进行标准化处理)
std = StandardScaler()
x_train = std.fit_transform(x_train)
x_test = std.transform(x_test)
#f = linear_model.LinearRegression() #线性回归
#f = tree.DecisionTreeRegressor()#决策树回归
f = neighbors.KNeighborsRegressor()#KNN回归
'''
f.fit(x_train,y_train)
y_predict = f.predict(x_test) # 获取预测结果
for i in range(len(y_predict)):
    print("第%d次测试:真实值:%s    预测值:%d"%((i+1),y_test[i],int(y_predict[i])))
'''
def draw(self):#绘制死亡人数预测图
    self.fit(x_train,y_train)
    result =self.predict(x_test)
    index = np.arange(len(result))
    plt.figure(figsize=(15,5))
    plt.ylim(0,350000,30000)
    plt.plot(index,y_test,'go-')
    plt.plot(index,result,'ro-')
    plt.legend(['死亡人数-真实值','死亡人数-预测值'],loc ='best')
    plt.title("准确率："+str(self.score(x_test, y_test)))
    plt.savefig('死亡人数预测图（KNN算法）.jpg')
    plt.show()
def draw_2():#绘制死亡率和治愈率折线图.png
    index = np.arange(0,len(Rate_Dead))
    plt.figure(figsize=(15,5))
    plt.ylim(0,1,0.05)
    plt.plot(index,Rate_Dead,'ko-')
    plt.plot(index,Rate_Heal,'r*-')
    plt.legend(['死亡率','治愈率'],loc ='best')
    plt.savefig('死亡率和治愈率折线图.png')
    plt.show()
def draw_3():#绘制确诊人数增长率与死亡率的散点图.png
    for i in range(len(confirm)):
        confirm_add[i] = confirm_add[i] / (confirm[i]-confirm_add[i])#转化为确诊人数增长率
    plt.figure(figsize=(15,5))
    plt.xlabel('确诊人数增长率')
    plt.ylabel('死亡率')
    plt.scatter(confirm_add,Rate_Dead,c='red',marker='o',s = 100)
    plt.title('确诊人数增长率与死亡率的散点图\n相关系数:'+str(stats.pearsonr(confirm_add,Rate_Dead)))
    plt.savefig('确诊人数增长率与死亡率的散点图.png')
    plt.show()
#draw()
#draw_2()
draw_3()
print('运行结束')
