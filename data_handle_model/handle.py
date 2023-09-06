import csv
import yaml
import uuid
import pandas as pd
from data_handle_model import neo4j
import subprocess

#def create_csv(path):

def read_csv(path,out):
    #conn = neo4j.connect2neo4j()
    # date=pd.read_csv(path)
    # for index,row in date.iterrows():
    #     for i in date.
    df = pd.read_csv(path)
    first_column = df.columns[0]
    other_columns = df.columns[1:]
    tuples = []
    for _, row in df.iterrows():
        first_value = row[first_column]
        for column in other_columns:
            other_value = row[column]
            tuples.append((first_value,f"{column}", other_value))
    result_df = pd.DataFrame(tuples, columns=['uuid', 'link','value'])
    result_df.to_csv(out, index=False,encoding='UTF-8')

    # with open(path,"r") as file:
    #     l=readline_count(file)
    #     reader=csv.reader(file)
    #     labels=next(reader)
    #     print(labels)
    #     for row in reader:
    #         uid=str(uuid.uuid4())
    #         #nodeA = conn.creat_node("uuid", uid)
    #         #print(row)
    #         for i in range(len(row)):
    #             #print(attribute_name,row[i])
    #             attribute_name=f"UA_{labels[i]}"
    #             #print(attribute_name,row[i])
    #             nodeB=conn.creat_node("attribute",row[i])
    #             conn.creat_relationship(nodeA,nodeB,attribute_name)
    # file.close()
def readline_count(file_name):
    return len(open(file_name).readlines())
#def read_json(path):

if __name__=='__main__':
    path='../data/csv/adult_with_pii.csv'
    out='../data/output/csv_out.csv'
    read_csv(path,out)
    print("hello world")
    # with open("datebase.yaml","r") as file:
    #     config=yaml.safe_load(file)
    # username=config['datebase']['username']
    # password=config['datebase']['password']
    # nodes=config['filepath']['node_csv']
    # rela=config['filepath']['rela_csv']
    # commend=f"neo4j - admin import --database ={username} --nodes = {nodes} --relationships ={rela}"
    # print(commend)
    # subprocess.run(commend)