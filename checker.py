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
    # print(M)
    # 2. get g1 nodes and edges as dictionary
    g1_labels={}
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
                g1_labels[index]=label
                g1_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g1_edges[v_i].add(v_j)
    # 2. get g2 nodes and edges as dictionary
    g2_labels={}
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
                g2_labels[index]=label
                g2_edges[index]=set()
            elif mode=='edge':
                v_i, v_j=int(parts[0]), int(parts[1])
                g2_edges[v_i].add(v_j)
    return M, g1_labels, g1_edges, g2_labels, g2_edges

def check_label(M, g1_labels, g2_labels):
    for g1_node in M.keys():
        g2_node=M[g1_node]
        if g1_labels[g1_node]!=g2_labels[g2_node]: #if the matched nodes' labels are different
            return False
    return True

def check_children(M, g1_edges, g2_edges): #matched된 것만 확인하는 것으로 바꿔야 함
    for g1_node in M.keys():
        # print('checking children of', g1_node)
        g2_node=M[g1_node]
        if not g1_edges[g1_node].issubset(g2_edges[g2_node]): #if the matched nodes' children set are different
            # print(g1_node, g1_edges, g2_edges)
            return False
    return True

def main():
    M, g1_labels, g1_edges, g2_labels, g2_edges=open_files("input_g1.txt", "input_g2.txt", "output1.txt")
    # print('g1 edges:', g1_edges)
    # print('g2 edges:', g2_edges)
    # print('g1 nodes:', g1_labels)
    # print('g2 nodes:', g2_labels)
    if len(M)!=len(g1_labels):
        print('not a match: match does not cover all nodes of g1')
        return -1
    if not check_label(M, g1_labels, g2_labels):
        print('not a match: label different')
        return -1
    if not check_children(M, g1_edges, g2_edges):
        print('not a match: children different')
        return -1
    print('match!')
    return 0

main()
