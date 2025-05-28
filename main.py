from typing import *
from graph_and_node import Graph, Node, load_graph_from_txt

class VF2State:
    def __init__(self, G1: Graph, G2: Graph):
        self.G1 = G1
        self.G2 = G2
        self.core_1 = {}  # G1 → G2
        self.core_2 = {}  # G2 → G1
        self.nodes_G1 = self._collect_nodes(G1.root)
        self.nodes_G2 = self._collect_nodes(G2.root)

        self.in_1 = set()
        self.out_1 = set()
        self.in_2 = set()
        self.out_2 = set()

    def __repr__(self):
        core = ', '.join(f'{n.index}->{m.index}' for n, m in self.core_1.items())
        return f'VF2State(core: {{{core}}})'

    def _collect_nodes(self, root):
        visited, result = set(), []
        def dfs(node):
            if node.index in visited: return
            visited.add(node.index)
            result.append(node)
            for nb in node.next:
                dfs(nb)
        dfs(root)
        return result

    def update_frontiers(self):
        self.in_1 = {n for n in self.nodes_G1 if n not in self.core_1 and any(nb in self.core_1 for nb in n.prev) and n.index != 'root'}
        self.out_1 = {n for n in self.nodes_G1 if n not in self.core_1 and any(nb in self.core_1 for nb in n.next) and n.index != 'root'}
        self.in_2 = {m for m in self.nodes_G2 if m not in self.core_2 and any(nb in self.core_2 for nb in m.prev) and m.index != 'root'}
        self.out_2 = {m for m in self.nodes_G2 if m not in self.core_2 and any(nb in self.core_2 for nb in m.next) and m.index != 'root'}

    def get_candidate_pairs(self):
        self.update_frontiers()
        if self.out_1 and self.out_2:
            print(f'candidates from T_out')
            return self.out_1, self.out_2
        elif self.in_1 and self.in_2:
            print(f'candidates from T_in')
            return self.in_1, self.in_2
        else:
            print(f'candidates from All pairs')
            T1_rest = [n for n in self.nodes_G1 if n not in self.core_1 and n.index != 'root']
            T2_rest = [m for m in self.nodes_G2 if m not in self.core_2 and m.index != 'root']
            return T1_rest, T2_rest

    def check_semantic(self, n, m):
        return n.label == m.label

    def is_feasible(self, n, m):
        if n in self.core_1 or m in self.core_2:
            return False
        
        # R_pred
        for n_pred in n.prev:
            if n_pred in self.core_1:
                if self.core_1[n_pred] not in m.prev:
                    print('R_pred out')
                    return False

        # R_succ
        for n_succ in n.next:
            if n_succ in self.core_1:
                if self.core_1[n_succ] not in m.next:
                    print('R_succ out')
                    return False

        # R_in
        in_n = sum(1 for u in n.prev if u not in self.core_1 and u in self.in_1)
        in_m = sum(1 for v in m.prev if v not in self.core_2 and v in self.in_2)
        if in_n > in_m:
            print('R_in out')
            return False

        # R_out
        out_n = sum(1 for u in n.next if u not in self.core_1 and u in self.out_1)
        out_m = sum(1 for v in m.next if v not in self.core_2 and v in self.out_2)
        if out_n > out_m:
            print('R_out out')
            return False

        # R_new
        new_n = sum(1 for u in n.prev | n.next if u not in self.core_1 and u not in self.in_1 and u not in self.out_1)
        new_m = sum(1 for v in m.prev | m.next if v not in self.core_2 and v not in self.in_2 and v not in self.out_2)
        if new_n > new_m:
            print('R_new out')
            return False

        if not self.check_semantic(n, m):
            print(f'Label out')
            return False

        return True

    def add_pair(self, n, m):
        self.core_1[n] = m
        self.core_2[m] = n

    def remove_pair(self, n, m):
        del self.core_1[n]
        del self.core_2[m]
        
def match(G1: Graph, G2: Graph):
    results = []

    def recursive_match(state: VF2State):
        if results:
            return True

        if len(state.core_1) == len(state.nodes_G1):
            results.append(dict(state.core_1))
            return True

        S1, S2 = state.get_candidate_pairs()

        for n in S1:
            for m in S2:
                print(f'candidate pair: {n.index}, {m.index}')
                if state.is_feasible(n, m):
                    state.add_pair(n, m)
                    if recursive_match(state):
                        return True
                    print(f'Rollback: {n.index}, {m.index}')
                    state.remove_pair(n, m)

        return False

    state = VF2State(G1, G2)
    recursive_match(state)
    return results
 
         
if __name__ == "__main__":
    print('------TC1--------')
    g1=load_graph_from_txt("input_g1.txt")
    g2=load_graph_from_txt("input_g2.txt")
    print(f'Graph G1 : {g1}')
    print(f'Graph G2 : {g2}')
    vf2 = match(g1, g2)
    print('matched : ',vf2)
    
    print('------TC2--------')
    g1=load_graph_from_txt("input_g1_negative.txt")
    g2=load_graph_from_txt("input_g2_negative.txt")
    print(f'Graph G1 : {g1}')
    print(f'Graph G2 : {g2}')
    vf2 = match(g1, g2)
    print('matched : ',vf2)
    
    
    
    print('------TC3 (R_pred)--------')
    g1=load_graph_from_txt("test_inputs/g1_R_pred_negative.txt")
    g2=load_graph_from_txt("test_inputs/g2_R_pred_negative.txt")
    print(f'Graph G1 : {g1}')
    print(f'Graph G2 : {g2}')
    vf2 = match(g1, g2)
    print('matched : ',vf2)
    
    print('------TC4 (R_succ)--------')
    g1=load_graph_from_txt("test_inputs/g1_R_succ_negative.txt")
    g2=load_graph_from_txt("test_inputs/g2_R_succ_negative.txt")
    print(f'Graph G1 : {g1}')
    print(f'Graph G2 : {g2}')
    vf2 = match(g1, g2)
    print('matched : ',vf2)
    
    # print('------TC4 (R_in)--------')
    # g1=load_graph_from_txt("test_inputs/g1_R_in_negative.txt")
    # g2=load_graph_from_txt("test_inputs/g2_R_in_negative.txt")
    # print(f'Graph G1 : {g1}')
    # print(f'Graph G2 : {g2}')
    # vf2 = match(g1, g2)
    # print('matched : ',vf2)
    
    # print('------TC5 (R_out)--------')
    # g1=load_graph_from_txt("test_inputs/g1_R_out_negative.txt")
    # g2=load_graph_from_txt("test_inputs/g2_R_out_negative.txt")
    # print(f'Graph G1 : {g1}')
    # print(f'Graph G2 : {g2}')
    # vf2 = match(g1, g2)
    # print('matched : ',vf2)
    
    # print('------TC6 (R_new)--------')
    # g1=load_graph_from_txt("test_inputs/g1_R_new_negative.txt")
    # g2=load_graph_from_txt("test_inputs/g2_R_new_negative.txt")
    # print(f'Graph G1 : {g1}')
    # print(f'Graph G2 : {g2}')
    # vf2 = match(g1, g2)
    # print('matched : ',vf2)