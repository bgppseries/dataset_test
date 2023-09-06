import pandas as pd
import pymysql as sql
import numpy as np
import random
# 检验是否满足k匿名
# 将所有准标识符的组合存入字典，值为出现次数。
def group_data(testedSet):
    quasiDict = {}
    for item in testedSet.itertuples():
        # --------------------------------------------------------------
        # 将准标识符转化为字符串
        item_statement = ''
        for label in quasi_identifier_list:
            item_statement = item_statement + str(getattr(item, label)) + ' '
            #print(item_statement)
        # --------------------------------------------------------------
        # 如果该准标识符组合已经出现过了，则计数+1
        if item_statement in quasiDict.keys():
            quasiDict[item_statement] += 1
        # 如果该准标识符组合没有出现过，则新建记录
        else:
            quasiDict[item_statement] = 1
    # 返回字典
    return quasiDict


# 判断数据集testedSet是否满足k匿名，是则返回true，否则返回false
def if_k(testedSet, k):
    # 对数据集进行分组，获得组合数量
    ans_dict = group_data(testedSet)
    # -----------------------------------------------------------------
    # 展示准标识符组合
    print('当前准标识符组合')
    print(ans_dict)
    print('')
    # -----------------------------------------------------------------
    min_k = None
    # 遍历分组字典，取出最小的重复个数，赋值给min_k
    for i in ans_dict:
        if min_k is None or ans_dict[i] < min_k:
            min_k = ans_dict[i];
    # 如果字典的最小k值大于等于给定的k值，则满足k匿名
    if min_k >= k:
        return True
    else:
        return False

#对数据集tempDataSet（dataframe）的属性列attr（String）进行泛化
#vgh（dataframe）是泛化树

def Generalization_attr(tempDataSet, attr, vgh, h):
    for index,row in vgh.iterrows():
        if row.height==h:
            tempDataSet.replace({attr:row.value},vgh.loc[row.parent].value,inplace=True)
            #print('1',row.value,vgh.loc[row.parent].value)

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
# 准标识符定义
quasi_identifier_list = []
#泛化树
quasi_identifier_DGH_list = []
quasi_identifier_VGH_list = []
quasi_identifier_height_list = []

##选择准标识符进行泛化
# marital-status属性标签
marital_attributeLabels = ['***',  # 0抑制标签
                           'Married-h2',  # 1已婚
                           'Alone',  # 2独自一人
                           'Married-h1',  # 3已婚
                           'Single',  # 4单身
                           'Widowhood',  # 5鳏寡
                           'Married-civ-spouse',  # 已婚-公民-配偶
                           'Married-AF-spouse',  # 已婚-无房-配偶
                           'Separated',  # 分居
                           'Divorced',  # 离婚
                           'Never-married',  # 未婚
                           'Widowed',  # 寡居
                           'Married-spouse-absent'  # 已婚-配偶-不在
                           ]
# marital-status的泛化树
vgh_marital = pd.DataFrame({'value': marital_attributeLabels,
                            'parent': [-1, 0, 0, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5],
                            'height': [3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]})

quasi_identifier_list.append(attributeLabels[5])  # 将marital-status设置为准标识符
quasi_identifier_DGH_list.append(3)
quasi_identifier_VGH_list.append(vgh_marital)
quasi_identifier_height_list.append(0)
#test
print(vgh_marital)

# race属性标签
race_attributeLabels = ['***',  # 0抑制标签
                        'White-h1',  # 1白人
                        'Non-White',  # 2非白人
                        'White',  # 3白人
                        'Asian-Pac-Islander',  # 4亚洲-太平洋-伊斯兰人
                        'Amer-Indian-Eskimo',  # 5美洲-印第安人-爱斯基摩人
                        'Other',  # 6其他
                        'Black'  # 7黑人
                        ]
# race的泛化树
vgh_race = pd.DataFrame({'value': race_attributeLabels,
                         'parent': [-1, 0, 0, 1, 2, 2, 2, 2],
                         'height': [2, 1, 1, 0, 0, 0, 0, 0]})

