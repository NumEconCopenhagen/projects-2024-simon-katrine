from scipy import optimize
from types import SimpleNamespace
import math

class modelprojectclass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        par.alpha = 1/3
        par.omega = 0.0007
        par.s = 0.3
        par.delta = 0.05
        par.n = 0.02
        par.g = 0.02
        par.gama = 0.022
        par.Z_hat = 36.8
        par.psi =  0.0001
        par.theta = 0.00003


    def temperature(self,S):
        """ Function for temperature"""

        par = self.par
        return par.omega*S
    

    def emission_total(self,S,a):
        """ Function for how much CO2 there is in the next period"""

        par = self.par
        return S + (par.Z_hat - a)
    

    def capital(self,K,A,L):
        """Function for capital in the next period"""

        par = self.par
        return par.s * self.GDP(A,L,K) + (1-par.delta)*K
    

    def labour(self,L):
        """Function for labour in the next period"""

        par = self.par
        return (1+par.n)*L
    

    def technology (self,A):
        """Function for technology in the next period"""

        par = self.par
        return (1+par.g)*A
    

    def damage(self,S):
        """ How much the temperature affects the economy"""

        par = self.par
        return math.exp(-(par.gama * (self.temperature(S)**2))/2)
    

    def abetment(self,a):
        """How much active climate policy affects the economy"""

        par = self.par
        return math.exp((par.psi((par.Z_hat-a)**2)) - ((par.theta*((par.Z_hat-a)**2))/2))


    def GDP(self,A,L,K):
        """ Function for GDP"""

        par = self.par
        return self.damage(S) * self.abetment(a) * (K**par.alpha)*((A*L)**(1-par.alpha))

    
    #def solve_ss(alpha, c):
        """ Example function. Solve for steady state k. 
        
        Args:
        c (float): costs
        alpha (float): parameter
        
        Returns:
        result (RootResults): the solution represented as a RootResults object. """ 
        
        # a. Objective function, depends on k (endogenous) and c (exogenous).
        #f = lambda k: k**alpha - c
        #obj = lambda kss: kss - f(kss)
        #. b. call root finder to find kss.
        #result = optimize.root_scalar(obj,bracket=[0.1,100],method='bisect')
        #return result