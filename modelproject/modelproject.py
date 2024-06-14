from types import SimpleNamespace

class modelprojectclass:
    
    def __init__(self):

        par = self.par = SimpleNamespace()

        # paramters
        par.alpha = 0.33
        par.s = 0.3
        par.n = 0.02
        par.delta = 0.05
        par.phi = 0.5
        par.L = 1
  
    