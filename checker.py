def open_files(g1_filepath, g2_filepath, output):
    # 1. get result match as dictionary
    M={} #define match with dictionary. if node 1 in g1 corresponds to node3 in g2, M[1]=3
    with open(output, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split()
            g1_node=int(parts[0])
            g2_node=int(parts[1])
            M[g1_node]=g2_node
    print(M)
    # 2. get g1 nodes and edges as dictionary
    g1_nodes={}
    g1_edges={}
    with open(g1_filepath, 'r') as file:
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
                continue
            parts = line.split()
            if mode=='node':
                index, label=int(parts[0]), parts[1]
                g1_nodes[index]=label
                g1_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g1_edges[v_i].add(v_j)
    # 2. get g2 nodes and edges as dictionary
    g2_nodes={}
    g2_edges={}
    with open(g2_filepath, 'r') as file:
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
                continue
            parts = line.split()
            if mode=='node':
                index, label=int(parts[0]), parts[1]
                g2_nodes[index]=label
                g2_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g2_edges[v_i].add(v_j)
    return M, g1_nodes, g1_edges, g2_nodes, g2_edges

def check_label(M, g1_nodes, g2_nodes):
    for node_idx in M.keys():
        if g1_nodes[node_idx]!=g2_nodes[node_idx]: #if the matched nodes' labels are different
            return False
    return True

def check_children(M, g1_edges, g2_edges):
    for node_idx in M.keys():
        if g1_edges[node_idx]!=g2_edges[node_idx]: #if the matched nodes' children set are different
            print(node_idx, g1_edges, g2_edges)
            return False
    return True

def main():
    M, g1_nodes, g1_edges, g2_nodes, g2_edges=open_files("input_g1.txt", "input_g2.txt", "output1.txt")
    if len(M)!=len(g1_nodes):
        print('not a match: match does not cover all nodes of g1')
        return -1
    if not check_label(M, g1_nodes, g2_nodes):
        print('not a match: label different')
        return -1
    if not check_children(M, g1_nodes, g2_nodes):
        print('not a match: children different')
        return -1
    print('match!')
    return 0

main()