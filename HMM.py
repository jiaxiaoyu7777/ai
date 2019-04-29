import numpy as np
import time
start=time.time()
# 模型参数

A = np.asarray([[0.5748292, 0.2125854, 0.2125854], [0.2125854, 0.5748292, 0.2125854], [0.2125854, 0.2125854, 0.5748292]]) # 转移矩阵(骰子切换的概率)
B = np.asarray([[0.609538,0.35022354,0.04023844], [0.53583914,0.42132866,0.042832196], [0.44592032,0.14358002,0.41049963]])# 每个骰子掷出每个数字的概率矩阵
Pi = np.asarray([1/3, 1/3, 1/3]).transpose() # 开始时三个骰子被选择的概率相同都是1/3


# 观察的序列
O = np.asarray([3, 2, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 1, 3, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 2, 2, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3, 1, 1, 1, 2, 1, 1, 3, 1, 2, 3, 3, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 1, 2, 2, 1])

O=O-1

T = O.shape[0]
N = A.shape[0]   # 骰子数

#print(B[:,O[0]])
p_nodes = Pi * B[:, O[0]]     # 记录每个节点的路径概率
p=Pi * B[:, O[0]]
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
        p[this_node] =np.max(p_news)    # 记录节点路径概率
        last_index = np.argmax(p_news)         # 记录节点路径
        temp = path_nodes[last_index][:]
        temp.append(this_node)
        path_tmp[this_node] = temp
    for i in range(N):
        p_nodes[i]=p[i] #更新节点路径概率
        path_nodes[i]=path_tmp[i] #更新节点路径

#print(path_nodes)
print (max(p_nodes))
max_index = np.argmax(p_nodes)
max_path = path_nodes[max_index]
print(np.asarray(max_path)+1)
end=time.time()
time=end-start
print(time)



