from py2neo import Graph, Node, Relationship
from py2neo import NodeMatcher, RelationshipMatcher, NodeMatch


class connect2neo4j():
    def __init__(self):
        self.username = "neo4j"
        self.password = "M5s762xGmsfJcgQ"
        self.neo4jUrl = 'http://127.0.0.1:7474'
        self.conn = Graph(self.neo4jUrl, auth=(self.username, self.password))

    def creat_node(self, labels, properties):
        insertNode = Node(labels, name=properties)
        self.conn.create(insertNode)
        return insertNode

    def creat_relationship(self, NodeA, NodeB, properties):
        insertrelationship = Relationship(NodeA, properties, NodeB)
        self.conn.create(insertrelationship)

    def search_node(self, labels, limit=None):
        if limit:
            d = NodeMatch(self.conn, labels=frozenset({'{}'.format(labels)})).limit(limit)
        else:
            node_matcher = NodeMatcher(self.conn)
            d = node_matcher.match(labels)
        return d

    # 按关系名字查询
    def search_relationship(self, nodes=None, r_type=None, limit=None):
        relation = RelationshipMatcher(self.conn)
        d = relation.match(nodes=nodes, r_type='{}'.format(r_type)).limit(limit)
        return d
    def clear(self):
        print("Warning! You will delete all node")
        self.conn.delete_all()

def print_hi(name):
    print(f'Hi,{name}')


if __name__ == '__main__':
    connect = connect2neo4j()
    # node1 = connect.creat_node("user", "qwb")
    # node2 = connect.creat_node("user", "www")
    # connect.creat_relationship(node1, node2, "friend")
    # date = connect.search_node("user",limit=25)
    # dats=connect.search_relationship(r_type="friend",limit=24)
    # for i in date:
    #     connect.conn.delete(i)
    connect.clear()
    print_hi('pycharm')
