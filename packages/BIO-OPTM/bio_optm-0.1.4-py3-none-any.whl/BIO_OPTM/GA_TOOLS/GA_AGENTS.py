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
        
        if mode == "max":
            self.best_performance = -np.inf
        else:
            self.best_performance = np.inf
        self.best_solution = []
        self.generations = generations
        self.generation = 0
        self.mR = mutation_rate
        self.cR = crossOver_rate
        self.chromosomes = dict()
        self.chromosomes_fittness = dict()
        self.objective_function = objective_func
        self.mode=mode
        
        
        if mode == "min":
            self.bestScore = np.inf
            self.assessor = min
        else:
            self.bestScore = -np.inf
            self.assessor = max
        self.init()

    def init_pop(self, ):
        self.chromosomes.clear()
        self.chromosomes_fittness.clear()

        #  Randomly initialize solution population
        for c in range(self.population_size):
            # print(self.chromosomeAlphabet)
            self.chromosomes[c] = RNG_gen.choice(self.chromosomeAlphabet, self.chromosome_size)
            # print(f"c: {c}, chromos: {self.chromosomes[c]}")
            self.chromosomes_fittness[c] = 0    
    
    
    def init(self, ):
        """
            Quick way to get to the initialization method
        """
        self.init_pop()
        
        
    def observePerformance(self, chromosome, score, **kwargs):
        """
            Will store the score for the given chromosome (number)
            Arguments: 
            * chromosome: the number in the chromosome list that got this score
            * score: numeric value for the objective function of the test
        """
        # Track largest score for funsies
        # if score > self.best_performance:
        # print(f"\n\n\n------------------Best: {self.best_performance}--------------------------> score: {score}\n\n\n\n")
        
        if score == self.assessor(self.best_performance, score):
            self.best_performance = score
            self.best_solution = self.chromosomes[chromosome]
        self.chromosomes_fittness[chromosome] = score


    def rank_performance(self, **kwargs):
        """Sorts chromos based on their performance. If the mode is set to 'min' 
           all scores are substracted from the maximum scores and this values replaces the 
           scores for each chromo. This makes it so that the highest scoreing chromo 
           becomes the lowest and vice versa
        """
        #  If in minimimum finding mode replace the score achieved
        #  with maxScore - score. This will make the highest score 
        #  the smallest and vice versa 
        if self.mode == "min":
            maxval = np.max(list(self.chromosomes_fittness.values()))
            # print(f"Maxvalue: {maxval}")
            for c in self.chromosomes_fittness:
                self.chromosomes_fittness[c] = maxval - self.chromosomes_fittness[c]
        # otherwise just sort in ascending order based on the scores
        # NOTE: This is not needed with the methods I am using now but I will leave it here for now (10/19/23)
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
        # basic bit flipping mutation method
        # mp1 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        # mp2 = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        mp1 = np.random.default_rng().choice(range(self.chromosome_size), 1)[0]
        mp2 = np.random.default_rng().choice(range(self.chromosome_size), 1)[0]
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
        # based on params, do cross-over operation 
        # with some prob
        if np.random.default_rng().random() <= self.cR:
            kid_a, kid_b = self.cross_over(parent_a, parent_b) 
        else: 
            kid_a, kid_b =  parent_a, parent_b
       # base on params with some prob do mutation for each child
        return self.childrenMutation(kid_a, kid_b)
    
    def generateBreedingPairs(self, ):
        # adjust scores and rank agents
        self.rank_performance()

        # store the fitness scores for the agents sorted on their objective scores
        fitness = list(self.chromosomes_fittness.values())

        # store the indices related to the scores
        # we will use this list to pull pairs based on their scores since the score
        ranked_chromo = list(self.chromosomes_fittness.keys()) 
        
        # Convert scores into (Probabilities) based on the sum of the fitness scores
        # the below is just some checks to ensure we are not dividing by zero
        # it will just make them all equally likely 
        if sum(fitness) == 0:
            breeding_probs = np.around(np.array(list([1]*len(fitness)))/len(fitness), 4)
        else:
            breeding_probs = np.around(fitness/np.sum(fitness), 2)
            # breeding_probs = fitness/np.sum(fitness)
        # print(f"ranked: {ranked_chromo}")
        # print(f"fitness: {fitness}")
        # print(f"probs: {breeding_probs}")
        summed = 0

         # # the below ensures we have probs that sum to 1
        breeding_probs = self.ensureUnity(breeding_probs)
        

        # Now iterate through the pairs randomly selecting 
        # breeding pairs and return this list of parents
        couplings = list()   # will be a list of pairs
        patience = 5
        for i in range(int(np.ceil(self.population_size/2))):
            kid_a = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
            c = 0
            while True: # avoid inbreeding
                kid_b = np.random.default_rng().choice(ranked_chromo, 1, p=breeding_probs, replace=False)[0]
                # print(f"parent-A: {kid_a}, parent-B: {kid_b}")
                if kid_b != kid_a:
                    break
                c += 1
                if c >= patience:
                    print("out of patience")
                    print(f"crhomose: {ranked_chromo}")
                    while kid_b == kid_a:
                        print(f"OOP: A: {kid_a}, B: {kid_b}")
                        kid_b = np.random.default_rng().choice(ranked_chromo, 1, replace=False)[0]
            couplings.append([kid_a, kid_b])
        return couplings

    def ensureUnity(self, breeding_probs):
        # the below ensures we have probs that sum to 1
        summed = np.sum(breeding_probs);
        # for v in breeding_probs:
        #     summed += v
        

        # if we are over 1 reduce it by that amount 
        # by reducing the Lowest-scoring unit by the excess
        if summed > 1.0:
            adj = summed - 1.0 
            # way = adj/self.population_size
            # print(f"down adj: {adj}")
            # breeding_probs[0] = 0
            # 
            
            for v in range(len(breeding_probs)):
                if breeding_probs[v] - adj < 0:
                    val = breeding_probs[v]
                    breeding_probs[v] = 0
                    adj = adj - val
                else:
                    breeding_probs[v] -= adj
                    adj -= breeding_probs[v]
                if adj <= 0:
                    break
            #     breeding_probs[v] -= way
            # breeding_probs[0] -= adj
            # breeding_probs[0] = max(breeding_probs[0], 0)
        summed = np.sum(breeding_probs)
        
        # if we are less than 1 increase the sum by that amount 
        # by Increasing the highest-scoring unit by the excess
        if summed < 1.0:
            adj = 1 - summed
            way = adj/self.population_size
            
            for v in range(len(breeding_probs)):
                breeding_probs[v] += way
            
        
        return breeding_probs
    
    def survivalOfTheFittest(self, ):
        # ******************** Pair Off ***********************
        #  generate breeding pairs based on performance
        breeding_pairs = self.generateBreedingPairs()
        
        # set up for the next generation
        Next_Gen = list()
        
        # generate and store new solutions
        for parent_a, parent_b in breeding_pairs:
            # breed the paired agents 
            kidA, kidB = self.breed_pair(self.chromosomes[parent_a], 
                                            self.chromosomes[parent_b])
            
            Next_Gen.append(kidA)
            Next_Gen.append(kidB)
        
        
        # replace the last generation with the new one
        self.chromosomes_fittness.clear()
        self.chromosomes.clear()
        chromosome = 0
        while len(self.chromosomes) < self.population_size:
            self.chromosomes[chromosome] = Next_Gen[chromosome]
            self.chromosomes_fittness[chromosome] = 0
            chromosome += 1
        self.generation += 1


