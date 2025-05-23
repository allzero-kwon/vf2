#shallowcoding

from typing import *

class Node :
    def __init__(self, index, label) -> None:
        #label, parent node, children
        self.index=index
        self.label=label
        self.prev=set()
        self.next=set()


class Graph :
    def __init__(self) -> None:
        self.root=Node(None, None)
        
    def insert(self, parent, child): #insert input child node to input parent node
        parent.next.add(child)
        child.prev.add(parent)
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
        return found_node
    
    @property
    def nodes(self):
        # nodes list 반환
        # ex. self.pattern_length = len(self.G2.nodes)
        pass 
    
    

class VF2 : 
    
    def __init__(self) -> None:
        def __init__(self, G1:Graph, G2:Graph):
            self.G1 = G1
            self.G2 = G2 # pattern graph
            self.pattern_length = len(self.G2.nodes) 
            
            self.core1 = {} # Matched G1 -> G2 
            self.core2 = {} # Matched G2 -> G1 
            self.t1_in = {}
            self.t1_out = {}
            self.t2_in = {}
            self.t2_out = {}
            
            # in, out 객체   node id -> depth 저장! 
            #Four vectors, in_1,out_1,in_2,out_2, whose dimen-sions are equal to the number of nodes in the correspond-ing graphs, describing the membership of the terminalsets. In particular, in_1[n] is nonzero if n is either in M1ðsÞor in Tin1ðsÞ; similar definitions hold for the other threevectors. The actual value stored in the vectors is the depthin the SSR tree of the state in which the node entered thecorresponding set
            
            self.result = False # bool (isormorphic or not)
    
        
    @property
    def matched_length(self):
        assert len(list(self.core1.keys())) == len(list(self.core2.keys()))
        return len(list(self.core1.keys()))
    
    def match(self):
        self.match_dfs(1) 
        print(f'Graph is {"isormorphic" if self.result else "non-isormorphic"}')
    
    def match_dfs(self, depth=1):
        if self.matched_length == self.pattern_length:
            self.result = True
            return True
        
        for n1, n2 in self.generate_candidate_pairs():
            if self.check_feasibility(n1, n2):
                self.add_matched_pair(n1, n2, depth)
            if self.match_dfs(depth+1):
                return True 
            # not matched -> rollback
            self.rollback(n1, n2, depth)
            
        return False 
            
    def generate_candidate_pairs(self):
        # construct T1, T2    
        # 1. from T_out (not matched & out)
        T1_out = [n for n in self.G1.nodes if n not in self.core_1 and self.out_1.get(n, 0) > 0]
        T2_out = [n for n in self.G2.nodes if n not in self.core_2 and self.out_2.get(n, 0) > 0]
        
        if T1_out and T2_out:
            for n1 in T1_out:
                for n2 in T2_out:
                    yield n1, n2 # use generator to memory / time optimization (lazy 생성)
            return

        # 2. from T_in (not matched & in)
        T1_in = [n for n in self.G1.nodes if n not in self.core_1 and self.in_1.get(n, 0) > 0]
        T2_in = [n for n in self.G2.nodes if n not in self.core_2 and self.in_2.get(n, 0) > 0]
        if T1_in and T2_in:
            for n1 in T1_in:
                for n2 in T2_in:
                    yield n1, n2
            return
        
        # 3. from all nodes (not matched, disconnected)
        N1 = [n for n in self.G1.nodes if n not in self.core_1]
        N2 = [n for n in self.G2.nodes if n not in self.core_2]
        for n1 in N1:
            for n2 in N2:
                yield n1, n2
    
    def check_feasibility(self, n1, n2) -> bool : 
        pass 
    
    def add_matched_pair(self, n1:Node, n2:Node, depth:int):
        self.core1[n1.id] = n2.id
        self.core2[n2.id] = n1.id
        
        # in,out 업데이트 
        for child in n1.next:
            cid = child.id
            if cid not in self.core_1 and self.out_1.get(cid, 0) == 0:
                self.out_1[cid] = depth
        for prev in n1.prev:
            pid = prev.id
            if pid not in self.core_1 and self.in_1.get(pid, 0) == 0:
                self.in_1[pid] = depth

        for child in n2.next:
            cid = child.id
            if cid not in self.core_2 and self.out_2.get(cid, 0) == 0:
                self.out_2[cid] = depth
                
        for prev in n2.prev:
            pid = prev.id
            if pid not in self.core_2 and self.in_2.get(pid, 0) == 0:
                self.in_2[pid] = depth

    
    def rollback(self, n1, n2, depth):
        # rollback 
        # 1. matched pair에서 삭제 
        del self.core_1[n1.id]
        del self.core_2[n2.id]
        
        # 2. in/out에서 해당 실패한 depth의 item 지우기
        # 여기 한번 실행해봐야함.. del 때문에 runtime error 날수도
        for k,v in list(self.in_1.items()):
            if v == depth : 
                del self.in_1[k]          
   
        for k,v in list(self.out_1.items()):
            if v == depth : 
                del self.out_1[k]     

        for k, v in list(self.in_2.items()):
            if v == depth:
                del self.in_2[k]

        for k, v in list(self.out_2.items()):
            if v == depth:
                del self.out_2[k]
    
    def check_Rpred(self, state) -> bool : 
        pass 

    def check_Rsucc(self, state) -> bool : 
        pass 

    def check_Rin(self, state) -> bool : 
        pass 

    def check_Rout(self, state) -> bool : 
        pass 

    def check_Rnew(self, state) -> bool : 
        pass 

    def check_Sem(self, state) -> bool :
        pass 
        
def main():
    #input to graph
    pass

if __name__ == "__main__":
    pass