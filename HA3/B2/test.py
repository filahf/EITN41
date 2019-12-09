import numpy as np

def main():
    #coeffs for p1
    p1_poly = [4,4,7,9]
    #given shares from the other participants’ polynomials
    received_shares = [34,52,36,34,35,39]
    #[index,value] for each of the collabs
    collabs = [[3, 2080], [6, 12469], [7, 19052]]
    
    
    combined_shares = sum(p1_poly) + sum(received_shares)
    collabs.append([1,combined_shares])
    calculate_secret(collabs)

def calculate_secret(poly):
    #https://stackoverflow.com/questions/44471236/python-code-for-lagrange-interpolation-determining-the-equation-of-the-polynom
    equations = np.array([[index[0] ** i for i in range(len(poly))] for index in poly])
    values = np.array([index[1] for index in poly])
    coef = np.linalg.solve(equations, values)
    print('Secret:', coef[0])

if __name__ == "__main__":
    main()