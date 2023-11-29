from flask import jsonify
from neo4j import GraphDatabase
import configparser
from py2neo import Graph
from py2neo.bulk import create_nodes,create_relationships,merge_nodes,merge_relationships
import json
import pandas as pd
import time
def load_json_file1(file_path):
    #hotel
    #todo 感觉还是得配置文件读取 先todo吧
    query_f=f"""
    CALL apoc.load.json('{file_path}') YIELD value AS v
    """
    query_s = """
    CREATE (a:UUID {value: v.uuid})
    MERGE (s:Sex {value: v.sex})
    MERGE (i:Id_num {value: v.id_number})
    MERGE (p:Phone {value: v.phone})
    MERGE (h:Hotel {name: v.hotel_name})
    
    MERGE (a)-[:has_sex]->(s)
    MERGE (a)-[:has_id]->(i)
    MERGE (a)-[:has_phone]->(p)
    MERGE (a)-[:visit {start:v.day_start,end:v.day_end}]->(h)
    """
    query=query_f+query_s
    config = configparser.ConfigParser()
    # 只供测试
    config.read('../setting/set.config')
    url = config.get('neo4j', 'url')
    driver = GraphDatabase.driver(url, auth=(config.get('neo4j', 'user'), config.get('neo4j', 'password')))
    with driver.session() as session:
        result = session.run(query)
    return result



def load_json_file1p(file):
    #hotel
    config = configparser.ConfigParser()
    # 只供测试
    config.read('../setting/set.config')
    url = config.get('neo4j', 'url')
    graph = Graph(url, auth=(config.get('neo4j', 'user'), config.get('neo4j', 'password')))
    with open(file, 'r', encoding='UTF-8') as f:
        data = pd.read_json(f)

    for i in data.columns:
        print(i)
    node_u = [
        {"uuid": uuid} for uuid in data['uuid'].tolist()
    ]
    node = [[uuid] for uuid in data['uuid'].tolist()]
    print(node)
    lable_u = "uuid"
    keys = ('uuid', 'uuid')
    key = ['uuid']
    merge_nodes(graph.auto(), node, labels={lable_u}, merge_key=keys, keys=key)
    # create_nodes(graph.auto(),node_u,labels={lable_u})
    print("end")

def load_json_file2(file):
    #info
    # todo 感觉还是得配置文件读取 先todo吧
    query_f = f"""
        CALL apoc.load.json('{file}') YIELD value AS v
        """
    query_s = """
        create (a:UUID {value: v.uuid})
        MERGE (n:Person {name: v.name})
        MERGE (s:Sex {value: v.sex})
        MERGE (b:Birthday {value: v.birthday})
        MERGE (g:Age {value: v.age})
        MERGE (m:Marital_status {value: v.marital_status})
        MERGE (e:Email {value: v.email})
        MERGE (u:Bank_num {value: v.bank_number})
        MERGE (r:Address {value: v.address})
        MERGE (i:Id_num {value: v.id_number})
        MERGE (p:Phone {value: v.phone})

        MERGE (a)-[:has_sex]->(s)
        MERGE (a)-[:has_name]->(n)
        MERGE (a)-[:has_bir]->(b)
        MERGE (a)-[:has_age]->(g)
        MERGE (a)-[:has_mar]->(m)
        MERGE (a)-[:has_email]->(e)
        MERGE (a)-[:has_bank]->(u)
        MERGE (a)-[:has_addr]->(r)
        MERGE (a)-[:has_id]->(i)
        MERGE (a)-[:has_phone]->(p)
        """
    query = query_f + query_s
    config = configparser.ConfigParser()
    # 只供测试
    config.read('../setting/set.config')
    url = config.get('neo4j', 'url')
    driver = GraphDatabase.driver(url, auth=(config.get('neo4j', 'user'), config.get('neo4j', 'password')))
    with driver.session() as session:
        result = session.run(query)
    print(result)


if __name__=='__main__':
    #file='file:///hotel_low.json'
    #file='../data/json/hotel_low.json'
    file='file:///info_low.json'
    time_s=time.time()
    load_json_file2(file)
    time_e=time.time()
    total_time = time_s-time_e
    print('程序运行时间为：', total_time, '秒')




