from types import SimpleNamespace

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3
        par.w1B = 0.2
        par.w2B = 0.7

        # c. vector
        par.p2 = 1



    def utility_A(self,x1A,x2A):
        """ Utility function for consumer A """

        par = self.par
        return (x1A**par.alpha)*(x2A**(1-par.alpha))


    def utility_B(self,x1B,x2B):
        """ Utility function for consumer B """

        par = self.par
        return (x1B**par.beta)*(x2B**(1-par.beta))

    def demand_A1(self,p1):
        """ Consumer A's demand for good 1 """

        par = self.par
        return par.alpha*((p1*par.w1A+par.p2*par.w2A)/p1)
    
    def demand_A2(self,p1):
        """ Consumer A's demand for good 2 """

        par = self.par
        return (1-par.alpha)*((p1*par.w1A+par.p2*par.w2A)/par.p2)

    def demand_B1(self,p1):
        """ Consumer B's demand for good 1 """

        par = self.par
        return par.beta*((p1*par.w1B+par.p2*par.w2B)/p1)
    
    def demand_B2(self,p1):
        """ Consumer B's demand for good 2 """

        par = self.par
        return (1-par.beta)*((p1*par.w1B+par.p2*par.w2B)/par.p2)

    def check_market_clearing(self,p1):

        par = self.par

        x1A = self.demand_A1(p1)
        x2A = self.demand_A2(p1)
        x1B = self.demand_B1(p1)
        x2B = self.demand_B2(p1)

        eps1 = x1A - par.w1A + x1B - (1 - par.w1A)
        eps2 = x2A - par.w2A + x2B - (1 - par.w2A)

        return eps1,eps2
    