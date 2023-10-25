from neo4j import GraphDatabase

url = "bolt://192.168.1.121:7474"
driver = GraphDatabase.driver(url, auth=("neo4j", "123456"))

def load_json_file(tx, file_path):
    query = """
    CALL apoc.load.json($file_path) YIELD value
    MERGE (n:Node {id: value.id})
    SET n += value.properties
    """
    tx.run(query, file_path=file_path)





if __name__=='__main__':
    with driver.session() as session:
        session.write_transaction(load_json_file, "")
