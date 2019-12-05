from hashlib import sha1
import matplotlib.pyplot as plt

def create_commit(v,k):
    v_value = bin(v)[2:]
    k_value = bin(k)[2:]
    vk = v_value + k_value
    commit = bin(int(sha1(vk.encode()).hexdigest(),16))
    return commit

# https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return len(lst3) 


def find_collisions():
    commit_v_1 = []
    commit_v_0 = []
    graph_x = []
    grap_y = []
    for k in range(2 ** 15, 2 ** 16):
        commit_v_0.append(create_commit(0,k))
        commit_v_1.append(create_commit(1,k))
    
    for trunc in range(1,35):
        v_0 = []
        v_1 = []
        for a,b in zip(commit_v_0,commit_v_1):
            v_0.append(a[2:trunc +2])
            v_1.append(b[2:trunc +2])
        
        graph_x.append(trunc)
         
        grap_y.append(intersection(v_0,v_1) / len(v_0))


    print_graph(graph_x,grap_y)


#https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
def print_graph(x,y):
    # plotting the points  
    plt.plot(x, y) 
    
    # naming the x axis 
    plt.xlabel('Truncation') 
    # naming the y axis 
    plt.ylabel('Intersections') 
    
    # giving a title to my graph 
    plt.title('Intersection per length of commit') 
    
    # function to show the plot 
    plt.show() 


find_collisions()
        









