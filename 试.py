import numpy as np
import time
start=time.time()
# 模型参数
A = np.asarray([[0.9600141, 0.01999295, 0.01999295], [0.01999295, 0.9600141, 0.01999295], [0.01999295, 0.01999295, 0.9600141]]) # 转移矩阵
B = np.asarray([[0.17749698,0.27015644,0.5523466], [0.32282755,0.38856372,0.2886087], [0.22987872,0.37872106,0.39140022]])
Pi = np.asarray([1/3, 1/3, 1/3]).transpose()



O = np.asarray([3, 3, 3, 1, 3, 2, 3, 2, 3, 1, 3, 3, 3, 3, 1, 1, 3, 1, 2, 1, 2, 2, 3, 3, 3, 2, 1, 3, 1, 3, 3, 3, 2, 3, 3, 3, 1, 3, 3, 2, 2, 3, 3, 3, 3, 3, 1, 1, 2, 2, 3, 3, 3, 1, 1, 3, 3, 1, 1, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 3, 1, 2, 1, 3, 2, 3, 3, 1, 3, 2, 1, 1, 3, 1, 1, 3, 1, 1, 3, 3, 3, 1, 3, 3, 3])
O=O-1
#print(O)
T = O.shape[0]
N = A.shape[0]   # 状态数

#print(B[:,O[0]])
p_nodes = Pi * B[:, O[0]]     # 记录每个节点的路径概率
#print(p_nodes)
path_nodes = []           # 记录每个节点的路径
path_tmp=[]
# 初始化路径
for node in range(N):
    path_nodes.append([node])
    path_tmp.append([node])

# T 个时刻
for step in range(1, T):
    for this_node in range(N):# 计算每个节点的新概率
        p_news = []
        for last_node in range(N):
            p_trans = A[last_node, this_node]  # 转移概率
            p_out = B[this_node, O[step]]       # 输出概率
            p_new = p_nodes[last_node] * p_trans * p_out
            p_news.append(p_new)
        p_nodes[this_node] = np.max(p_news)    # 更新节点路径概率
        last_index = np.argmax(p_news)         # 更新节点路径
        temp = path_nodes[last_index][:]
        temp.append(this_node)
        path_tmp[this_node] = temp
    for i in range(N):
        if not(path_tmp[i]==[i]):
            path_nodes[i]=path_tmp[i]
    path_tmp=[[0],[1],[2]]
#print(path_nodes)
print (max(p_nodes))
max_index = np.argmax(p_nodes)
max_path = path_nodes[max_index]
print(np.asarray(max_path)+1)
end=time.time()
time=end-start
print(time)
print(len(path_nodes[2]))
print(len(max_path))


