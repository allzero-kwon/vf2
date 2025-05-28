from typing import Union

class Node :
    def __init__(self, index, label) -> None:
        #label, parent node, children
        self.index=index
        self.label=label
        self.prev=set()
        self.next=set()
        
    def __repr__(self):
        prev_ids = sorted(n.index for n in self.prev)
        next_ids = sorted(n.index for n in self.next)
        return f'Node(index={self.index}, label=\'{self.label}\', prev=Nodes({prev_ids}), next=Nodes({next_ids}))'

class Graph :
    def __init__(self):
        self.root=Node(0, None)
        self.nodes=0
        
    def insert(self, parent, child) -> None: #insert input child node to input parent node
        parent.next.add(child)
        child.prev.add(parent)
        self.nodes=self.nodes+1

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
        # repr for debugging graph class 
        nodes = []
        edges = []
        visited = set()

        def dfs(node):
            if node.index in visited:
                return
            visited.add(node.index)
            nodes.append(node.index)
            for neighbor in node.next:
                edges.append(f"({node.index}->{neighbor.index})")
                dfs(neighbor)

        dfs(self.root)

        node_list_str = ", ".join(map(str, sorted(nodes)))
        edge_list_str = ", ".join(edges)

        return f"Graph(nodes=Nodes({node_list_str}), edges=Edges({edge_list_str})"
    
def load_graph_from_txt(filepath):
    graph = Graph()
    node_list=[None]
    with open(filepath, 'r') as file:
        mode='init'
        prev_node_id=0
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'): #change mode node/edge
                if line[1]=='n':
                    mode='node'
                elif line[1]=='e':
                    mode='edge'
                    graph.insert(graph.root, node_list[1]) #when changing to edge mode, add node1 to graph.root
                continue
            parts = line.split()
            if mode=='node': #in node mode, add new node to node list
                node_id = int(parts[0])
                label = parts[1]
                if node_id!=prev_node_id+1: #check if node id increases by 1
                    print('error node id at', node_id)
                node_list.append(Node(node_id, label))
                prev_node_id=node_id
            elif mode=='edge': #in edge mode, add new edge to graph
                v_i, v_j = int(parts[0]), int(parts[1])
                graph.insert(node_list[v_i], node_list[v_j])
    return graph
    

if __name__ == "__main__" : 
    g1=load_graph_from_txt("input_g1.txt")
    g2=load_graph_from_txt("input_g2.txt")
    example_index=g1.find(5)
    assert example_index == None
    
    example_index=g1.find(2)
    assert example_index is not None 
    print(f'[TEST] index : {example_index.index} | label : {example_index.label}')