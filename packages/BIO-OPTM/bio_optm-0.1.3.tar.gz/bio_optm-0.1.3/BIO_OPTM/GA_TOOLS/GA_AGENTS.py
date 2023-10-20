import numpy as np
import pandas as pd
import random 

RNG_gen = np.random.default_rng()

sum_obj = lambda X: np.sum(X)

class GA_AGENT:
    def __init__(self, 
                 chromosome_size: int or list or 4,
                 population_size: int or list or 10, 
                 chromosomeAlphabet: int or list,
                 generations: int or 100,
                 mutation_rate: float or .1,
                 crossOver_rate: float or .7,
                 objective_func: sum_obj,
                 **kwargs,
                 ) -> None:
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.chromosomeAlphabet = chromosomeAlphabet
        self.best_performance = -np.inf
        self.best_solution = []
        self.generations = generations
        self.generation = 0
        self.mR = mutation_rate
        self.cR = crossOver_rate
        self.chromosomes = dict()
        self.chromosomes_fittness = dict()
        self.objective_function = objective_func
        self.init()

    def init_pop(self, ):
        #  initialize solution population
        for c in range(self.population_size):
            self.chromosomes[c] = RNG_gen.choice(self.chromosomeAlphabet, self.chromosome_size)
            print(f"c: {c}, chromos: {self.chromosomes[c]}")
            self.chromosomes_fittness[c] = 0    
    
    
    def init(self, ):
        self.init_pop()
        
        
    def observePerformance(self, chromosome, score, **kwargs):
        if score > self.best_performance:
            self.best_performance = score
            self.best_solution = self.chromosomes[chromosome]
        self.chromosomes_fittness[chromosome] = score


    def rank_performance(self, **kwargs):
        self.chromosomes_fittness = dict(sorted(self.chromosomes_fittness.items(), 
                                            key=lambda x:[1]))
    
    
    def cross_over(self, parent_a, parent_b, **kwargs):
        # get random cross over point
        cp = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        
        # create children
        kid_a = list(parent_a)[0:cp] + list(parent_b)[cp:] 
        kid_b = list(parent_b)[0:cp] + list(parent_a)[cp:] 
        return kid_a, kid_b
    
    def mutate(self, agent, **kwargs):
        mp1 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        mp2 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        tmp = agent[mp1]
        agent[mp1] = agent[mp2]
        agent[mp2] = tmp
        return agent
        
    def childrenMutation(self, kid_a, kid_b, **kwargs):
        #  do random mutation for each child
        for i in range(2):
            if np.random.default_rng().random() <= self.mR:
                if i == 0:
                    kid_a = self.mutate(kid_a)
                else:
                    kid_b = self.mutate(kid_b)
        return kid_a, kid_b
    
    def breed_pair(self, parent_a, parent_b,**kwargs):
        if np.random.default_rng().random() <= self.cR:
            kid_a, kid_b = self.cross_over(parent_a, parent_b) 
        else: 
            kid_a, kid_b =  parent_a, parent_b
       
        return self.childrenMutation(kid_a, kid_b)
    
    def generateBreedingPairs(self, ):
        self.rank_performance()
        
        fittness = list(self.chromosomes_fittness.values())
        
        ranked_chromo = list(self.chromosomes_fittness.keys()) 
        if sum(fittness) == 0:
            breeding_probs = np.around(np.array(list([1]*len(fittness)))/len(fittness))
        else:
            breeding_probs = np.around(fittness/np.sum(fittness), 3)
        print(f"ranked: {ranked_chromo}")
        print(f"fittness: {fittness}")
        print(f"probs: {breeding_probs}")
        summed = 0
        
        for v in breeding_probs:
            summed += v
        print(f"summed: {summed}")

        if summed > 1.0:
            adj = summed - 1 
            print(f"down adj: {adj}")
            breeding_probs[-1] -= adj
            
        elif summed < 1.0:
            adj = 1 - summed
            print(f"up adj: {adj}")
            breeding_probs[-1] += adj 

        couplings = list()
        patience = 5
        for i in range(int(np.ceil(self.population_size/2))):
            kid_a = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
            c = 0
            while True:
                kid_b = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
                print(f"A: {kid_a}, B: {kid_b}")
                if kid_b != kid_a:
                    break
                c += 1
                if c >= patience:
                    print("out of patience")
                    while kid_b == kid_a:
                        print(f"OOP: A: {kid_a}, B: {kid_b}")
                        kid_b = np.random.default_rng().choice(ranked_chromo, 1, replace=False)[0]
            couplings.append([kid_a, kid_b])
        return couplings
    
    
    def survivalOfTheFittest(self, ):
        #  generate breeding pairs based on performance
        breeding_pairs = self.generateBreedingPairs()
        
        # set up for the next generation
        Next_Gen = list()
        
        for parent_a, parent_b in breeding_pairs:
            Next_Gen.append(self.breed_pair(self.chromosomes[parent_a], 
                                            self.chromosomes[parent_b]))
        
        # replace the last generation with the new one
        self.chromosomes_fittness.clear()
        self.chromosomes.clear()
        chromosome = 0
        while len(self.chromosomes) < self.chromosome_size:
            self.chromosomes[chromosome] = Next_Gen[chromosome][0]
            self.chromosomes_fittness[chromosome] = 0
            if len(self.chromosomes) >= self.chromosome_size:
                break
            self.chromosomes[chromosome+1] = Next_Gen[chromosome][1]
            self.chromosomes_fittness[chromosome+1] = 0
            chromosome += 1
            print(f"chr: {chromosome}")
            print(f"len: {len(self.chromosomes)}")



