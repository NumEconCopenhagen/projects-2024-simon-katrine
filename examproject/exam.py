from types import SimpleNamespace
import numpy as np
from scipy.optimize import fsolve

class ExamClass():
     
    # Parameters needed 
    def __init__(self):

        par = self.par = SimpleNamespace()

        # Question 1 parameters
        par.A = 1.0
        par.gamma = 0.5
        par.alpha = 0.3
        par.nu = 1.0
        par.epsilon = 2.0
        par.kappa = 0.1

        par.tau = 0.0
        par.T = 0.0

        # Wage as numeraire
        par.w = 1 

        # Question 2 parameters 
        par.J = 3
        par.N = 10
        par.K = 10000

        par.F = np.arange(1,par.N+1)
        par.sigma = 2

        par.v = np.array([1,2,3])

        par.c = 1
        par.question_3 = False

    


    # For question 1
    def labor_demand_1(self,p1):
        par = self.par
        return (p1 * par.A * par.gamma / par.w)**(1 / (1 - par.gamma))

    def labor_demand_2(self,p2):
        par = self.par
        return (p2 * par.A * par.gamma / par.w)**(1 / (1 - par.gamma))

    def production_output_1(self,p1):
        par = self.par

        L1 = self.labor_demand_1(p1)
        return par.A * L1**par.gamma

    def production_output_2(self,p2):
        par = self.par

        L2 = self.labor_demand_2(p2)
        return par.A * L2**par.gamma

    def profit_1(self,p1):
        par = self.par

        L1 = self.labor_demand_1(p1)
        return ((1-par.gamma)/par.gamma)*par.w*L1

    def profit_2(self,p2):
        par = self.par

        L2 = self.labor_demand_2(p2)
        return ((1-par.gamma)/par.gamma)*par.w*L2

    def consumer_demand_1(self, p1, p2):
        par = self.par

        pi1 = self.profit_1(p1)
        pi2 = self.profit_2(p2)
        L1 = self.labor_demand_1(p1)
        
        return par.alpha*((par.w * L1 + par.T + pi1 + pi2) / p1)
    
    def consumer_demand_2(self, p1, p2):
        par = self.par

        pi1 = self.profit_1(p1)
        pi2 = self.profit_2(p2)
        L2 = self.labor_demand_2(p1)
        
        return (1-par.alpha)*((par.w * L2 + par.T + pi1 + pi2) / (p2 + par.tau))

    def labor_supply_eq(self,l,p1,p2):
        par = self.par

        c1 = self.consumer_demand_1(p1, p2)
        c2 = self.consumer_demand_2(p1, p2)
        return par.alpha / c1 + (1 - par.alpha) / c2 - par.nu * l**par.epsilon #differentiad l*
    
    def compute_market_errors(self, p1, p2):
        
        # Labor market error
        L1 = self.labor_demand_1(p1)
        L2 = self.labor_demand_2(p2)
        labor_supply = fsolve(lambda l: self.labor_supply_eq(l,p1, p2), x0=1.0)[0]
        labor_error = L1 + L2 - labor_supply

        # Goods market 1 error
        y1 = self.production_output_1(p1)
        c1 = self.consumer_demand_1(p1, p2)
        goods1_error = y1 - c1

        # Goods market 2 error
        y2 = self.production_output_2(p2)
        c2 = self.consumer_demand_2(p1, p2)
        goods2_error = y2 - c2
        
        return labor_error, goods1_error, goods2_error
    
    def utility(self, c1, c2, l):
        par = self.par
        return np.log(c1 ** par.alpha * c2 ** (1 - par.alpha)) - par.nu * (l ** (1 + par.epsilon)) / (1 + par.epsilon)

    def update_transfer(self, tau, p1, p2):
        par = self.par
        c2 = self.consumer_demand_2(p1, p2)
        par.T = tau * c2

    def social_welfare(self, tau, p1, p2):
        par = self.par

        self.update_transfer(tau, p1, p2)
        y2 = self.production_output_2(p2)
        c1 = self.consumer_demand_1(p1, p2)
        c2 = self.consumer_demand_2(p1, p2)
        L = fsolve(lambda l: self.labor_supply_eq(l, p1, p2), x0=1.0)[0]  # Solve for labor supply
        U = self.utility(c1, c2, L)
        return U - par.kappa * y2

    

    # For question 2
    def simulate_career_choices(self):

        par = self.par 

        np.random.seed(0)  # set seed
    
        # we initialize storage for results for K simulations and N individuals
        self.prior_expectation= np.zeros((par.K, par.N))
        self.chosen_career = np.zeros((par.K, par.N), dtype=int)
        self.realized_value= np.zeros((par.K, par.N))
        self.j_own_utility= np.zeros((par.K, par.N))

        for k in range(par.K):
            for i in range(par.N):
                
                # 1)find the prior expected average utility of each career track given the friends
                # Since person i has i friends in each career, and par.F = np.arange(1,par.N+1) and we loop over N = 10, but python starts the loop at 0, then F[0] = 1 aka F[i] = i's friends
                friend_epsilon = np.random.normal(loc=0, scale=par.sigma, size=(par.F[i], par.J))  
                friend_utility = par.v + friend_epsilon
                prior_expected_average_utility = np.mean(friend_utility, axis=0)

                # their own noise term, epsilon
                own_epsilon = np.random.normal(loc=0, scale=par.sigma, size=(par.J)) 
            
                # 2) find the career track with the highest expected utility 
                highest_expected_utility = np.argmax(prior_expected_average_utility)
            
                # 3) 
                # store the choosen careers (highest expected average utility), 
                self.chosen_career[k, i] = highest_expected_utility
    
                # store the prior expectation of their chosen carer 
                self.prior_expectation[k, i] = prior_expected_average_utility[highest_expected_utility]
                
                # store the realized value of their chosen career track
                own_utility = par.v + own_epsilon
                self.realized_value[k, i] = own_utility[highest_expected_utility]
            
                if par.question_3:
                    # we define their current utility as the utility when choosing j^*
                    current_utility = own_utility[highest_expected_utility]

                    for j in range(par.J):
                        if j != highest_expected_utility: 
                            # we find the expected utility given j
                            expected_utility_switch = prior_expected_average_utility[j]

                            # if their expected utility from a switch minus the cost c is higher than their current utility they switch
                            if expected_utility_switch - par.c > current_utility:
                                # we update their career choice, prior expectation and realized value
                                self.chosen_career[k, i] = j
                                self.prior_expectation[k, i] = prior_expected_average_utility[j] - par.c
                                self.realized_value[k, i] = own_utility[j] - par.c
                                break  # break loop after first valid switch

                        # if no switch occurs nothing changes
                        self.prior_expectation[k, i] = prior_expected_average_utility[highest_expected_utility]
                        self.realized_value[k, i] = own_utility[highest_expected_utility]
                    
        return self.chosen_career, self.prior_expectation, self.realized_value

    # For question 3
    def find_closest_points(X,y):
        rng = np.random.default_rng(2024)
        X = rng.uniform(size=(50,2))
        y = rng.uniform(size=(2,))

        A = None
        B = None
        C = None
        D = None

        min_dist_A = float('inf')
        min_dist_B = float('inf')
        min_dist_C = float('inf')
        min_dist_D = float('inf')
    
        for x in X:
            if x[0] > y[0] and x[1] > y[1]: # check the condtion
                dist = np.linalg.norm(x - y) # find distance between x and y
                if dist < min_dist_A: # check if the found distance is less than the stored distance 
                    min_dist_A = dist # if it is it updates min_dist_A
                    A = x # updates A to store the point x
                
            elif x[0] > y[0] and x[1] < y[1]:
                dist = np.linalg.norm(x - y)
                if dist < min_dist_B:
                    min_dist_B = dist
                    B = x
                
            elif x[0] < y[0] and x[1] < y[1]:
                dist = np.linalg.norm(x - y)
                if dist < min_dist_C:
                    min_dist_C = dist
                    C = x
                
            elif x[0] < y[0] and x[1] > y[1]:
                dist = np.linalg.norm(x - y)
                if dist < min_dist_D:
                    min_dist_D = dist
                    D = x
    
        return A, B, C, D




    



