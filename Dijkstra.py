import time
import os

file = open('/Users/jiaxiaoyu/Downloads/graph1000_100020.txt')

# read all data to list
lines = file.readlines()

# close file
file.close()

# get the line number of 'Vertices' and 'Edges' to locate range of vertices and range of edges
v_index, e_index = lines.index('Vertices\n'), lines.index('Edges\n')

V_set = []
for line in lines[v_index + 1:e_index - 1]:  # read between Vertices and Edges
    v = line.strip('\n').split(',')  # Remove the line breaks at the end of each line, separated by commas into a list
    v = list(map(int, v))   # string list convert to int list
    V_set.append(v)  # append into vertex set，in form of [name,x,y]
E_set = [[-1 for n in range(len(V_set))] for n in range(len(V_set))] # initialize a 1000*1000 matrix and initialize all the value to -1,use -1 to represent no edge
for line in lines[e_index + 1:]:
    e = line.strip('\n').split(',')
    E_set[int(e[0])][int(e[1])] = int(e[2])   # store the edge into matrix
    E_set[int(e[1])][int(e[0])] = int(e[2])   # because the graph is undirected, so save edge inversely


# define a vertex class which contain three attributes
class vertex:

    def __init__(self, a, b, c):
        self.G = a      # G is the already cost
        self.name = b
        self.father = c

    def __str__(self):
        return '[' + str(self.G) + ',' + str(self.name) + ',' + str(self.father) + ']'

    # __eq__ and __hash__  is to remove duplicates so that can Significantly reduce the amount of calculations
    def __eq__(self, o: object) -> bool:
        return self.G == o.G and self.name == o.name and self.father == o.father

    def __hash__(self) -> int:
        return self.G + self.name + self.father


# set up a open set,a close set, a start vertex and a end vertex
start_vertex=''
end_vertex=''
openset=[]     # open set store the vertices which are waited to be examed
closeset=[]    # close set store the verticles which are no longer need to be examed


# define a function:move the the vertex whose has the minimal G from the openset to the closeset， and return this vertex's name
def move():
    name0 = -1    # initialize
    G0 = 99999    # use 9999 to represent infinite
    v0 = vertex(0, -1, -1, )
    for v in openset:
        if v.G < G0:
            name0 = v.name
            G0 = v.G
            v0 = v

    closeset.append(v0)
    openset.remove(v0)
    return name0


# define a function:find neighbor vertices which are not in closeset
def findneighbor(name):
    neighbor = []
    for idx, e in enumerate(E_set[name]):
        if e != -1 and not idx in map(lambda x: x.name, closeset): # if e!= -1 mean have edge, find vertices which are not in closeset,and have edge connect
            neighbor.append(idx)

    return neighbor

# define a function to calculate G to select vertex with the smallest G
def shortestpath(processing_vertex=vertex(0, -1, -1), possible_vertex=[]):
    for name in possible_vertex:
        for v1 in openset:
            if name == v1.name:
                G = ''
                if E_set[name][processing_vertex.name] != -1:  # -1 means no edge between
                    G = processing_vertex.G + E_set[name][processing_vertex.name]  # G=the G(alreadly cost) of the processing vertex + the edge value between these two vertices
                # choose the vertex with the smallest G and set the processing vertex to be this vertex's father
                if G < v1.G:
                    v1.G = G
                    v1.father = processing_vertex.name

                continue
        # openset do not have
        G = ''
        if E_set[name][processing_vertex.name] != -1:
            G = processing_vertex.G + E_set[name][processing_vertex.name]

        temp = vertex(G, name, processing_vertex.name)
        openset.append(temp)  # append this vertex to openset


# define a function to judge whether path is found or not, if found reture 1, if not found return -1
def findpath():
    for v in closeset:
        if v.name == end_vertex:
            return 1

    return -1

# define a function to output the path
def outputpath():
    temp = (0, -1, -1)
    for v in closeset:
        if v.name == end_vertex:
            temp = v
            break

    path = []
    v = temp
    # append the vertex(name)in the path to path[], from the end vertex using the attribute father of each vertex(record in shortestpath function)to get the vertex in path one by one
    while v.name != start_vertex:
        path.append(v.name)
        for vertex in closeset:
            if vertex.name == v.father:
                v = vertex
                break
    path.append(start_vertex)  # in the end, append the start vertex(name) to path[]
    path.reverse()             # reverse the path[] because it begin from the end vertex

    print('shortest path is :' + str(path))
    print('distance is :' + str(temp.G))

# input your start vertex and end vertex
start_vertex = int(input("Enter your start vertex: "))
if start_vertex + 1 > len(V_set):
    print('this vertex is not in the graph')
    os._exit(0)
end_vertex = int(input("Enter your end vertex: "))
if end_vertex + 1 > len(V_set):
    print('this vertex is not in the graph')
    os._exit(0)

start=time.time()

openset = [vertex(0, start_vertex, -1)]   # add the start vertex(name) into openset

while len(openset) == 1 or findpath() != 1:   # the while loop stop when can not find the end vertex, the openset is empty or the path has already been found
    openset = list(set(openset))  # Remove duplicates
    v1 = move()
    v2 = findneighbor(v1)
    v3 = vertex(0, -1, -1)
    for v in closeset:
        if v.name == v1:
            v3 = v
            break

    shortestpath(v3, v2)

if findpath() == -1:            # findpath()=-1 mean can not find path
    print('can not find path')

outputpath()

end=time.time()
clock=end-start
print('clock time is :' + str(clock) + 's')