class GA_OptimizerOmegaMin:
    def __init__(self, 
                 chromosome_size: int or list or 4,
                 population_size: int or list or 10, 
                 chromosomeAlphabet: int or list,
                 generations: int or 100,
                 mutation_rate: float or .1,
                 crossOver_rate: float or .7,
                 objective_func: sum_obj,
                 mode: str or "max",
                 **kwargs,
                 ) -> None:
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.chromosomeAlphabet = chromosomeAlphabet
        self.best_performance = -np.inf
        self.best_solution = []
        self.generations = generations
        self.generation = 0
        self.mR = mutation_rate
        self.cR = crossOver_rate
        self.chromosomes = dict()
        self.chromosomes_fittness = dict()
        self.objective_function = objective_func
        self.mode=mode
        self.init()

    def init_pop(self, ):
        #  initialize solution population
        for c in range(self.population_size):
            print(self.chromosomeAlphabet)
            self.chromosomes[c] = RNG_gen.choice(self.chromosomeAlphabet, self.chromosome_size)
            print(f"c: {c}, chromos: {self.chromosomes[c]}")
            self.chromosomes_fittness[c] = 0    
    
    
    def init(self, ):
        self.init_pop()
        
        
    def observePerformance(self, chromosome, score, **kwargs):
        # if score > self.best_performance:
        if score < self.best_performance:
            self.best_performance = score
            self.best_solution = self.chromosomes[chromosome]
        self.chromosomes_fittness[chromosome] = score


    def rank_performance(self, **kwargs):
        if self.mode == "min":
            maxval = np.max(list(self.chromosomes_fittness.values()))
            for c in self.chromosomes_fittness:
                self.chromosomes_fittness[c] = maxval - self.chromosomes_fittness[c]
        
        self.chromosomes_fittness = dict(sorted(self.chromosomes_fittness.items(), 
                                            key=lambda x:[1]))
    list
    
    def cross_over(self, parent_a, parent_b, **kwargs):
        # get random cross over point
        cp = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        
        # create children
        kid_a = list(parent_a)[0:cp] + list(parent_b)[cp:] 
        kid_b = list(parent_b)[0:cp] + list(parent_a)[cp:] 
        return kid_a, kid_b
    
    def mutate(self, agent, **kwargs):
        mp1 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        mp2 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        tmp = agent[mp1]
        agent[mp1] = agent[mp2]
        agent[mp2] = tmp
        return agent
        
    def childrenMutation(self, kid_a, kid_b, **kwargs):
        #  do random mutation for each child
        for i in range(2):
            if np.random.default_rng().random() <= self.mR:
                if i == 0:
                    kid_a = self.mutate(kid_a)
                else:
                    kid_b = self.mutate(kid_b)
        return kid_a, kid_b
    
    def breed_pair(self, parent_a, parent_b,**kwargs):
        if np.random.default_rng().random() <= self.cR:
            kid_a, kid_b = self.cross_over(parent_a, parent_b) 
        else: 
            kid_a, kid_b =  parent_a, parent_b
       
        return self.childrenMutation(kid_a, kid_b)
    
    def generateBreedingPairs(self, ):
        self.rank_performance()
        
        fittness = list(self.chromosomes_fittness.values())
        
        ranked_chromo = list(self.chromosomes_fittness.keys()) 
        if sum(fittness) == 0:
            breeding_probs = np.around(np.array(list([1]*len(fittness)))/len(fittness))
        else:
            breeding_probs = np.around(fittness/np.sum(fittness), 3)
        print(f"ranked: {ranked_chromo}")
        print(f"fittness: {fittness}")
        print(f"probs: {breeding_probs}")
        summed = 0
        
        for v in breeding_probs:
            summed += v
        print(f"summed: {summed}")

        if summed > 1.0:
            adj = summed - 1 
            print(f"down adj: {adj}")
            breeding_probs[-1] -= adj
            
        elif summed < 1.0:
            adj = 1 - summed
            print(f"up adj: {adj}")
            breeding_probs[-1] += adj 

        couplings = list()
        patience = 5
        for i in range(int(np.ceil(self.population_size/2))):
            kid_a = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
            c = 0
            while True:
                kid_b = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
                print(f"A: {kid_a}, B: {kid_b}")
                if kid_b != kid_a:
                    break
                c += 1
                if c >= patience:
                    print("out of patience")
                    while kid_b == kid_a:
                        print(f"OOP: A: {kid_a}, B: {kid_b}")
                        kid_b = np.random.default_rng().choice(ranked_chromo, 1, replace=False)[0]
            couplings.append([kid_a, kid_b])
        return couplings
    
    
    def survivalOfTheFittest(self, ):
        #  generate breeding pairs based on performance
        breeding_pairs = self.generateBreedingPairs()
        
        # set up for the next generation
        Next_Gen = list()
        
        for parent_a, parent_b in breeding_pairs:
            Next_Gen.append(self.breed_pair(self.chromosomes[parent_a], 
                                            self.chromosomes[parent_b]))
        
        # replace the last generation with the new one
        self.chromosomes_fittness.clear()
        self.chromosomes.clear()
        chromosome = 0
        while len(self.chromosomes) < self.population_size:
            self.chromosomes[chromosome] = Next_Gen[chromosome][0]
            self.chromosomes_fittness[chromosome] = 0
            if len(self.chromosomes) >= self.chromosome_size:
                break
            self.chromosomes[chromosome+1] = Next_Gen[chromosome][1]
            self.chromosomes_fittness[chromosome+1] = 0
            chromosome += 1
            print(f"chr: {chromosome}")
            print(f"len: {len(self.chromosomes)}")
            
            
     
            
    