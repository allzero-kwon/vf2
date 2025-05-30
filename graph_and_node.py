from typing import Union

class Node :
    def __init__(self, index, label) -> None:
        #label, parent node, children
        self.index=index
        self.label=label
        self.prev=set()
        self.next=set()
        
    def __repr__(self):
        return f'Node({self.index}, \'{self.label or ""}\')'

class Graph :
    def __init__(self):
        self.root=Node('root', None)
        self.n_nodes=0
        
    def insert(self, parent, child) -> None: #insert input child node to input parent node
        parent.next.add(child)
        child.prev.add(parent)
        self.n_nodes=self.n_nodes+1
    def remove_from_root(self, node):
        node.prev.remove(self.root)
        self.root.next.remove(node)

    def find(self, index) -> Union[None, Node]: #don't need this function. for checking Graph object. does not work for disconnected graph
        current=self.root
        visited=set()
        def dfs(graph, start, visited, index): #find node with certain label using dfs
          if start.index==index:
              print('found node', index)
              return start
          # Mark the current node as visited
          visited.add(start.index)
          print('at node', start.index)  # Process the node (e.g., print it)
            
          # Recur for all the adjacent vertices
          for neighbor in start.next:
              if neighbor.index not in visited:
                  result=dfs(graph, neighbor, visited, index)
                  if result is not None:
                      return result
        found_node=dfs(self, current, visited, index)
        return found_node
    
    def __repr__(self):
        nodes = []
        edges = []
        visited = set()

        def dfs(node):
            if node.index in visited:
                return
            visited.add(node.index)
            nodes.append(node.index)
            for neighbor in node.next:
                if node.index != 'root':
                    edges.append(f"({node.index}->{neighbor.index})")
                dfs(neighbor) 

        # 모든 노드에서 시작 → disconnected 포함
        all_nodes = set()

        def collect_all_nodes(n):
            if n in all_nodes:
                return
            all_nodes.add(n)
            for nb in n.next | n.prev:
                collect_all_nodes(nb)

        collect_all_nodes(self.root)

        for node in all_nodes:
            dfs(node)

        nodes = sorted([n for n in nodes if n != 'root'])
        node_list_str = ", ".join(map(str, nodes))
        edge_list_str = ", ".join(edges)

        return f"Graph(nodes=Nodes({node_list_str}), edges=Edges({edge_list_str}))"
    
def load_graph_from_txt(filepath):
    graph = Graph()
    node_list={}
    disconnected_heads=set()
    with open(filepath, 'r') as file:
        mode='init'
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'): #change mode node/edge
                if line[1]=='n':
                    mode='node'
                elif line[1]=='e':
                    mode='edge'
                    # @TODO: disconnected graph 일 때는? 
                    # first_node = list(node_list.values())[0] #밑에 new_node 다 insert하는 걸로 바꿔서 삭제합니다
                    # graph.insert(graph.root, first_node) #when changing to edge mode, add node1 to graph.root
                continue
            parts = line.split()
            if mode=='node': #in node mode, add new node to node list
                node_id = parts[0]
                label = parts[1]
                if node_id in node_list: 
                    raise ValueError(f'{node_id} has already inserted. Node ids of input should be different.')
                new_node=Node(node_id, label)
                node_list[node_id] = new_node
                disconnected_heads.add(node_id) #add node id to disconnected nodes list
                graph.insert(graph.root, new_node) #add node to root node of graph(delete when connected to another node)
            elif mode=='edge': #in edge mode, add new edge to graph
                v_i, v_j = parts[0], parts[1] #v_i->v_j
                graph.insert(node_list[v_i], node_list[v_j])
                if v_j in disconnected_heads:
                    disconnected_heads.remove(v_j) #add node id to disconnected nodes list
                    graph.remove_from_root(node_list[v_j]) #add node to root node of graph(delete when connected to another node)
    return graph
    

if __name__ == "__main__" : 
    g1=load_graph_from_txt("input_g1.txt")
    g2=load_graph_from_txt("input_g2.txt")
    example_index=g1.find('5')
    assert example_index == None
    
    example_index=g1.find('1')
    assert example_index is not None 
    print(f'[TEST] index : {example_index.index} | label : {example_index.label}')
    # n1=Node(1, 'A')
    # n2=Node(2, 'B')
    # n3=Node(3, 'C')
    # n4=Node(4, 'D')
    # n5=Node(5, 'E')
    # n6=Node(6, 'F')
    # g1=Graph()
    # g1.insert(g1.root, n1)
    # g1.insert(n1, n2)
    # g1.insert(n1, n3)
    # g1.insert(n1, n4)
    # g1.insert(g1.root, n2)
    # print(g1.root.next)
    # g1.remove_from_root(n2)
    # print(g1.root.next)