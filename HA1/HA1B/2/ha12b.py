import random

#Toss balls in bins. Full bin => coin
def coin_function(u, k, c):
    bins = [0] * (2 ** u)
    bin_cap = k
    coins = 0
    coin_goal = c
    balls = 0

    while coins < coin_goal:
        balls += 1
        bin_index = int(random.random() * len(bins))
        bins[bin_index] += 1
        if bins[bin_index] >= bin_cap:
            coins += 1
            bins[bin_index] = 0

    return balls


#Loop over the function to accumulate a mean and print it out
def meanBalls(u,k,c,t):
    x = 0
    sum = 0
    while(x <  t):
        sum += coin_function(u,k,c)
        x +=1
    
    return sum/t 


print(meanBalls(19,2,10000,1000))