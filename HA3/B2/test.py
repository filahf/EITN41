import numpy as np
from pypoly import Polynomial

def calculate_secret(poly):
    #https://stackoverflow.com/questions/44471236/python-code-for-lagrange-interpolation-determining-the-equation-of-the-polynom
    equations = np.array([[index[0] ** i for i in range(len(poly))] for index in poly])
    values = np.array([index[1] for index in poly])
    coef = np.linalg.solve(equations, values)
    print('Secret:', coef[0])



def main():
    #coeffs for p1
    p1_poly = [9, 19, 5]
    #given shares from the other participants’ polynomials
    received_shares = [ 37, 18, 40, 44, 28]
    #[index,value] for each of the collabs
    collabs = [[4, 1385],[5,2028]]
    
    
    combined_shares = sum(p1_poly) + sum(received_shares)
    collabs.append([1,combined_shares])
    calculate_secret(collabs)




if __name__ == "__main__":
    main()