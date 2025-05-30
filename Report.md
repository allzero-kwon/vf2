# VF2 : A (Sub)Graph Isomorphism Algorithm for Matching Large Graphs

## 1. 환경 및 실행방법
- python >= 3.10
### VF2 Matching 
  + `./run.sh <pattern graph> <target graph> <output file>`
  + ex) `./run.sh tests/input_g1.txt tests/input_g2.txt output1.txt`

### Checker
  + `./run_checker.sh <pattern graph> <target graph> <output file>`



## 2. Input/Output Format 
### Input Format
Input graph 는 Directed Graph 이며, 아래와 같이 nodes와 edges로 나누어져 있는 text 파일 형태입니다.

1.	#nodes : 각 노드의 고유 ID (int)와 **라벨(label)**을 정의합니다.
- `<Node ID> <Node Label>`
2.	#edges : 노드 간의 **edge**을 정의합니다.
- `<출발 Node ID> <도착 Node ID>`

```
#nodes
1 A
2 B
3 C

#edges
1 2
2 3
```

### Output Format
- 첫번째 line : Isomorphic 여부를 나타내는 값 (True, False)
- 이 후 : Matched Node ID Pairs

```
True
1 2
2 1
3 3
```



## 3. Testcase 및 동작 설명