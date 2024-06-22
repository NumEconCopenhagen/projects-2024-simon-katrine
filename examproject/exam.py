from types import SimpleNamespace
import numpy as np

class ExamClass():
     
    # Question 1

    # Question 2
    def __init__(self):

        par = self.par = SimpleNamespace()

        par.J = 3
        par.N = 10
        par.K = 10000

        par.F = np.arange(1,par.N+1)
        par.sigma = 2

        par.v = np.array([1,2,3])

        par.c = 1
        par.question_2 = False


    def simulate_career_choices(self):

        par = self.par 
        np.random.seed(0)  # set seed
    
        # we initialize storage for results for K simulations and N individuals
        self.prior_expectation= np.zeros((par.K, par.N))
        self.chosen_career = np.zeros((par.K, par.N), dtype=int)
        self.realized_value= np.zeros((par.K, par.N))
        #self.switch_shares = np.zeros((par.N, par.J))

        for k in range(par.K):
            for i in range(par.N):
            
                # 1) First we should find the prior expected average utility of each career track given the friends
                # Since person i has i friends, and par.F = np.arange(1,par.N+1) and we loop over N = 10, but python starts the loop at 0, then F[0] = 1 aka F[i] = i
                # We start out by finding friends epsilon
                friend_epsilon = np.random.normal(loc=0, scale=par.sigma, size=(par.F[i], par.J))  # par.F[i] and par.J since it is J*F_i
                friend_utility = par.v + friend_epsilon
                prior_expected_average_utility = np.mean(friend_utility, axis=0)

                if par.question_2:
                    for j in range(par.J):
                        if j != self.chosen_career[k, i]:
                            prior_expected_average_utility[j] -= par.c

                # we should also find their own noise term, epsilon
                own_epsilon = np.random.normal(loc=0, scale=par.sigma, size=(par.J)) #par.J since it is their J noise terms
            
                # 2) we should now find the career track with the highest expected utility 
                highest_expected_utility = np.argmax(prior_expected_average_utility)
            
                # 3) Store det different things
                # We should now store the choosen careers (highest expected average utility), 
                self.chosen_career[k, i] = highest_expected_utility
                # We should store the prior expectation of their chosen carer 
                self.prior_expectation[k, i] = prior_expected_average_utility[highest_expected_utility]
                # We should store the realized value of their chosen career track
                own_utility = par.v + np.mean(own_epsilon, axis=0)
                self.realized_value[k, i] = own_utility[highest_expected_utility]

                if par.question_2:
                    for j in range(par.J):
                        if j != self.chosen_career[k, i]:
                            self.realized_value[k, i] = own_utility[highest_expected_utility] - par.c
        
        return self.chosen_career, self.prior_expectation, self.realized_value
    