quasi_identifier_list.append(attributeLabels[8])  # 将workclass设置为准标识符
quasi_identifier_DGH_list.append(2)
quasi_identifier_VGH_list.append(vgh_race)
quasi_identifier_height_list.append(0)
#test
print(vgh_race)
# workclass属性标签
workclass_attributeLabels = ['***',  # 0抑制标签
                           'Private-h2',  # 1隐私一级
                           'Non-Private',  # 2非隐私
                           'Private-h1',  # 3隐私二级
                           'government department',  # 4政府部门
                           'Self-employed',  # 5个体户
                           'Private',  # 6隐私三级
                           'Self-emp-not-inc',  # 7
                           'Self-emp-int',  # 8
                           'Federal-gov',  # 9
                           'Local-gov',  # 10
                           'State-gov',  # 11
                           'Without-pay', # 12
                            'Never-worked' #13
                           ]
# workclass的泛化树
vgh_workclass = pd.DataFrame({'value': workclass_attributeLabels,
                            'parent': [-1, 0, 0, 1, 2, 2, 3, 5, 5, 4, 4, 4, 5, 5],
                            'height': [3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]})

quasi_identifier_list.append(attributeLabels[1])  # 将workclass设置为准标识符
quasi_identifier_DGH_list.append(3)
quasi_identifier_VGH_list.append(vgh_workclass)
quasi_identifier_height_list.append(0)
#test
print(vgh_workclass)
# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    data=pd.read_csv('data/csv/adult.data',header=None,sep=',',names=attributeLabels)
    # 将缺失值部分的“ ？” 置为空，即np.NaN，便于使用pandas来处理缺失值
    data_clean = data.replace(regex=[r'\?|\.|\$'], value=np.nan)
    data=data_clean.dropna(how='any')#将所有含有缺失值的行都去掉
    #剔除没有用的列
    data=data.drop(['fnlwgt'],axis=1)
    # 类型为字符串的标签
    attributeLabels_str = ["workclass", "education", "marital_status", "occupation",
                           "relationship", "race", "sex", "native_country", "wage_class"]
    # 删除数据值前的空格
    for label in attributeLabels_str:
        data[label] = data[label].str.strip()

    data.reset_index(drop=True, inplace=True)#重置索引
    data.info()
    print(data.shape)
    #data.reset_index(drop=True, inplace=True)#重置索引
    print(data[:15])
    # k值定义
    k_Anonymity = 18
    #data['workclass'].replace('Self-emp-not-inc','Private-h1',inplace=True)
    # 泛化次数计数，初始化为所有准标识符泛化次数之和
    gen_count = 0
    for index in range(len(quasi_identifier_DGH_list)):
        gen_count += quasi_identifier_DGH_list[index]

    while if_k(data, k_Anonymity) is False:
        for index in range(len(quasi_identifier_list)):
            # 如果已经到达了泛化顶点
            if quasi_identifier_height_list[index] >= quasi_identifier_DGH_list[index]:
                continue
            # -----------------------------------------------------------------
            # 泛化
            Generalization_attr(data,
                                quasi_identifier_list[index],
                                quasi_identifier_VGH_list[index],
                                quasi_identifier_height_list[index])
            #-----------------------------------------------------------------
            # 泛化次数-1
            gen_count -= 1
            # 泛化高度+1
            quasi_identifier_height_list[index] += 1
            if if_k(data, k_Anonymity):
                break
        print('当前泛化高度：')
        for index in range(len(quasi_identifier_list)):
            print(quasi_identifier_list[index] + ':' + str(quasi_identifier_height_list[index]))
        # 直至无法泛化
        if gen_count == 0:
            print('泛化失败')
            break

    print('当前泛化高度：')
    for index in range(len(quasi_identifier_list)):
        print(quasi_identifier_list[index] + ':' + str(quasi_identifier_height_list[index]))

    print('当前k值为：')
    print(k_Anonymity)

    if_k(data,k_Anonymity)
    data.to_csv("data/output/K_15.csv")
    # data.insert(0,'name',None)
    # print(data.shape)
    # data.info()
    # for indexs in data.index:
    #     # print(data.loc[index])
    #     data.loc[indexs,"name"]=''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 7))
    # print(data[:15])

    # connection=sql.connect(host="localhost"
    #                        ,user="root",password="123456qwb",db="myteast")
    # cur=connection.cursor()
    # print(cur.fetchall())#数据库部分
    print('end')
    # print('精确度为：')
    # prec = 0
    # for index in range(len(quasi_identifier_list)):
    #     prec += (quasi_identifier_height_list[index]) / (quasi_identifier_DGH_list[index])
    # prec = 1 - (prec / len(quasi_identifier_list))
    #
    # print(prec)