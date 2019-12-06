from hashlib import sha1
import matplotlib.pyplot as plt
import numpy as np 
import random

def create_commit(v,k):
    v_value = bin(v)[2:]
    k_value = bin(k)[2:]
    vk = v_value + k_value
    commit = bin(int(sha1(vk.encode()).hexdigest(),16))
    return commit




def conceal(trunc):
    k = random.randint(2 ** 15, 2 ** 16)
    ref_commit = create_commit(1,k)[2:trunc +2]
    commit_hit_0 = []
    commit_hit_1 = []
    for i in range(2**16):
        commit_0 = create_commit(0, i)[2:trunc +2]
        commit_1 = create_commit(1, i)[2:trunc +2]
        if commit_0 == ref_commit:
            commit_hit_0.append(commit_0)
        if commit_1 == ref_commit:
            commit_hit_1.append(commit_1)
    return len(commit_hit_1) / (len(commit_hit_0) + len(commit_hit_1))
        



# https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return len(lst3) 



def find_collisions():
    commit_v_1 = []
    commit_v_0 = []
    graph_x = []
    #binding
    grap_y = []
    #conceal
    grap_y_c = []
    
    for k in range(2 ** 15, 2 ** 16):
        commit_v_0.append(create_commit(0,k))
        commit_v_1.append(create_commit(1,k))
        
    
    for trunc in range(1,40):
        v_0 = []
        v_1 = []
        for a,b in zip(commit_v_0,commit_v_1):
            v_0.append(a[2:trunc +2])
            v_1.append(b[2:trunc +2])

        print("Calculating probability with commit length:",trunc)
        graph_x.append(trunc)
        grap_y_c.append(conceal(trunc))
        
        #Find collisions
        if (intersection(v_0,v_1) / len(v_0)) > 0:
            grap_y.append(1)
        else:
            grap_y.append(0)


    print_graph(graph_x,grap_y,grap_y_c)


#https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
def print_graph(x,y,y2):
    # plotting the points  
    plt.plot(x, y,label = "Binding")
    plt.plot(x, y2,label = "Conceal") 
    
    # naming the x axis 
    plt.xlabel('Commit length') 
    # naming the y axis 
    plt.ylabel('Probability') 
    
    # giving a title to my graph 
    #plt.title('Intersection per length of commit') 
    plt.legend()
    # function to show the plot 
    plt.show() 


find_collisions()
        









