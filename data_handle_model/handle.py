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
    other_columns = df.columns[0:]
    u_node = []
    A_node=[]
    A_U_link=[]
    uuid_column = [str(uuid.uuid4()) for _ in range(df.shape[0])]
    node_id=0
    for l, row in df.iterrows():
        u_node.append((uuid_column[l], "user"))
        for column in other_columns:
            other_value = row[column]
            A_node.append((node_id,other_value,f"{column}"))
            A_U_link.append((uuid_column[l],node_id,f"{column}"))
            node_id=node_id+1
    unode=pd.DataFrame(u_node,columns=['uuid:ID',':LABEL'])
    anode=pd.DataFrame(A_node,columns=['node_id:ID','value',':LABEL'])
    A_U=pd.DataFrame(A_U_link,columns=[':START_ID',':END_ID',':TYPE'])
    out1=out+"u_nodes.csv"
    out2=out+"a_nodes.csv"
    out3=out+"au_relationship.csv"
    unode.to_csv(out1, index=False,encoding='UTF-8')
    anode.to_csv(out2, index=False,encoding='UTF-8')
    A_U.to_csv(out3, index=False,encoding='UTF-8')
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
    out='../data/output/'
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