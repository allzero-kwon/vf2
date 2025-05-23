class Node :
    def __init__(self, index, label) -> None:
        #label, parent node, children
        self.index=index
        self.label=label
        self.prev=None
        self.next=[]


class Graph :
    def __init__(self) -> None:
        self.root=Node(None, None)
        
    def insert(self, parent, child): #insert input child node to input parent node
        parent.next.append(child)
        child.prev=parent
    def find(self, index):
        current=self.root
        visited=set()
        def dfs(graph, start, visited, index): #find node with certain label using dfs
          if start.index==index:
              print('found node', index)
              return start
          # Mark the current node as visited
          visited.add(start.index)
          print(start.index)  # Process the node (e.g., print it)

          # Recur for all the adjacent vertices
          for neighbor in start.next:
              if neighbor.index not in visited:
                  result=dfs(graph, neighbor, visited, index)
                  if result is not None:
                      return result
        found_node=dfs(self, current, visited, index)
        print(found_node)
        return found_node
    
    @property
    def nodes(self):
        # nodes list 반환
        # ex. self.pattern_length = len(self.G2.nodes)
        pass 
    
  
def main():
    #input to graph
    g=Graph()
    n1=Node(1, 'A')
    n2=Node(2, 'B')
    n3=Node(3, 'C')
    n4=Node(4, 'D')
    g.insert(g.root, n1)
    g.insert(n1, n2)
    g.insert(n1, n3)
    g.insert(n2, n4)
    index_4=g.find(4)
    print(index_4.index, index_4. label)
main()