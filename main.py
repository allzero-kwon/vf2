from typing import *
from graph_and_node import Graph, Node, load_graph_from_txt
from checker import main as checker

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
            if node in visited: return
            visited.add(node)
            if node.index != 'root':
                result.append(node)
            for nb in node.next | node.prev:
                dfs(nb)
        dfs(root)
        return result

    def update_frontiers(self):
        """ T in/out update 
            T out : the sets of nodes, not yet in the partial mapping, that are the destination of branches starting from G1, G2
            T_in : the sets of nodes, not yet in the partial mapping,  that are the origin of branches ending into G1,G2
        """
        self.in_1 = {n for n in self.nodes_G1 if n not in self.core_1 and any(nb in self.core_1 for nb in n.prev) and n.index != 'root'}
        self.out_1 = {n for n in self.nodes_G1 if n not in self.core_1 and any(nb in self.core_1 for nb in n.next) and n.index != 'root'}
        self.in_2 = {m for m in self.nodes_G2 if m not in self.core_2 and any(nb in self.core_2 for nb in m.prev) and m.index != 'root'}
        self.out_2 = {m for m in self.nodes_G2 if m not in self.core_2 and any(nb in self.core_2 for nb in m.next) and m.index != 'root'}

    def get_candidate_pairs(self):
        """Get Candidate pairs 
        - If T_out 1,2 are empty, then consider T_in. 
        - If T_out, in are empty (Disconnected Graph or Init graph), use all the pairs of nodes not contained neither in G1, G2.

        Returns:
            pairs (List[tuple]): list of pairs (Node from G1, Node from G2)
        """
        self.update_frontiers()
        if self.out_1 and self.out_2:
            return [(n, m) for n in self.out_1 for m in self.out_2]
        elif self.in_1 and self.in_2:
            return [(n, m) for n in self.in_1 for m in self.in_2]
        else:
            T1_rest = [n for n in self.nodes_G1 if n not in self.core_1 and n.index != 'root']
            T2_rest = [m for m in self.nodes_G2 if m not in self.core_2 and m.index != 'root']
            return [(n, m) for n in T1_rest for m in T2_rest]

    def check_semantic(self, n, m):
        return n.label == m.label

    def is_feasible(self, n, m):
        if n in self.core_1 or m in self.core_2:
            return False
        
        # R_pred : All matched predecessors of n must match predecessors of m
        for n_pred in n.prev:
            if n_pred in self.core_1:
                if self.core_1[n_pred] not in m.prev:
                    print(f'R_pred check failed')
                    return False

        # R_succ : All matched successors of n must match successors of m
        for n_succ in n.next:
            if n_succ in self.core_1:
                if self.core_1[n_succ] not in m.next:
                    print(f'R_succ check failed')
                    return False

        # R_in : Number of in-frontier neighbors must not exceed in G2
        in_n = sum(1 for u in n.prev if u not in self.core_1 and u in self.in_1)
        in_m = sum(1 for v in m.prev if v not in self.core_2 and v in self.in_2)
        if in_n > in_m:
            print(f'R_in check failed {in_n} > {in_m}')
            return False

        # R_out : Number of out-frontier neighbors must not exceed in G2
        out_n = sum(1 for u in n.next if u not in self.core_1 and u in self.out_1)
        out_m = sum(1 for v in m.next if v not in self.core_2 and v in self.out_2)
        if out_n > out_m:
            print(f'R_out check failed {out_n} > {out_m}')
            return False

        # R_new : Remaining unmapped neighbors must structurally match between n and m
        new_n = sum(1 for u in n.prev | n.next if u not in self.core_1 and u not in self.in_1 and u not in self.out_1)
        new_m = sum(1 for v in m.prev | m.next if v not in self.core_2 and v not in self.in_2 and v not in self.out_2)
        if new_n > new_m:
            print(f'R_new check failed {new_n} > {new_m}')
            return False

        if not self.check_semantic(n, m):
            print(f'Label (Semantic Attribute) check failed')
            return False

        return True

    def add_pair(self, n, m):
        self.core_1[n] = m
        self.core_2[m] = n

    def remove_pair(self, n, m):
        del self.core_1[n]
        del self.core_2[m]
        
def match(G1: Graph, G2: Graph):
    """VF2 Match function
    

    Args:
        G1 (Graph): g1 graph = pattern graph
        G2 (Graph): g2 graph = target graph

    Returns:
        matching dict {g1 node : g2 node}
    """
    # results = []

    def recursive_match(state: VF2State):
        if len(state.core_1) == len(state.nodes_G1):
            return list(state.core_1.items())

        for n, m in state.get_candidate_pairs():
            print(f'Candidate pair: {n.index}, {m.index}')
            if state.is_feasible(n, m):
                state.add_pair(n, m)
                results = recursive_match(state)
                if results : 
                    return results
                print(f'Rollback: {n.index}, {m.index}')
                state.remove_pair(n, m)

        return []

    state = VF2State(G1, G2)
    results = recursive_match(state)
    return results
 
 
def main(input_g1_path, input_g2_path, output_path):
    """main function for VF2 

    Args:
        input_g1 (str): pattern graph file path
        input_g2 (str): target graph file path
        output (str): output file path 
    """
    g1=load_graph_from_txt(input_g1_path)
    g2=load_graph_from_txt(input_g2_path)
    import pdb 
    pdb.set_trace()
    print(g1)
    print(g2)
    # validate input
    if g1.n_nodes > g2.n_nodes : 
        print(
            f"Pattern graph (g1) has more nodes ({g1.n_nodes}) than target graph (g2) ({g2.n_nodes}). Subgraph isomorphism is not possible. Isomorphism result is False"
        )
        vf2 = []
    else : 
        vf2 = match(g1, g2)
   
    print(vf2)
    with open(output_path, 'w') as f :
        f.write(f'{"True" if len(vf2) > 0 else "False"}')
        for g1, g2 in vf2:
            f.write(f'\n{g1.index} {g2.index}')

         
if __name__ == "__main__":
    import argparse
    import sys 
    import io
    parser = argparse.ArgumentParser()
    parser.add_argument('g1', type=str, help='g1 input txt file')
    parser.add_argument('g2', type=str, help='g2 input txt file')
    parser.add_argument('output', type=str, help='output txt file')
    parser.add_argument('--debug', action='store_true', help='Debugging Mode')
    parser.add_argument('--checker', action='store_true', help='Check output')
    args = parser.parse_args()
    
    if not args.debug : 
        sys.stdout = io.StringIO()
    
    g1_input = args.g1
    g2_input = args.g2
    output = args.output
    main(g1_input, g2_input, output)
    
    if args.checker : 
        checker(g1_input, g2_input, output)