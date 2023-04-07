import pandas as pd
import pymysql as sql
import numpy as np
import random

def tmp():
    # 准标识符定义
    quasi_identifier_list = []
    quasi_identifier_DGH_list = []
    quasi_identifier_VGH_list = []
    quasi_identifier_height_list = []
    ##暂且没用
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':

    # 属性标签
    attributeLabels = ["age",  # 0年龄            int64
                       "workclass",  # 1工作类型        object
                       "fnlwgt",  # 2人口特征权重    int64
                       "education",  # 3学历            object
                       "education_num",  # 4受教育时间      int64
                       "marital_status",  # 5婚姻状态        object
                       "occupation",  # 6职业            object
                       "relationship",  # 7关系            object
                       "race",  # 8种族            object
                       "sex",  # 9性别            object
                       "capital_gain",  # 10资本收益        int64
                       "capital_loss",  # 11资本损失        int64
                       "hours_per_week",  # 12每周工作小时数  int64
                       "native_country",  # 13原籍            object
                       "wage_class"]  # 14收入类别        object
    data=pd.read_csv('data/adult.data',header=None,sep=',',names=attributeLabels)
    data_clean = data.replace(regex=[r'\?|\.|\$'], value=np.nan)
    data=data_clean.dropna(how='any')#将所有含有缺失值的行都去掉
    #剔除没有用的列
    data=data.drop(['fnlwgt'],axis=1)
    data.info()
    print(data.shape)
    data.insert(0,'name',None)
    print(data.shape)
    data.info()
    for indexs in data.index:
        # print(data.loc[index])
        data.loc[indexs,"name"]=''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 7))
    print(data[:15])
    # connection=sql.connect(host="localhost"
    #                        ,user="root",password="123456qwb",db="myteast")
    # cur=connection.cursor()
    # print(cur.fetchall())#数据库部分

    print('end')