class GA_TSPOptimizer(GA_OptimizerOmegaMin):
    def __init__(self, chromosome_size: int, population_size: int, chromosomeAlphabet: int, generations: int, mutation_rate: float, crossOver_rate: float, 
                 objective_func: sum_obj, mode: str, 
                 DistanceMat: np.array,
                 **kwargs) -> None:
        super().__init__(chromosome_size, population_size, chromosomeAlphabet, generations, mutation_rate, crossOver_rate, objective_func, mode, **kwargs)
        self.adjacencyMat = DistanceMat
        
    def init_pop(self, ):
        #  initialize solution population
        for c in range(self.population_size):
            self.chromosomes[c] = RNG_gen.choice(self.chromosomeAlphabet, self.chromosome_size, replace=False)
            self.chromosomes[c] = self.fixRepeats(self.chromosomes[c])
            # print(f"c: {c}, chromos: {self.chromosomes[c]}")
            self.chromosomes_fittness[c] = 0  
    
    def cross_over(self, parent_a, parent_b, **kwargs):
        # get random cross over point
        cp = np.random.default_rng().choice(range(1, self.chromosome_size), 1)[0]
        
        # create children
        kid_a = list(parent_a)[0:cp] + list(parent_b)[cp:] 
        kid_b = list(parent_b)[0:cp] + list(parent_a)[cp:] 
        kid_a = self.fixRepeats(kid_a)
        kid_b = self.fixRepeats(kid_b)
        return kid_a, kid_b

    def fixRepeats(self, chromosome):
        seen = list()
        for gene in range(len(chromosome)):
            #  if this one is already seen 
            # print(f"chromo: {chromosome}")
            if chromosome[gene] in seen:
                # print(f"Seen: {seen}")
                # print(f"c: {chromosome[gene]}")
                for o in self.chromosomeAlphabet:
                    if o not in chromosome:
                        chromosome[gene] = o
            seen.append(chromosome[gene])
        return chromosome