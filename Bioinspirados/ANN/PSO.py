import numpy as np


class Particula:

    def __init__(self, xinf, xsup) -> None:
        self.d = len(xinf)
        self.xinf = xinf
        self.xsup = xsup
        self.x = np.array([np.random.uniform(self.xinf[i],self.xsup[i]) for i in range(self.d)])
        self.v = np.array([np.random.uniform(self.xinf[i],self.xsup[i]) for i in range(self.d)])
        self.p = np.copy(self.x)
        self.fx = float('inf')
        self.pbest = float('inf')
        
    def update(self,g, phi1, phi2, chi):
        r_phi1 = np.random.uniform(0.00001,phi1,self.d)
        r_phi2 = np.random.uniform(0.00001,phi2,self.d)
        tmp_local = self.p - self.x
        tmp_local = r_phi1 * tmp_local
        tmp_global = g - self.x
        tmp_global = r_phi2 * tmp_global
        tmp_v = chi * (self.v + tmp_local + tmp_global)
        tmp_v = np.clip(tmp_v, self.xinf, self.xsup)
        self.v = np.copy(tmp_v)
        tmp_x = self.x + self.v
        tmp_x = np.clip(tmp_x, self.xinf, self.xsup)
        self.x = np.copy(tmp_x)

class PSO:
    def __init__(self, problem, xinf, xsup, pop_size = 30, max_it = 100, phi1 = 2.05, phi2 = 2.05 ) -> None:
        self.pop_size = pop_size
        self.max_it = max_it
        self.phi1 = phi1
        self.phi2 = phi2
        phi = self.phi1 + self.phi2
        self.chi = 2 / (phi - 2 + (phi**2 - 4 * phi)**0.5)
        self.pop = [Particula(xinf, xsup) for _ in range(self.pop_size)]
        self.f_obj = problem
        
    def optimize(self, verbose = False):
        gbest = Particula(xinf, xsup)
        for i in range(self.max_it):
            for p in self.pop:
                p.fx = self.f_obj(p.x)                
                if p.fx < p.pbest:
                    p.p = np.copy(p.x)
                    p.pbest = p.fx
            g = min(self.pop, key=lambda p:p.fx)
            g = np.copy(g.x)
            for p in self.pop:
                p.update(g, self.phi1, self.phi2, self.chi)
            g = min(self.pop, key=lambda p:p.fx)
            if g.fx < gbest.fx:
                gbest.x = np.copy(g.x)    
                gbest.fx = g.fx
            if verbose:
                print(f'It {(i+1)}\tBest Particle: x = {gbest.x}, fx = {gbest.fx}')
            
        return gbest


def sphere_function(x):
    return np.sum(x**2)


if __name__=='__main__':
    d = 100
    xinf = np.repeat(-5.12, d)
    xsup = np.repeat(5.12,d)
    pso = PSO(sphere_function, xinf, xsup, max_it=1000, pop_size=50)   
    sol = pso.optimize()
    print(f'Solucion: x={sol.x}, fx={sol.fx}')